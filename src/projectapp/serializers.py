import django_filters
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import EmailField, CharField
from rest_framework.validators import UniqueValidator

# from base.error_messages import ErrorMessage
# from base.exceptions import EmailAlreadyExists, FormInvalid
# from projectapp.models import User, TokenRequest
# from projectapp.services.user_service import UserService
from projectapp.models import User, Treatment \
    , Reservation


class DoctorSerializer(serializers.ModelSerializer):
    # reservations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # doctor_choice_reservation = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'id']


class UserSerializer(serializers.ModelSerializer):
    reservations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    email = EmailField(
        allow_blank=False,
        label='Email address',
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'email_verified', 'user_type', 'gender', 'date_of_birth', 'number', 'username',
                  'presentation', 'pic_url', 'reservations', 'doctor']
        # fields = '__all__'


class TreatmentSerializer(serializers.ModelSerializer):
    reservations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Treatment
        fields = ('treatment_name', 'pic_url', 'treatment_description', 'comment', 'id', 'reservations')


class ReservationSerializer(serializers.ModelSerializer):
    # doctor = serializers.CharField(source=User.Usertype == 3)
    # User.doctor = User.objects.filter(user_type=3)

    class Meta:
        model = Reservation
        fields = '__all__'
        # depth = 1

# class ReservationDepthSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reservation
#         fields = '__all__'
#         depth = 1

