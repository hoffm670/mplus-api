cd <repo_path>
git pull
docker build -f Dockerfile.pi . -t mplus-api
docker run -d -p 8080:8080 mplus-api