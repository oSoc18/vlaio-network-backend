# VLAIO NETWORK
The backend for the VLAIO visualisation project. The project uses [Django](https://www.djangoproject.com) and [PostgreSQL](https://www.postgresql.org).

## Starting the project
Before starting the project, make sure [Docker](https://www.docker.com) and [docker-compose](https://docs.docker.com/compose/) are installed.

`docker-compose up -d --build`

The startup script will:
- Make and run all Django migrations
- Insert mock data
 
To stop:

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
