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
DB_HOST=127.0.0.1 
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
  
- Copy the contents of the file docker-compose-production.xml from the **infra** directory to the file you created

```bash
mkdir foodgram-project-react
cd foodgram-project-react
touch docker-compose.yml
```
- Create a file .env in the project folder:
```.env
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_passwords
DB_HOST=db 
DB_PORT=5432
SECRET_KEY='your_secret_django_settings'
DEBUG=False
ALLOWED_HOSTS='*'
```
- Pulls an image associated with a service defined in a compose.yaml file.
```bash
sudo docker compose pull
```
- Builds, (re)creates, starts, and attaches to containers for a service. Run containers in the background.
```bash
sudo docker compose up -d
```
- Perform migrations:
```bash
sudo docker compose exec backend python manage.py migrate
```
- Collect static files from multiple apps into a single path
```bash
sudo docker compose exec backend python manage.py collectstatic
sudo docker compose exec backend cp -r /app/collected_static/. /app/staticfiles/
```
- Fill in the database with test data: 
```bash
sudo docker compose exec backend python manage.py loaddata tags ingredients
sudo docker compose exec backend python manage.py importjson
```

## API example request:

## users

#### New user registration (allow any):
  
POST http://localhost:8000/api/users/

* Payload:
```json
{
    "email": "djohn@hollywood.com",
    "username": "John",
    "first_name": "John",
    "last_name": "Malkovich",
    "password": "Caligula37"
}
```
* Response: 
```json
{
    "id": 16,
    "username": "John",
    "email": "djohn@hollywood.com",
    "first_name": "John",
    "last_name": "Malkovich"
}
```
#### Get Token:
  
POST http://localhost:8000/auth/token/login/

* Payload:
```json
{
    "email": "djohn@hollywood.com",
    "password": "Caligula37"
}
```
* Response: 
```json
{
    "auth_token": "a449f2f60f77d0eec99bbdbd316524580fb06903"
}
```
## recieps

#### Add new reciep (only authorized):
  
POST http://localhost:8000/api/recipes/

* Payload:
```json
{
  "ingredients": [
    {
      "id": 1,
      "amount": 10
    },
    {
      "id": 2,
      "amount": 10
    }
  ],
  "tags": [
    1,
    4
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "Something edible (this is not accurate)",
  "text": "Cook these ingredients somehow",
  "cooking_time": 5
}
```
* Response: 
```json
{
    "id": 19,
    "tags": [
        {
            "id": 1,
            "name": "Breakfast",
            "color": "#ADFF2F",
            "slug": "breakfast"
        },
        {
            "id": 4,
            "name": "Supper",
            "color": "#8A2BE2",
            "slug": "supper"
        }
    ],
    "author": {
        "id": 16,
        "username": "John",
        "email": "djohn@hollywood.com",
        "first_name": "John",
        "last_name": "Malkovich",
        "is_subscribed": false
    },
    "ingredients": [
        {
            "id": 1,
            "name": "Russet potatoes",
            "measurement_unit": "pound",
            "amount": 10
        },
        {
            "id": 2,
            "name": "Kosher salt",
            "measurement_unit": "teaspoon",
            "amount": 10
        }
    ],
    "is_favorited": false,
    "is_in_shopping_cart": false,
    "name": "Something edible (this is not accurate)",
    "image": "http://localhost:8000/media/dishes/temp_qGc3cZ8.png",
    "text": "Cook these ingredients somehow",
    "cooking_time": 5
}
```

#### Get recieps with limit (allow any):

GET http://localhost:8000/api/recipes/?limit=2

