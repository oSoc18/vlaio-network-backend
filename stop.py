import os

os.system("docker-compose rm")
print("Stopping VLAIO docker images:")
os.system('docker rm $(docker stop $(docker ps -a -q --filter ancestor=vlaio-network-backend_web --format="{{.ID}}"))')
os.system('docker rm $(docker stop $(docker ps -a -q --filter ancestor=postgres --format="{{.ID}}"))')