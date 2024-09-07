from dark_fream.template import LazyImport


def path(path, view, name=None):
    """
    Возвращает словарь, содержащий информацию о маршруте.

    Args:
        path (str): Путь URL-адреса.
        view (function): Функция, обрабатывающая запрос к этому пути.
        name (str, optional): Имя маршрута. Defaults to None.

    Returns:
        dict: Словарь с ключами 'path', 'view' и 'name'.

    Example:
        >>> path('/home', my_view, 'home_page')
        {'path': '/home', 'view': my_view, 'name': 'home_page'}
        >>> path('', my_view)
        {'path': '', 'view': my_view, 'name': None}
    """
    if not path.startswith('/'):
        path = '/' + path
    return {'path': path, 'view': view, 'name': name}


def include(path_url):
    """
    Возвращает список маршрутов, определенных в модуле, указанном в path_url.

    Args:
        path_url (str): Путь к модулю, содержащему маршруты.

    Returns:
        list: Список маршрутов, определенных в модуле.

    Example:
        >>> include('myapp.urls')
        [{'path': '/home', 'view': my_view, 'name': 'home_page'},
         {'path': '/about', 'view': about_view, 'name': 'about_page'}]
    """
    urlpatterns = LazyImport(f'{path_url}', 'urlpatterns')
    return urlpatterns
