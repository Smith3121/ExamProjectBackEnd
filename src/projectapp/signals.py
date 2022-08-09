from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from finalproject.settings import AUTH_USER_MODEL
from projectapp.models import User


@receiver(pre_save, sender=AUTH_USER_MODEL, dispatch_uid="user_pre_save_signal_id")
def create_auth_token(sender, instance=None, **kwargs):
    print("This email printed", instance.email)
    print("This is the sender", sender)
    # print("This is the sender name", sender.username)

    if len(instance.email) > 0:
        print("Instance email is longer than zero")
        instance.username = instance.email
