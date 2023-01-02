# amopromo-test-dev-fullstack

# Description


the following topics contain a brief explanation of what was done in each of the tasks performed in this project
###### PROBLEM 1

To solve this problem I chose to create a command called import_airports.py that can be called by a routine that will run the following command daily:
`python manage.py import_airports`

###### PROBLEM 2

To solve this problem I created a web interface using ReactJS and UmiJS. The requested page at this problem can be found directly at the initial page: `http://localhost:8001/`
It contains a datatable with the columns from the external api, the option to activate or inactivate (informing the reason) any airport and also a filter by status ("active" or "inactive").

###### PROBLEM 3

To solve this problem I created a View that can be found at the following directory: `backend/company/airport/views.py`
This view returns all the possible going and back flight combinations and their total price.

- request url example and it's params:
`http://localhost:8000/api/airport/flight-query?origin=POA&destination=MAO&departure_date=2023-10-01&return_date=2023-10-05`
  - origin - origin airport IATA
  - destination - destination airport IATA
  - departure_date - date of departure from the origin airport
  - return_date - date of return from the destination airport
<br>
- example of curl request:
  - `curl -X GET "http://127.0.0.1:8000/api/airport/flight-query?origin=POA&destination=MAO&departure_date=2023-10-01&return_date=2023-10-05" -H 'Authorization: Token eb4f768a22a1baaa4b485eb223af7fe308751da8'`
<br>
- obs.: the following token can be used in your request's header: `Token eb4f768a22a1baaa4b485eb223af7fe308751da8`


# Set Up

To configure the project the following configurations were used:

- Python version 3.8.10
- Node version 16.0.0

##### Backend setup

1. cd into `backend/company` directory
2. create a virtualenv
3. run `pip install -r requirements.txt`
4. run `python manage.py runserver` to run the project

##### Frontend setup

1. cd into `frontend`
2. run `npm install` or `yarn install`
3. run `npm start` or `yarn start`

# Technologies

This project was developed with the following technologies:

#### Frontend

- [ReactJS](https://pt-br.reactjs.org/) - React is an open source JavaScript front-end library focused on creating user interfaces on web pages.

- [UmiJS](https://v3.umijs.org/docs) - Umi is a routing-based framework that supports next.js-like conventional routing and various advanced routing functions, such as routing-level on-demand loading.

#### UI Framework

- [Ant Design](https://ant.design/components/overview/) - Antd provides plenty of UI components to enrich web applications and improve components experience consistently.

#### Backend

- [Python](https://docs.python.org/pt-br/3/) - Python is an interpreted, object-oriented, high-level programming language with dynamic semantics.
- [Django REST Framework](https://www.django-rest-framework.org/) - Django REST framework is a powerful and flexible toolkit for building Web APIs.

#### Database

- [SQLite](https://www.sqlite.org/docs.html) - SQLite is an in-process library that implements a self-contained, serverless, zero-configuration, transactional SQL database engine. The