### For Development

1. Run the following command to spawn your environment for the first time
  
```
docker-compose -f docker-compose.yml -p mis up -d --build
```

See if the docker containers running

```
docker ps
```

You'll see you containers like this

```
CONTAINER ID        IMAGE                     COMMAND                  CREATED              STATUS              PORTS                                                                NAMES
ea3b914c3193        mis_web                   "python manage.py ru…"   About a minute ago   Up 58 seconds       0.0.0.0:8082->8081/tcp                                               mis_web_1
57f30698ccda        postgres:12.0-alpine      "docker-entrypoint.s…"   About a minute ago   Up About a minute   5432/tcp   mis_db_1
```

Connect to your `mis_web` with

```
docker logs {{id}}
```

in this case

```
docker logs ea3b914c3193 -f
```

press `CTRL+C` to exit logs view

2. When you're done, you can do the following command

```
docker-compose -f docker-compose.yml -p mis stop
```

3. When you go back to code

```
docker-compose -f docker-compose.yml -p mis start
```

4. When you have to delete the environment

```
docker-compose -f docker-compose.yml -p mis down
```
