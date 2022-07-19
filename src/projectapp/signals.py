from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=settings.AUTH_USER_MODEL,  dispatch_uid="user_pre_save_signal_id")
def create_auth_token(sender, instance=None, **kwargs):
    if len(instance.email) > 0:
        instance.username = instance.username
