
# Docker-compose

To build the Docker containers and run the project, use Docker Compose. There are separate configurations for production and development.


## Development Server

Run the following commands to start Docker Compose in a development environment:

```
$ docker-compose -f docker-compose.yml up -d --build
$ docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
```


## Production Server

Run the following commands to start Docker Compose in a production environment:

```
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```

__NOTE: In some setups, collecting static files might be necessary. However, this project uses a separate front end (see tweeti\_front\_end).__


```
$ docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```

To create a superuser during the initial setup (you will be prompted for a username, email, and password), run:

```
$ docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```


### View logfiles

To view the log files of the Docker containers running Tweeti, use the following command:

```
$ docker-compose -f docker-compose.prod.yml logs -f
```





\newpage{}
