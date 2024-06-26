# Test task for Hammer Systems 

This project aims to provide a custom authentication system and referral logic.
## Technologies Used

- Python 3.9
- Django 2.2.16
- Django Rest Framework 3.12.4
- PostgreSQL
- Docker

## Installation of the project:
Clone the repository and change into it on the command line:

	git clone https://github.com/mityay36/hamer_test/

Make your own .env file in main directory. All required variables are listed in .env.example

#### Start Docker Compose in daemon mode

    docker-compose -f docker-compose.yml up --build

#### Make migrations and collect static of your project
    docker-compose -f docker-compose.yml exec backend python manage.py makemigrations
    docker-compose -f docker-compose.yml exec backend python manage.py migrate
    docker-compose -f docker-compose.yml exec backend python manage.py collectstatic
    docker-compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /backend_static/static/

#### Perform your own superuser
    docker-compose -f docker-compose.yml exec backend python manage.py createsuperuser

### Congrats! Now you can access the application docs at [localhost](http://localhost:8000/api/docs)

### Examples of server responses

Request URL:

	http://127.0.0.1:8000/api/v1/auth/signup/
 
Sample response:

 	{
	    "phone_number": "+79008007060",
	    "confirmation_code": "1111"
	}

Request URL:

 	http://127.0.0.1:8000/api/v1/auth/token/
  
Sample response:

  	{
	    "token": "generated_token"
	}

Request URL:

	http://127.0.0.1:8000/api/v1/users/me
 
Sample response:

	 {
	    "phone_number": "+79060847800",
	    "first_name": "",
	    "last_name": "",
	    "bio": "",
	    "role": "user",
	    "referral_code": "X3bfHa",
	    "user_referrals": []
	}


## Author
[Dmitry Pokrovsky](https://github.com/mityay36)
