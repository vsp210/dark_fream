# dark_fream
Мой собственный фреймворк dark_fream.

## Привет я молодой 14 летний программист который патается создавать невозможное


#### dark_fream - Мой собственный фреймворк основаный на всеми известном Django
dark_fream - это фреймворк который позволяет создавать крайне простые веб-сайты
#### dark_fream - Основные функции:
+ **Создание моделей** - Создание моделей для базы данных крайне схожая с Django но имеет меньший функционал например:
- **CharField**
- **TextField**
- **IntegerField**
- **ImageField** (работает запись но получить данные из бд крайне сложно сможете исправить пишите контакты ниже)
- и т. д.

+ **Работа с шаблонами** - Работа с шаблонами похожая с Django например:
- **render** (рендерит шаблон)
- **redirect** (изменяет ваш url)

+ **Работа с url** - тут всё также как и в джанго например:
- **path** (создает url)

### Запуск проекта

- для запуска требуется слонировать репозиторий командой:
```git clone https://github.com/vsp210/dark_fream.git```
- затем рекомендую создать venv
~~~bash
py -3.* -m venv venv
source venv/Scripts/activate
~~~
- затем установите зависимости командой:
~~~bash
pip install -r requirements.txt
~~~
- перейдите в папку:
~~~bash
cd dark_fream
~~~
- затем создайте приложение командой:
~~~bash
python -m dark_fream.app createapp **
~~~
где * - любое название
- затем запустите проект командой:
~~~bash
python -m dark_fream.app runserver
~~~

- можно запускать сервер на выброчном адресе или порте
~~~bash
python -m dark_fream.app runserver <adress> <port>
~~~

### Контакты
- **ВКонтакте**: https://vk.com/vsp210
- **Телеграм**: https://t.me/vsp210
- **Электронная почта**: vsp210@gmail.com

### dark_fream - Мой собственный фреймворк основаный на всеми известном Django с открытым исходным кодом

### Пример использования:

- dark_fream/app/models.py:
~~~python
from dark_fream.models import *


# ваша модель
class User(Model):
    user = CharField()
    password = CharField()
    phone = CharField()
~~~

- dark_fream/app/views.py:
~~~python
from .models import *
from dark_fream.template import render

# ваш код
def home(request):
    User.create_table()
    user = User(user='vsp210', password='1234', phone='8 888 888 88 88')
    user.save()
    return render(request, 'home.html')

~~~

- dark_fream/app/urls.py:
~~~python
from .views import *
from dark_fream.urls import path

urlpatterns = [
    # ваши urls
    path('', home, name='home'),
]
~~~
- dark_fream/templates/home.html:
~~~html
<!DOCTYPE html>
<html>
    <head>
        <title>Home</title>
    </head>
    <body>
        <h1>Home</h1>
    </body>
</html>
~~~

### Пояснение:
В этом примере мы создали базовую структуру приложения DarkFream с базой данных и моделью User
Мы также добавили функцию home в views.py, которая создает нового пользователя и сохраняет его после каждой перезагрузки
В urls.py мы добавили url для функции home
В home.html мы добавили простую HTML-страницу с заголовком "Home"

## Предупреждаю!
## После любых изменений несчитая шаблонов нужно перезапускать сервер

##### Версия 3
