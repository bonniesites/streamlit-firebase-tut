import docker
from datetime import datetime, timedelta

# Connect to Docker
client = docker.from_env()

# Get current date
today = datetime.now().date()

# Get list of all images
images = client.images.list()


# Filter images created today
images_today = []
for image in images:
    created_str = image.attrs['Created']
    created_datetime = datetime.strptime(created_str.split('.')[0], "%Y-%m-%dT%H:%M:%S")
    if created_datetime.date() == today:
        images_today.append(image)

# Remove images created today
for image in images_today:
    client.images.remove(image.id, force=True)

# Rebuild Docker containers using Docker Compose
# You can execute this command using subprocess or any other method you prefer

# For example, using subprocess:
import subprocess
subprocess.run(["docker-compose", "up", "--build"])


