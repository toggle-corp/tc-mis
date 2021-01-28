Initial setup or Dockerfile is changed, make sure to update the containers with `docker-compose up -d` after a successful build.
```
docker-compose build  
```

To start the containers and view the logs. CTRL+C to stop the containers.
```
docker-compose up
```

Starting the containers in detach mode.
```
docker-compose up -d
```

To view containers logs, we can also specify service here.
```
docker-compose logs -f
```

To stop and remove the containers.
```
docker-compose down
```

To stop|start|restart containers, we can also specify service here. NOTE: restart will not update the container's image.
```
docker-compose stop|start|restart
```

To attach to container shell.
```
docker-compose exec web sh
```

To run commands directly inside the container.
```
docker-compose exec web python3 manage.py createsuperuser
```

For custom compose file
```
docker-compose -f docker-compose-custom.yml {COMMANDS}
```

For more, docker-compose -h or [https://docs.docker.com/compose/reference/](https://docs.docker.com/compose/reference/)

Current `docker-compose.yml` is only meant for local development. Don't use it in production. Define a custom compose file production-compose.yml and use it with docker-compose -f production-compose.yml in production.