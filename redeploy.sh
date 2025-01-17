cd <repo_path>
git pull
docker build -f Dockerfile.pi . -t mplus-api
docker stop $(docker ps -a | grep mplus-api | awk '{print $1}')
docker rm $(docker ps -a | grep mplus-api | awk '{print $1}')
docker run -d -p 8080:8080 mplus-api
