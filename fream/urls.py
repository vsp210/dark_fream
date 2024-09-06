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
        {'path': '/', 'view': my_view, 'name': None}
    """
    if path == '':
        path = '/'
    return {'path': path, 'view': view, 'name': name}