* Response: 
```json
{
    "count": 16,
    "next": "http://localhost:8000/api/recipes/?limit=2&page=2",
    "previous": null,
    "results": [
        {
            "id": 4,
            "tags": [
                {
                    "id": 2,
                    "name": "Lunch",
                    "color": "#556B2F",
                    "slug": "lunch"
                },
                {
                    "id": 3,
                    "name": "Dinner",
                    "color": "#00BFFF",
                    "slug": "dinner"
                }
            ],
            "author": {
                "id": 1,
                "username": "John",
                "email": "djohn@hollywood.com",
                "first_name": "John",
                "last_name": "Malkovich",
                "is_subscribed": false
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "Russet potatoes",
                    "measurement_unit": "pound",
                    "amount": 3
                },
                {
                    "id": 2,
                    "name": "Kosher salt",
                    "measurement_unit": "teaspoon",
                    "amount": 1
                },
                {
                    "id": 3,
                    "name": "Egg",
                    "measurement_unit": "pcs",
                    "amount": 1
                },
                {
                    "id": 4,
                    "name": "All-purpose flour",
                    "measurement_unit": "cup",
                    "amount": 1
                }
            ],
            "is_favorited": false,
            "is_in_shopping_cart": false,
            "name": "Potato Gnocchi",
            "text": "You will be pleasantly surprised at how easily you can turn out homemade gnocchi that cooks up soft and tender. They work well with pesto or red sauce -- but they are also delicious just tossed with butter.",
            "cooking_time": 105,
            "image": "http://localhost:8000/media/dishes/temp_8H02YvJ.jpeg"
        },
        {
            "id": 5,
            "tags": [
                {
                    "id": 1,
                    "name": "Breakfast",
                    "color": "#ADFF2F",
                    "slug": "breakfast"
                },
                {
                    "id": 3,
                    "name": "Dinner",
                    "color": "#00BFFF",
                    "slug": "dinner"
                }
            ],
            "author": {
                "id": 1,
                "username": "John",
                "email": "djohn@hollywood.com",
                "first_name": "John",
                "last_name": "Malkovich",
                "is_subscribed": false
            },
            "ingredients": [
                {
                    "id": 5,
                    "name": "Sweet onion",
                    "measurement_unit": "pcs",
                    "amount": 1
                },
                {
                    "id": 6,
                    "name": "Dried chives",
                    "measurement_unit": "teaspoon",
                    "amount": 2
                },
                {
                    "id": 7,
                    "name": "Ground chipotle",
                    "measurement_unit": "teaspoon",
                    "amount": 1
                },
                {
                    "id": 8,
                    "name": "Buttermilk",
                    "measurement_unit": "cup",
                    "amount": 1
                },
                {
                    "id": 9,
                    "name": "Gluten-free panko",
                    "measurement_unit": "cup",
                    "amount": 1
                },
                {
                    "id": 10,
                    "name": "Gluten-free potato flakes",
                    "measurement_unit": "cup",
                    "amount": 1
                }
            ],
            "is_favorited": false,
            "is_in_shopping_cart": false,
            "name": "Air Fryer Onion Rings with Onion Dip",
            "text": "Onions are probably one of my favorite pantry ingredients: they’re inexpensive, full of flavor and have a long shelf life. However, they don’t always get to be the star of the show—until now! The air fryer is a great tool for making a gluten-free version of traditional onion rings, here accompanied by an onion dip made with, yes, raw onions. Soaking the onions in buttermilk helps take away some of the bite!",
            "cooking_time": 55,
            "image": "http://localhost:8000/media/dishes/temp_yQMJNho.jpeg"
        }
    ]
}
```

## shopping cart

#### Add reciep to shopping cart (only authorized):
POST http://localhost:8000/api/recipes/4/shopping_cart/

* Response: 
```json
{
    "id": 4,
    "name": "Potato Gnocchi",
    "cooking_time": 105,
    "image": "/media/dishes/temp_8H02YvJ.jpeg"
}
```
#### Download the list of ingredients from the recipes added to the shopping cart (only authorized):
GET http://localhost:8000/api/recipes/download_shopping_cart/
* Response file: shopping-list.txt
```txt
All-purpose flour cup 1
Egg pcs 1
Kosher salt teaspoon 1
Russet potatoes pound 3
```

### Author:  
_Eugen Dolgor_<br>

### Supervisor:  
_Anna_<br>

### Reviewer:  
_Alex_<br>


