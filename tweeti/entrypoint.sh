#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# recreated database every time
# comment out these lines to prevent database flush
# use the following commands when lines are commented out to flush db:
#   $ docker-compose exec web python manage.py flush --no-input
#   $ docker-compose exec web python manage.py migrate
python manage.py flush --no-input
python manage.py migrate

exec "$@"

