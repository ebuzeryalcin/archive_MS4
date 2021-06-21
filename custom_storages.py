from django.conf import settings
# this is a class from installed django-storages
from storages.backends.s3boto3 import S3Boto3Storage

# Telling django that in production use s3 to store static
# files whenever collect static is runned and that
# uploaded book images to also go in here


# Custom class inherits from django-storages
class StaticStorage(S3Boto3Storage):
    # From settings location
    location = settings.STATICFILES_LOCATION


# Custom class inherits from django-storages
class MediaStorage(S3Boto3Storage):
    # From settings location
    location = settings.MEDIAFILES_LOCATION