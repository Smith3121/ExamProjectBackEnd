import uuid
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, ForeignKey, DateTimeField
from django.utils.timezone import now


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
    # username = models.CharField(max_length=50)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user_type = models.IntegerField(choices=Usertype.choices, blank=True, default=2)
    gender = models.IntegerField(choices=Gender.choices, default=1)
    number = models.CharField(max_length=30)
    date_of_birth = models.DateTimeField(null=True)
    specialisation = models.CharField(max_length=120, default='')

    presentation = models.TextField(blank=True)
    pic_url = models.CharField(max_length=1000)

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
