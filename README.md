# Tweeti\_Labeling

Tweeti is a web-based tool designed to facilitate the labeling of short messages, such as posts (formerly known as tweets). It includes features like shortcuts to speed up the labeling process and can be used on multiple devices, including laptops, phones, and tablets.

There is a Code Ocean capsule created for this project, to see the development code in action, see https://codeocean.com/capsule/8199255/tree/v1.

# Tags
- labeling
- data labeling
- Twitter


# Add Environment Variables

There are two files containing environment variables: `.env.dev` for development and `.env.prod` for production. In a production environment, it's recommended to run additional Docker containers, such as one for a database (Postgres in this case). The database container for production has its own set of environment variables, which are included in the `.env.prod.db` file.


## .env.dev

DEBUG=1                                              \# Show debug information
SECRET\_KEY=foo                                      \# Dummy value for secret key, used for encrypting passwords
DJANGO\_ALLOWED\_HOSTS=localhost 127.0.0.1 [::1]     \# Allowed hosts set to local hosts
DJANGO\_SUPERUSER\_PASSWORD=Welcome123               \# Set a superuser password to automatically create a superuser (see `tweeti/entrypoint.sh`)

__Optional: Set production environment variables for testing (some examples included)__

SQL\_ENGINE=django.db.backends.postgresql
SQL\_DATABASE=postgres\_db
SQL\_USER=hello\_django
SQL\_PASSWORD=hello\_django
SQL\_HOST=db
SQL\_PORT=5432
DATABASE=postgres

EMAIL\_BACKEND=anymail.backends.sendinblue.EmailBackend
DEFAULT\_FROM\_EMAIL=info@example.com
EMAIL\_API\_URL=https://api.sendinblue.com/v3/
EMAIL\_API\_KEY='VeRySeCrEtKeY'


## .env.prod


This file contains the same variables as `.env.dev`, with values tailored to the production environment.


DEBUG=0                                                                   \# Do not show debug information
SECRET\_KEY=\<long string of random characters\\>                         \# Use a strong secret key, e.g., '$k=^hblb\*o5^gbvu2!n58zx(&-\\_=1tnu3)p)\#-txrf&49p3-pv'
DJANGO\_ALLOWED\_HOSTS=localhost 127.0.0.1 [::1] \<additional hosts\>     \# Include the hostname of the production server (e.g., example.com)
SQL\_ENGINE=django.db.backends.postgresql                                 \# Using PostgreSQL; see https://docs.djangoproject.com/en/3.1/ref/databases/ for more information
SQL\_DATABASE=\<DATABASE-NAME\>                                           \# Database name, should match the one in `.env.prod.db`
SQL\_USER=\<DATABASE-USER\>                                               \# Database username, should match the one in `.env.prod.db`
SQL\_PASSWORD=\<DATABASE-PASSWORD\>                                       \# Database password, should match the one in `.env.prod.db`
SQL\_HOST=db                                                              \# Default database host
SQL\_PORT=5432                                                            \# Default database port
DATABASE=postgres                                                         \# Database type, should align with the SQL\_ENGINE variable
EMAIL\_BACKEND=\<email backend\>                                          \# See https://pypi.org/project/django-anymail/ for supported backends
DEFAULT\_FROM\_EMAIL=\<from address\>                                     \# This address will appear as the sender when users receive emails from Tweeti
EMAIL\_API\_URL=\<API URL\>                                               \# API URL from your email provider
EMAIL\_API\_KEY=\<API key\>                                               \# API key from your email provider


## .env.prod.db

POSTGRES\_USER=<DATABASE-USER>
POSTGRES\_PASSWORD=<DATABASE-PASSWORD>
POSTGRES\_DB=<DATABASE-NAME>


# Run via docker-compose

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


# Citation

When using this work for a publication, you can use the following bib-tex for citation:

```
@misc{muter2024tweeti,
  title = {Tweeti: X Post Annotation Tool, Optimised for Speed and Accuracy},
  author = {L.H.F. M{\"u}ter},
  journal = {SoftwareX},
  doi = {10.24433/CO.8056110.v1},
  howpublished = {\url{https://www.codeocean.com/}},
  year = 2024,
  month = {7},
  version = {v1}
}
```
