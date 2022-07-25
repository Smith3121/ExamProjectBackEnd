import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, ForeignKey

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

    # username = models.CharField(max_length=50)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email_verified = models.BooleanField(db_column='emailVerified', default=False)
    user_type = models.IntegerField(choices=Usertype.choices, blank=True, default=2)
    gender = models.IntegerField(choices=Gender.choices, default=1)
    number = models.CharField(max_length=30)
    date_of_birth = models.DateTimeField(null=True)

    presentation = models.TextField(blank=True)
    pic_url = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.username


class Treatment(models.Model):
    treatment_name = models.CharField(max_length=100)
    pic_url = models.CharField(max_length=100)
    treatment_description = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    # rating = models.IntegerField(default=0)

    def __str__(self) -> CharField:
        return self.treatment_name


class Reservation(models.Model):
    class ReservationStatus(models.IntegerChoices):
        CREATED = 1
        ACCEPTED = 2
        REFUSED = 3
        DONE = 4
#
#     # chosen_hour = models.DateTimeField(null=True)
    user = models.ForeignKey(
        User, related_name="reservations", on_delete=models.CASCADE)
    treatment = models.ForeignKey(
        Treatment, related_name="reservations", on_delete=models.CASCADE)
#     # problem_description = models.TextField(blank=True, null=True, default=' ')

    reservation_status = models.IntegerField(choices=ReservationStatus.choices, default=ReservationStatus.CREATED)

    def __str__(self) -> User.username:
        return str(self.user)

# class TokenRequest(TimeStampedModel):
#     user_id = models.UUIDField(db_column='userId', default=None, null=True, blank=True)
#     email = models.CharField(max_length=254, default=None, null=True, blank=True)
#     mtoken = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.email
#
#
# class MTokenRequest(TimeStampedModel):
#     email = models.CharField(max_length=254)
#
#     def __str__(self):
#         return self.email
