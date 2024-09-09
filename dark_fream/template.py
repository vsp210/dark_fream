import os
import sys
from jinja2 import Environment, FileSystemLoader

try:
    from settings.settings import *
except ModuleNotFoundError:
    pass

class LazyImport:
    """
    A lazy import mechanism to import modules and attributes on demand.

    Args:
        module_name (str): The name of the module to import.
        attribute_name (str): The name of the attribute to import from the module.

    Example:
        >>> lazy_import = LazyImport('math', 'sin')
        >>> lazy_import.sin(3.14)  # imports math and calls sin(3.14)
    """
    def __init__(self, module_name, attribute_name):
        self.module_name = module_name
        self.attribute_name = attribute_name
        self.module = None

    def __getattr__(self, name):
        if self.module is None:
            self.module = __import__(self.module_name, fromlist=[self.attribute_name])
        return getattr(self.module, name)


class Global:
    def __init__(self):
        self.values = {}

    def add(self, name, value):
        self.values[name] = value

    def get(self, name):
        return self.values.get(name)

    def upd(self, name=None, upd_value=None):
        if name is not None:
            self.values[name] = upd_value
            return self.values[name]

global_instance = Global()

try:
    for app in APPS:
        urlpatterns = LazyImport(f'{app}.urls', 'urlpatterns')
except NameError:
    urlpatterns = []

def url(endpoint):
    url = f"/{endpoint}"
    return url

def render(request, template_name, context={}, templates='templates'):
    """
    Renders a template with the given context.

    Args:
        request: The request object.
        template_name (str): The name of the template to render.
        context (dict): The context to pass to the template.
        templates (str): The directory where templates are located.

    Returns:
        str: The rendered template as a string.

    Example:
        >>> render(request, 'hello.html', {'name': 'John'})  # renders hello.html with name='John'
    """
    env = Environment(loader=FileSystemLoader(templates))
    env.globals['url'] = url
    template = env.get_template(template_name)
    return template.render(context)


def redirect(name, method='GET'):
    """
    Redirects to a URL pattern by name.

    Args:
        name (str): The name of the URL pattern to redirect to.
        method (str): The HTTP method to use for the redirect. Defaults to 'GET'.

    Returns:
        dict: A dictionary with the redirect response.

    Example:
        >>> redirect('login')  # redirects to the URL pattern named 'login' with GET method
        >>> redirect('login', 'POST')  # redirects to the URL pattern named 'login' with POST method
    """
    for urlpattern in urlpatterns.urlpatterns:
        if urlpattern['name'] == name:
            return {
                'status_code': 302,
                'headers': {
                    'Location': urlpattern['path']
                },
                'method': method
            }
