web: gunicorn --pythonpath DenzelProject DenzelProject.wsgi
release: python DenzelProject/manage.py migrate
release: python DenzelProject/manage.py collectstatic
