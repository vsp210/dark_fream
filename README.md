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

+ **Работа с шаблонами** - Работа с шаблонами похожая с Django например:
- **render** (рендерит шаблон)
- **redirect** (изменяет ваш url)
- **global_instance** (поможет сохранять данные глобально)

+ **Работа с url** - тут всё также как и в джанго например:
- **path** (создает url)
- **include** (включает url из другого файла)

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
- adress и port - необезательны
### Контакты
- **ВКонтакте**: https://vk.com/vsp210
- **Телеграм**: https://t.me/vsp210
- **Электронная почта**: vsp210@gmail.com

### dark_fream - Мой собственный фреймворк основаный на всеми известном Django с открытым исходным кодом

### Пример создания простого калькулятора:

- dark_fream/settings/urls.py:
~~~python
from dark_fream.urls import path, include

urlpatterns = [
    # ваши urls
    include('**.urls'),
]
~~~

- dark_fream/**/views.py:
~~~python
from .models import *
from dark_fream.template import render, global_instance, redirect
from dark_fream.functions.math import calculator

# ваш код

def home(request):
    if request.method == 'POST':
        data = request.data
        global_instance.add('data', data)
        return redirect('clac')
    return render(request, 'home.html', {'text': 'Hello'})


def clac(request):
    data = global_instance.get('data')
    if 'number1' in data and 'operation' in data and 'number2' in data:
        result = calculator(f"{data['number1']} {data['operation']} {data['number2']}")
        return render(request, 'home.html', {'text': result})
    else:
        return render(request, 'home.html', {'text': 'Invalid input data'})
~~~

- dark_fream/**/urls.py:
~~~python
from dark_fream.urls import *
from .views import *

urlpatterns = [
    # ваши urls
    path('', home),
    path('clac', clac, name='clac')
]

~~~
- dark_fream/templates/home.html:
~~~html
<!DOCTYPE html>
<html>
    <head>
        <title>Home</title>
        <meta charset="UTF-8"> <-- Рекомендую использовать эту строчку для избежания ошибки кодировки -->
    </head>
    <body>
        <form method="post" action="{{ url('') }}">
            <label for="name">Первое число:</label>
            <input type="number" id="number1" name="number1"><br><br>
            <label for="name">Второе число:</label>
            <input type="number" id="number2" name="number2"><br><br>
            <label for="name">Операция:</label>
            <select id="operation" name="operation">
            <option value="+">+</option>
            <option value="-">-</option>
            <option value="*">*</option>
            <option value="/">/</option>
            </select>
            <input type="submit" value="Submit">
        </form>
        <h1>{{ text }}</h1>
    </body>
</html>
~~~

### Пояснение:
В этом примере мы создали пример калькулятора
- dark_fream/settings/urls.py:
В этом фаиле мы указываем где надо искать urlpatterns
- dark_fream/**/views.py:
В этом файле мы создаем функцию home, которая будет обрабатывать GET и POST запросы с условием если запрос POST то переходить на страницу calc а также сохраняет данные которые передавались из шаблона. Затем функция calc с помошью функции calculator (встроеной в dark_fream) считает и отправляет результат
- dark_fream/**/urls.py:
В этом файле мы указываем urlpatterns
- dark_fream/templates/home.html:
В этом файле мы создаем форму которая будет отправлять POST запросы на страницу сalc и выводить результат на страницу home.
### Примечание:
В этом примере мы использовали функцию calculator которая встроеная в dark_fream.


## Предупреждаю!
## После любых изменений несчитая шаблонов нужно перезапускать сервер

##### Версия 1 (release)
