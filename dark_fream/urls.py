# код для распределения url адресов

def path(path, view, name=None):
    if path == '':
        path = '/'
    return {'path': path, 'view': view, 'name': name}
