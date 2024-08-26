# Tweeti\_Labeling
A tool for tweet labeling, based on TREC.


# add environment variables

## .env.dev
DEBUG=1
SECRET\_KEY=foo
DJANGO\_ALLOWED\_HOSTS=localhost 127.0.0.1 [::1]
SQL\_ENGINE=django.db.backends.postgresql
SQL\_DATABASE=<DATABASE-DEV-NAME>
SQL\_USER=hello\_django
SQL\_PASSWORD=hello\_django
SQL\_HOST=db
SQL\_PORT=5432
DATABASE=postgres
EMAIL\_BACKEND=anymail.backends.sendinblue.EmailBackend
DEFAULT\_FROM\_EMAIL=foo@bar.com
SENDINBLUE\_API\_URL=https://api.sendinblue.com/v3/"
SENDINBLUE\_API\_KEY=<API-KEY>

## .env.prod
Same variables as .env.dev where values represent producten environment.

## .env.prod.db
POSTGRES\_USER=<DATABASE-USER>
kPOSTGRES\_PASSWORD=<DATABASE-PASSWORD>
POSTGRES\_DB=<DATABASE-PROD-NAME>


# Run via docker-compose (on production server)
Using the followng bash command:

```
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```

NOTE
For a different setup, collect static might be required, however this project uses a seperated front end (see tweeti\_front\_end)

```
$ docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```

For initial setup one can create a super user (askes for username/email/password):

```
$ docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```


# View logfiles
Using the following bashcommand:

$ docker-compose -f docker-compose.prod.yml logs -f
