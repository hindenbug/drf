from i2x.settings.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'i2x_dev',
        'USER': 'manoj',
        'PASSWORD': 'manoj',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
