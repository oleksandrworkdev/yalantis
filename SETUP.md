SETUP GUIDE

Prerequisites:
Python version >= 3.9.0

Activate virtual env:
1. python3 -m venv env
2. source env/bin/activate
3. pip install pip -U
4. pip install -r requirements.txt
5. python manage.py migrate
6. python manage.py runserver 8000

Deactivate virtual env:
1. deactivate

Run tests:
1. Activate virtual env
2. python manage.py test cars_park_api



