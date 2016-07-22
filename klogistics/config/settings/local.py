from .base import *

# JSON-based secrets module
with open("secrets.json") as f:
    secrets = json.loads(f.read())

def get_secret(settings, secrets=secrets):
    """ Get the secret variable or return explicit exception."""
    try:
        return secrets[settings]
    except KeyError:
        error_msg = "Set the {0} enviroment variable".format(settings)
        raise ImproperlyConfigured(error_msg)

DEBUG = True

SECRET_KEY = get_secret("SECRET_KEY")

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    "default" : {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_secret("DBNAME"),
        "USER": get_secret("DBUSER"),
        "PASSWORD": get_secret("DBPASSWORD"),
        "HOST": "localhost",
        "PORT": "",
    }
}