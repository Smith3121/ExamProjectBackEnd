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
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
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
    treatment_name = models.CharField(max_length=100)
    pic_url = models.CharField(max_length=1000)
    treatment_description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    doctor = models.ForeignKey(User, related_name='doctor', on_delete=models.CASCADE, default='')

    # rating = models.IntegerField(default=0)

    def __str__(self) -> CharField:
        return self.treatment_name


class Hour(models.Model):
    hour = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return str(self.hour)


class Date(models.Model):
    date = models.CharField(max_length=1000)

    # hour = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return str(self.date)


class Reservation(models.Model):
    class ReservationStatus(models.IntegerChoices):
        CREATED = 1
        ACCEPTED = 2
        REFUSED = 3
        DONE = 4

    user = models.ForeignKey(User, related_name="reservations", on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, related_name="reservations", on_delete=models.CASCADE, default='')
    medical_note = models.TextField(blank=True, null=True, default=' ')
    reservation_status = models.IntegerField(choices=ReservationStatus.choices, default=ReservationStatus.CREATED)
    doctor = models.ForeignKey(User, related_name='resdoctor', on_delete=models.CASCADE)
    date = models.ForeignKey(Date, related_name='resdate', on_delete=models.CASCADE)
    hour = models.ForeignKey(Hour, related_name='hours', on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ('doctor', 'date', 'hour')

    def __str__(self) -> User.username:
        return str(self.user)
