web: gunicorn digital_business_card.wsgi --log-file -
#or works good with external database
web: python manage.py migrate && gunicorn digital_business_card.wsgi