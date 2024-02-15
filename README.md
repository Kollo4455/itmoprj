# itmoprj

На выбор есть две версии automl:
1. lightautoml в ветке main
2. fedot в ветке fedot

Для запуска надо:  
1. Создать вирутальное окружение с питоном версии 3.8
2. Клонировать проект
```bash
git clone https://github.com/Kollo4455/itmoprj
```
3. Надо скачать mongoDB и установить его https://www.mongodb.com/try/download/community
4. В открытой консоле с виртуальным окружением установить пакеты
```bash
pip install -r itmoprj/requirements.txt
```
5. После установки пакетов, надо сделать миграцию
```bash
python itmoprj/manage.py migrate
```
6. Так же надо сделать себе аккаунт, либо можно воспользоваться встроенной функцией приложения
```bash
python itmoprj/manage.py createsuperuser
```
7. Для запуска надо набрать
```bash
python itmoprj/manage.py runserver
```
## Эндпоинты

* /app/predict (Предсказание)
* /app/learn-model (Обучение модели)
* /app/guid (памятка)
* /users/login (вход в аккаунт)
* /users/logout (выход из аккаунта)
* /users/register (регистрация нового пользователя)

