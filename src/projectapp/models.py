import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg, Count
from django.utils.translation import gettext_lazy as _

from base.models import TimeStampedModel


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
        blank=True
    )
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user_type = models.IntegerField(choices=Usertype.choices, blank=True, null=True)
    gender = models.IntegerField(choices=Gender.choices, blank=True, null=True)
    number = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    specialisation = models.CharField(max_length=120, default='', blank=True, null=True)

    presentation = models.TextField(blank=True, null=True)
    pic_url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self) -> str:
        return self.username


class Treatment(models.Model):
    treatment_name = models.CharField(max_length=100, unique=True)
    pic_url = models.CharField(max_length=1000)
    treatment_description = models.TextField(blank=True)
    doctor = models.ForeignKey(User, related_name='treatment', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.treatment_name)


class Rating(models.Model):
    class RatingChoices(models.IntegerChoices):
        POOR = 1
        ABOVEPOOR = 1.5
        AVERAGE = 2
        ABOVEAVERAGE = 2.5
        GOOD = 3
        ABOVEGOOD = 3.5
        GREAT = 4
        ABOVEGREAT = 4.5
        EXCELLENT = 5

    comment = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=RatingChoices.choices, null=True, blank=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.rating)


class Reservation(models.Model):
    class ReservationStatus(models.IntegerChoices):
        CREATED = 1
        ACCEPTED = 2
        CANCELLEDBYDOCTOR = 3
        DONE = 4
        CANCELLEDBYUSER = 5

    user = models.ForeignKey(User, related_name="reservations", on_delete=models.CASCADE, blank=True, null=True)
    treatment = models.ForeignKey(Treatment, related_name="reservations", on_delete=models.CASCADE)
    medical_note = models.TextField(blank=True, null=True, default=' ')
    problem_description = models.TextField(blank=True, null=True, default="")
    reservation_status = models.IntegerField(choices=ReservationStatus.choices, default=ReservationStatus.CREATED)
    doctor = models.ForeignKey(User, related_name='doctor', on_delete=models.CASCADE)
    date = models.DateTimeField()

    class Meta:
        unique_together = ('doctor', 'date')

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
