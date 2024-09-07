import sys
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from dark_fream.template import render
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from settings.settings import *
except ModuleNotFoundError:
    pass
from winotify import Notification


try:
    for app in APPS:
        views_module = __import__(f'{app}.views', fromlist=['*'])
        globals().update({name: getattr(views_module, name) for name in dir(views_module) if not name.startswith('_')})

        urls_module = __import__(f'{app}.urls', fromlist=['*'])
        urlpatterns = getattr(urls_module, 'urlpatterns')
except NameError:
    urlpatterns = []

def messages(app_id, title, msg):
    icon_path = os.path.join(os.path.dirname(__file__), 'fream/icon.png')
    return Notification(app_id, title, msg, icon_path)


class MyApp(BaseHTTPRequestHandler):
    def do_GET(self):
        if not urlpatterns:
            if self.path == '/':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(render(self, 'index.html', templates='fream/templates').encode('utf-8'))
                return
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(render(self, '404.html', templates='fream/templates').encode('utf-8'))
                return

        for url_pattern in urlpatterns:
            if self.path.startswith(url_pattern['path']):
                response = url_pattern['view'](self)
                if response is not None:
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
                    return
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(render(self, '404.html', templates='fream/templates/404.html').encode('utf-8'))
        return




def run_server(port=8000, address='127.0.0.1'):
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

    with open(f'{app_name}/views.py', 'w', encoding='utf8') as f:
        f.write("""from .models import *
from dark_fream.template import render

# ваш код

""")
    with open(f'{app_name}/urls.py', 'w', encoding='utf8') as f:
        f.write("""from .views import *
from dark_fream.urls import path

urlpatterns = [
    # ваши urls
]
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
