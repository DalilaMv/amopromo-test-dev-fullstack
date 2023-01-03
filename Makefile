front_install:
	cd frontend && npm install 

front_start:
	cd frontend && npm start

back_venv:
	cd backend/company/ && virtualenv .venv2 --python=3.8

back_install:
	cd backend/company/ && pip install -r requirements.txt

back_run:
	cd backend/company/ && python manage.py runserver

back_tests:
	cd backend/company/ && python manage.py test

	