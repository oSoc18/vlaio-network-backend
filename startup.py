import os

os.system("docker-compose rm");
#os.system("docker stop $(docker ps -a -q)")
os.system("docker-compose up -d");
os.system("docker-compose exec web python3 manage.py makemigrations");
os.system("docker-compose exec web python3 manage.py migrate");
os.system("docker-machine ls");
