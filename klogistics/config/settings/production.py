import dj_database_url

from .base import *

def get_env_variable(var_name):
    """ Get the environment variable or return explicit exception. """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {0} enviroment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)

DEBUG = False

SECRET_KEY = get_env_variable('SECRET_KEY')

# Heroku database configuration
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS = [
    '.klogistics.herokuapp.com',
    'localhost',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# Amazon S3 support
# http://aws.amazon.com/

AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_STORAGE_BUCKET_NAME')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_S3_PATH = 'media'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATIC_S3_PATH = 'static'

MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
MEDIA_URL = '//s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME
STATIC_ROOT = "/%s/" % STATIC_S3_PATH
STATIC_URL = '//s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = 'admin/'