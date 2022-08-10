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
    class Usertype(models.IntegerChoices):
        ADMIN = 1
        USER = 2
        DOCTOR = 3

    class Gender(models.IntegerChoices):
        MAN = 1
        WOMAN = 2
        OTHER = 3

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
    user_type = models.IntegerField(choices=Usertype.choices, blank=True)
    gender = models.IntegerField(choices=Gender.choices, blank=True)
    number = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    specialisation = models.CharField(max_length=120, default='', blank=True)

    presentation = models.TextField(blank=True)
    pic_url = models.CharField(max_length=1000, blank=True)

    # training_space = models.ForeignKey(
    #    " TrainingSpace",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='users'
    # )

    def __str__(self) -> str:
        return self.username


class Treatment(models.Model):
    treatment_name = models.CharField(max_length=100, unique=True)
    pic_url = models.CharField(max_length=1000)
    treatment_description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    doctor = models.ForeignKey(User, related_name='treatment', on_delete=models.CASCADE, default='',
                               to_field='username')

    # rating = models.IntegerField(default=0)

    def __str__(self) -> CharField:
        return self.treatment_name


# class Dates(models.Model):
#     date = models.DateTimeField(unique=True)
#
#     def __str__(self) -> str:
#         return str(self.date)


class Reservation(models.Model):
    class ReservationStatus(models.IntegerChoices):
        CREATED = 1
        ACCEPTED = 2
        REFUSED = 3
        DONE = 4

    user = models.ForeignKey(User, related_name="reservations", on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, related_name="reservations", on_delete=models.CASCADE, default='')
    medical_note = models.TextField(blank=True, null=True, default=' ')
    problem_description = models.TextField(blank=True, null=True, default=' ')
    reservation_status = models.IntegerField(choices=ReservationStatus.choices, default=ReservationStatus.CREATED)
    doctor = models.ForeignKey(User, related_name='doctor', on_delete=models.CASCADE)
    # date = models.ForeignKey(Dates, related_name='resdate', on_delete=models.CASCADE, default="")
    date = models.DateTimeField()

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

