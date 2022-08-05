import uuid
from datetime import datetime
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db import models
from django.db.models.manager import EmptyManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import CharField, ForeignKey, DateTimeField
from django.utils.timezone import now

from base.models import TimeStampedModel
from finalproject.settings import APP_SETTINGS


class User(AbstractUser):
    class Usertype(models.TextChoices):
        ADMIN = "ADMIN"
        USER = "USER"
        DOCTOR = "DOCTOR"

    class Gender(models.TextChoices):
        MAN = "MAN"
        WOMAN = "WOMAN"
        OTHER = "OTHER"

    REQUIRED_FIELDS = []
    email_verified = models.BooleanField(db_column='emailVerified', default=False)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user_type = models.CharField(choices=Usertype.choices, blank=True, default='', max_length=100)
    gender = models.CharField(choices=Gender.choices, default='', max_length=100)
    number = models.CharField(max_length=30)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    specialisation = models.CharField(max_length=120, default='', blank=True)

    presentation = models.TextField(blank=True)
    pic_url = models.CharField(max_length=1000, blank=True)

    def __str__(self) -> str:
        return self.username


class Treatment(models.Model):
    treatment_name = models.CharField(max_length=100, unique=True)
    pic_url = models.CharField(max_length=1000)
    treatment_description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    doctor = models.ForeignKey(User, related_name='treatment', on_delete=models.CASCADE, default='', to_field='username')

    # rating = models.IntegerField(default=0)

    def __str__(self) -> CharField:
        return self.treatment_name


class Dates(models.Model):
    date = models.DateTimeField(unique=True, default="")

    def __str__(self) -> str:
        return str(self.date)


class Reservation(models.Model):
    class ReservationStatus(models.IntegerChoices):
        CREATED = 1
        ACCEPTED = 2
        REFUSED = 3
        DONE = 4

    user = models.ForeignKey(User, related_name="reservations", on_delete=models.CASCADE, to_field='username')
    treatment = models.ForeignKey(Treatment, related_name="reservations", on_delete=models.CASCADE, default='', to_field='treatment_name')
    medical_note = models.TextField(blank=True, null=True, default=' ')
    reservation_status = models.IntegerField(choices=ReservationStatus.choices, default=ReservationStatus.CREATED)
    doctor = models.ForeignKey(User, related_name='resdoctor', on_delete=models.CASCADE, to_field='username')
    date = models.ForeignKey(Dates, related_name='resdate', on_delete=models.CASCADE, to_field='date', default="")

    class Meta:
        unique_together = ('doctor', 'date',)

    def __str__(self) -> User.username:
        return str(self.user)


class TokenRequest(TimeStampedModel):
    user_id = models.UUIDField(db_column='userId', default=None, null=True, blank=True)
    email = models.CharField(max_length=254, default=None, null=True, blank=True)
    mtoken = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class MTokenRequest(TimeStampedModel):
    email = models.CharField(max_length=254)

    def __str__(self):
        return self.email


class IneligibleDomain(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TrainingSpace(TimeStampedModel):
    """An active training space means, that one of the users in the training space paid for it,
    therefore that user (claimer) claimed the training space and can act as the admin of it.
    """

    id = models.CharField(primary_key=True, max_length=255, editable=False)
    name = models.CharField(max_length=255)
    free_limit = models.IntegerField(db_column='freeLimit', default=APP_SETTINGS['FREE_LIMIT'])
    creator = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='created_training_space')
    claimer = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='claimed_training_space'
    )

    def __str__(self):
        return self.name
