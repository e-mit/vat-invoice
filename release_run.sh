docker build --target release -t release:latest .

new_sha=$(docker images --no-trunc --quiet release:latest)
echo $new_sha

PORT=8000 && docker run -p 8080:${PORT} --name release -e PORT=${PORT} --rm release:latest

# docker stop -t 0 release
