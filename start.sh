docker-compose rm
docker rm $(docker stop $(docker ps -a -q --filter ancestor=vlaio-network-backend_web --format="{{.ID}}"))
docker rm $(docker stop $(docker ps -a -q --filter ancestor=postgres --format="{{.ID}}"))
docker-compose up -d
docker-compose exec web python3 manage.py makemigrations
docker-compose exec web python3 manage.py migrate
docker-compose exec web python3 insert_mock.py
docker-machine ls