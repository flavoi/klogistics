import dj_database_url

from .base import *

DEBUG = True

SECRET_KEY = get_env_variable('SECRET_KEY')

# Heroku database configuration
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS = [
    '.klogistics.herokuapp.com',
    'localhost',
]