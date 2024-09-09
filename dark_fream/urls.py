from dark_fream.template import LazyImport


def path(path, view, name=None):
    """
    Returns a dictionary containing information about the route.

    Args:
        path (str): Path URL-адреса.
        view (function): The function that handles the request to this path.
        name (str, optional): Route name. Defaults to None.
        methods (list, optional): List of HTTP methods supported by the route. Defaults to None.

    Returns:
        dict: Dictionary with keys 'path', 'view', 'name' and 'methods'.

    Example:
        >>> path('/home', my_view, 'home_page')
        {'path': '/home', 'view': my_view, 'name': 'home_page', 'methods': None}
        >>> path('', my_view, methods=['GET', 'POST'])
        {'path': '', 'view': my_view, 'methods': ['GET', 'POST']}
    """
    if not path.startswith('/'):
        path = '/' + path
    return {'path': path, 'view': view, 'name': name}

def include(path_url):
    """
    Returns a list of routes defined in the module specified in path_url.

    Args:
        path_url (str): Path to the module containing routes.

    Returns:
        list: List of routes defined in the module.

    Example:
        >>> include('myapp.urls')
        [{'path': '/home', 'view': my_view, 'name': 'home_page'},
         {'path': '/about', 'view': about_view, 'name': 'about_page'}]
    """
    urlpatterns = LazyImport(f'{path_url}', 'urlpatterns')
    print(urlpatterns)
    return urlpatterns
