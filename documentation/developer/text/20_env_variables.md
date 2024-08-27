
# Environment Variables

There are two files containing environment variables: `.env.dev` for development and `.env.prod` for production. In a production environment, it's recommended to run additional Docker containers, such as one for a database (Postgres in this case). The database container for production has its own set of environment variables, which are included in the `.env.prod.db` file.


## .env.dev

```
DEBUG=1                                            # Show debug information
SECRET_KEY=foo                                     # Dummy value for secret key, used for encrypting passwords
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]     # Allowed hosts set to local hosts
DJANGO_SUPERUSER_PASSWORD=Welcome123               # Set a superuser password to automatically create a superuser (see `tweeti/entrypoint.sh`)
```

__Optional: Set production environment variables for testing (e.g. postgres database)__

```
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=postgres_db
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

__Optional: Set production environment variables for testing (e.g. sendinblue email backend)__

```
EMAIL_BACKEND=anymail.backends.sendinblue.EmailBackend
DEFAULT_FROM_EMAIL=info@example.com
EMAIL_API_URL=https://api.sendinblue.com/v3/
EMAIL_API_KEY='VeRySeCrEtKeY'
```

## .env.prod


This file contains the same variables as `.env.dev`, with values tailored to the production environment.

```
DEBUG=0                                                               # Do not show debug information
SECRET_KEY=<long string of random characters>                         # Use a strong secret key, e.g., '$k=^hblb*o5^gbvu2!n58zx(&-_=1tnu3)p)#-txrf&49p3-pv'
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1] <additional hosts>     # Include the hostname of the production server (e.g., example.com)
SQL_ENGINE=django.db.backends.postgresql                              # Using PostgreSQL; see https://docs.djangoproject.com/en/3.1/ref/databases/ for more information
SQL_DATABASE=<DATABASE-NAME>                                          # Database name, should match the one in `.env.prod.db`
SQL_USER=<DATABASE-USER>                                              # Database username, should match the one in `.env.prod.db`
SQL_PASSWORD=<DATABASE-PASSWORD>                                      # Database password, should match the one in `.env.prod.db`
SQL_HOST=db                                                           # Default database host
SQL_PORT=5432                                                         # Default database port
DATABASE=postgres                                                     # Database type, should align with the SQL_ENGINE variable
EMAIL_BACKEND=<email backend>                                         # See https://pypi.org/project/django-anymail/ for supported backends
DEFAULT_FROM_EMAIL=<from address>                                     # This address will appear as the sender when users receive emails from Tweeti
EMAIL_API_URL=<API URL>                                               # API URL from your email provider
EMAIL_API_KEY=<API key>                                               # API key from your email provider
```

## .env.prod.db

```
POSTGRES_USER=<DATABASE-USER>
POSTGRES_PASSWORD=<DATABASE-PASSWORD>
POSTGRES_DB=<DATABASE-NAME>
```



\newpage{}
