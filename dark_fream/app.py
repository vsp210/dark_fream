# myframework/app.py

import sys
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from dark_fream.template import render
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from settings.setings import APPS
except ModuleNotFoundError:
    pass

try:
    for app in APPS:
        views_module = __import__(f'{app}.views', fromlist=['*'])
        globals().update({name: getattr(views_module, name) for name in dir(views_module) if not name.startswith('_')})

        urls_module = __import__(f'{app}.urls', fromlist=['*'])
        urlpatterns = getattr(urls_module, 'urlpatterns')
except NameError:
    urlpatterns = []

class MyApp(BaseHTTPRequestHandler):
    def do_GET(self):
        if not urlpatterns:
            # display default page
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(render(self, 'index.html', templates='dark_fream/templates').encode())
            return

        for url_pattern in urlpatterns:
            if self.path == url_pattern['path']:
                response = url_pattern['view'](self)
                if response is None:
                    response = ""  # or some default response
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(response.encode())
                return
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(render(self, '404.html', templates='dark_fream/templates').encode())



def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyApp)
    print("Starting server...")
    httpd.serve_forever()

def create_app(app_name):
    os.mkdir(app_name)
    os.mkdir('settings')
    # добавление и заполнение файла
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

    with open(f'settings/setings.py', 'w', encoding='utf8') as f:
        f.write(f"""APPS = [
    '{app_name}'
]""")

if __name__ == "__main__":
    if sys.argv[1] == "runserver":
        run_server()
    if sys.argv[1] == "createapp":
        if len(sys.argv) != 3:
            print("Usage: python -m dark_fream.app createapp <app_name>")
            sys.exit(1)
        create_app(sys.argv[2])
    else:
        print("Unknown command")
        sys.exit(1)
