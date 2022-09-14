#!/bin/sh
echo "*****Make migrations*****"
echo "*****"
python manage.py makemigrations
echo "*****"
echo "*****Done*****"
echo "*****"
echo "*****Migrating tables*****"
echo "*****"
python manage.py migrate
echo "*****"
echo "*****Done*****"
echo "*****"
echo "*****"
echo "*****Collecting static*****"
echo "*****"
python manage.py collectstatic
echo "*****"
echo "*****Done******"
echo "*****"
echo "*****Configuring database*****"
echo "*****"
python manage.py runscript db_config
echo "*****"
echo "*****Done*****"
echo "*****"

exec "$@"