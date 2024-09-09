import html
import sys
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from dark_fream.template import render
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from settings.settings import *
except ModuleNotFoundError:
    pass
from winotify import Notification

urlpatterns = []

try:
    for app in APPS:
        views_module = __import__(f'{app}.views', fromlist=['*'])
        globals().update({name: getattr(views_module, name) for name in dir(views_module) if not name.startswith('_')})

        urls_module = __import__(f'{app}.urls', fromlist=['*'])
        urlpattern = getattr(urls_module, 'urlpatterns')
        for pattern in urlpattern:
            urlpatterns.append({'path': pattern['path'], 'view': pattern['view']})
    print(urlpatterns)
except ModuleNotFoundError:
    pass

def messages(app_id, title, msg):
    icon_path = os.path.join(os.path.dirname(__file__), 'dark_fream/icon.png')
    return Notification(app_id, title, msg, icon_path)


class Request:
    def __init__(self, method, path, data, headers=None, kwargs=None):
        self.method = method
        self.path = path
        self.data = data
        self.headers = headers
        self.kwargs = kwargs

class MyApp(BaseHTTPRequestHandler):
    def handle_response(self, response):
        if isinstance(response, dict) and 'status_code' in response:
            self.send_response(response['status_code'])
            for header, value in response.get('headers', {}).items():
                self.send_header(header, value)
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))


    def handle_404(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(render(self, '404.html', templates='dark_fream/templates').encode('utf-8'))


    def do_GET(self):
        if not urlpatterns:
            if self.path == '/':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(render(self, 'index.html', templates='dark_fream/templates').encode('utf-8'))
                return
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(render(self, '404.html', templates='dark_fream/templates').encode('utf-8'))
                return
        post_data = ''

        request = Request(
            method=self.command,
            path=self.path,
            data=post_data,
            headers=self.headers
        )

        for url_pattern in reversed(urlpatterns):
            if self.path == url_pattern['path']:
                response = url_pattern['view'](request)
                if response is not None:
                    self.handle_response(response)
                    return

        self.handle_404()
        return


    def do_POST(self):
        if not urlpatterns:
            self.send_response(405)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Method Not Allowed")
            return

        content_length = int(self.headers['Content-Length'])
        post_data_bytes = self.rfile.read(content_length)
        post_data = {key: html.unescape(value[0]) for key, value in urllib.parse.parse_qs(post_data_bytes.decode('utf-8')).items()}
        kwargs = {key: value for key, value in post_data.items() if key not in ['csrfmiddlewaretoken']}
        request = Request(
            method=self.command,
            path=self.path,
            data=post_data,
            kwargs=kwargs,
            headers=self.headers
        )
        for url_pattern in reversed(urlpatterns):
            if self.path == url_pattern['path']:
                response = url_pattern['view'](request)
                if response is not None:
                    self.handle_response(response)
                    return

        self.handle_404()
        return




def run_server(port=8000, address='127.0.0.1'):
    try:
        server_address = (address, int(port))
        httpd = HTTPServer(server_address, MyApp)
        try:
            if MESSAGES:
                toast = messages('Dark Fream', 'started', 'Server started on port 8000')
                toast.show()
        except NameError:
            print('App is not defined')
        print("Starting server...")
        print(f'Server running on http://{address}:{port}/')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        exit()
    except ConnectionAbortedError:
        print("\n")

def create_app(app_name):
    os.mkdir(app_name)
    if not os.path.exists('settings'):
        os.mkdir('settings')
        with open(f'settings/settings.py', 'a+', encoding='utf8') as f:
            f.write(f"""
MESSAGES = True
APPS = [
    '{app_name}',
]""")
        with open(f'settings/urls.py', 'w', encoding='utf8') as f:
            f.write("""from dark_fream.urls import path, include

urlpatterns = [
    # ваши urls
]
""")

    with open(f'{app_name}/views.py', 'w', encoding='utf8') as f:
        f.write("""from .models import *
from dark_fream.template import render

# ваш код

""")

    with open(f'{app_name}/models.py', 'w', encoding='utf8') as f:
        f.write("""from dark_fream.models import *


# ваша модель
""")
    with open(f'{app_name}/__init__.py', 'w', encoding='utf8') as f:
        pass


    toast = messages('Dark Fream', 'app created', 'app created')
    toast.show()
    print(f'App "{app_name}" created. You can start it by running "python -m dark_fream.app runserver"')

if __name__ == "__main__":
    if sys.argv[1] == "runserver":
        if len(sys.argv) == 2:
            run_server()
        elif len(sys.argv) == 3:
            run_server(sys.argv[2])
        else:
            run_server(sys.argv[2], sys.argv[3])
    if sys.argv[1] == "createapp":
        if len(sys.argv) != 3:
            print("Usage: python -m dark_fream.app createapp <app_name>")
            sys.exit(1)
        create_app(sys.argv[2])
    else:
        print("Unknown command")
        sys.exit(1)
