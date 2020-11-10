from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "test",
        "USER": "postgres",
        "PASSWORD": "test",
        "HOST": "db",
        "PORT": 5432,
    }
}
