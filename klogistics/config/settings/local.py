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

ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost'
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# Amazon S3 support
# http://aws.amazon.com/

AWS_ACCESS_KEY_ID = get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_secret('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_secret('AWS_STORAGE_BUCKET_NAME')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_S3_PATH = 'media'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATIC_S3_PATH = 'static'

MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
MEDIA_URL = '//s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME
STATIC_ROOT = "/%s/" % STATIC_S3_PATH
STATIC_URL = '//s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = 'admin/'