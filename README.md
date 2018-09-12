# VLAIO NETWORK
The backend for the VLAIO visualistion project. The project uses [Django](https://www.djangoproject.com) and [PostgreSQL](https://www.postgresql.org).

## Starting the project
Before starting the project, make sure [Docker](https://www.docker.com) and [docker-compose](https://docs.docker.com/compose/) are installed.

For starting the project on windows/mac/linux if python is installed, run the following command:

``` python startup.py ```


This script will:
- Stop other running docker containers from the same image
- Start the project using docker-compose
- Make and run all Django migrations
- Insert mock data
- Print IP where the project is running (windows only). For mac the project will be running on localhost:8000.

If you want to stop the project run the following command:

``` docker-compose down ```

## API endpoints
The API for this project was build using [Django Rest Framework](http://www.django-rest-framework.org).

The following endpoints have been created:
- api/companies
    - Print all companies
- api/partners
    - Print all partners
- api/interactions
    - Print all interactions between companies and partners
- api/interactions?name=*example*
    - Print all interactions between a company and a certain partner (by partner name)