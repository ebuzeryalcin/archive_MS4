from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Since countryfield is here
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    Profile model for maintaining user default
    delivery information and order history
    """
    # user below telling each user can only have one profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Fields is set to be optional, null true and blank true
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country *', null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)

    # Returning username
    def __str__(self):
        return self.user.username

# To create a profile for user when new order is created
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # To save an object bag if user exists
    instance.userprofile.save()