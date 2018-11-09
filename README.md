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
- api/interactions/types
    - Print all interaction types (i.e. subsidie,begeleiding,financiering,..)
- api/overlap
    - Print the interaction overlap between partners (endpoint for upset plot)
    - param: limit (limits the overlaps for beter performance) 
- api/overlap/filter
    - Endpoint for filtering the interaction overlaps (endpoint for upset plot)
    - params: timeframe (between interactions in weeks), type (interaction type), limit
- api/upload/
    - endpoint for uploading excel files (in progress)
    - the content-type header should be set to multipart/form-data
    - the excel file is putted in the key `file`
    - return an array of warnings (string) and one of:
        - array of errors (string) if errors
        - an upload_id (int)
    - call HELP http method for details
- api/apply/<upload_id>
    - apply the upload file
- api/view
    - params: max_depth(int)
    - criteria: two possibles values are "partner" (default) and "interaction"
    - endpoint for sunburst chart 
