# run this from startach machine on amazon aws (ssh startach)

cd ~/deploy/minyaneto-backend
git pull
OLD_IMAGE=$(docker images startach/minyaneto-backend --format "{{ .ID}}")
docker stop minyaneto-backend && docker rm minyaneto-backend && docker rmi $OLD_IMAGE
docker build -f ./Dockerfile -t startach/minyaneto-backend:$(date +"%Y%m%dT%H%M%S") .
NEW_IMAGE=$(docker images startach/minyaneto-backend --format "{{ .ID}}")
docker run -d --name="minyaneto-backend" -p 10080:80 -e SA_ES=https://search-startach-es-kjunyv6dur2zgmoygirwebhxaa.us-east-1.es.amazonaws.com:443 $NEW_IMAGE
