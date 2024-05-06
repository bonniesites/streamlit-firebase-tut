#!/bin/bash

# Stop and remove containers
docker-compose down

# Remove unused Docker volumes
docker volume prune -f

# Remove images created today
docker images --format '{{.ID}} {{.CreatedAt}}' | \
    awk -v today=$(date +%Y-%m-%d) '$2 ~ today { print $1 }' | \
    while read -r image_id; do
        # Stop and remove containers based on this image
        docker ps -aq --filter ancestor=$image_id | xargs docker stop
        docker ps -aq --filter ancestor=$image_id | xargs docker rm -f      
        # Remove the image
        docker rmi $image_id
    done

# Clean up
dot_clean .

# Build and start containers
docker compose up --build -d
# docker-compose watch


