[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=034230)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=034230)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=034230)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=034230)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=034230)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=034230)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=034230)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=034230)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=034230)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=034230)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=034230)](https://cloud.yandex.ru/)
## Foodgram - instagram for recipes
«Grocery Assistant»: This is a project created by Yandex Praktikum methodologists to teach students the basics of backend development and DevOps. There is no practical benefit from it. The user interface is terrible. But there is a collection of queries for Postman, which greatly simplifies development.

## Launching a project in developer mode

 - Clone the repository with the project to your computer. In the terminal, run the command from the working directory:
```bash
git clone git@github.com:eugensut/foodgram-project-react.git
```

- Go to subdirectory
```bash
cd foodgram-project-react'
```
- Create a virtual environment

```bash
python3.9 -m venv venv
```
- Activate the virtual environment:
  
```bash
source venv/bin/activate
```
- Update the pip Package manager
  
```bash
pip install --upgrade pip
```  

- Install dependencies from a file requirements.txt

```bash
pip install -r requirements.txt
```
- Create a file .env in the project folder:
```.env
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_passwords
DB_HOST=db 
DB_PORT=5432
SECRET_KEY='your_secret_django_settings'
DEBUG=True
ALLOWED_HOSTS='*'
```
- Perform migrations:
```bash
python3.9 manage.py migrate
```
- Create super user 
```bash
python3.9 manage.py createsuperuser
```
### Fill in the database with test data: 
```bash
python3.9 manage.py loaddata tags ingredients
```
- you can also download ingredients from csv and json files by putting them in the data directory.

```bash
python3.9 manage.py importcsv
python3.9 manage.py importjson
```
### Start a project: 
```bash
python3.9 manage.py runserver
```
## Launching a project via Docker

### Create a directory: 
- create a file in this directory for running multicontainer applications.
  
- Copy the contents of the file docker-compose-production.xml from the infra directory to the file you created

```bash
mkdir foodgram-project-react
cd foodgram-project-react
touch docker-compose.yml
```
