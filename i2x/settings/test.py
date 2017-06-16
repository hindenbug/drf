from i2x.settings.base import *

DEBUG = True

AUTH_USER_MODEL = 'api.User'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'i2x',
        'USER': 'manoj',
        'PASSWORD': 'manoj',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
