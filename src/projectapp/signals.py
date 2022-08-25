from django.db.models.signals import pre_save
from django.dispatch import receiver

from finalproject.settings import AUTH_USER_MODEL


@receiver(pre_save, sender=AUTH_USER_MODEL, dispatch_uid="user_pre_save_signal_id")
def create_auth_token(sender, instance=None, **kwargs):
    if len(instance.email) > 0:
        instance.username = instance.email
