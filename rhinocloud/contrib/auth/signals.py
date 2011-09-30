from django.contrib.auth.models import User
from rhinocloud.utils import random_generator


def generate_username_from_email(sender, instance, **kwargs):
    if isinstance(instance, User):
        email = instance.email
        username = random_generator(email[:25])
        while sender.objects.filter(username=username).exists():
            username = random_generator(username[:25])
        instance.username = username
            
def username_shorten(sender, instance, **kwargs):
    if sender == User:
        if len(instance.username) > 30:
            instance.username = instance.username[:30]

def first_name_shorten(sender, instance, **kwargs):
    if sender == User:
        if len(instance.first_name) > 30:
            instance.first_name = instance.first_name[:30]
            
def last_name_shorten(sender, instance, **kwargs):
    if sender == User:
        if len(instance.username) > 30:
            instance.last_name = instance.last_name[:30]
