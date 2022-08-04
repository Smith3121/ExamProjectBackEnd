from rest_framework import serializers
from rest_framework import serializers
from rest_framework.serializers import EmailField
from rest_framework.validators import UniqueValidator

# from base.error_messages import ErrorMessage
# from base.exceptions import EmailAlreadyExists, FormInvalid
# from projectapp.models import User, TokenRequest
# from projectapp.services.user_service import UserService
from projectapp.models import User, Treatment \
    , Reservation, Dates


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dates
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id', 'treatment']


class UserSerializer(serializers.ModelSerializer):
    reservations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    treatment = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
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
                  'presentation', 'pic_url', 'reservations', 'treatment', 'specialisation']
        # fields = '__all__'


class TreatmentSerializer(serializers.ModelSerializer):
    # reservations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # doctor = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Treatment
        fields = ('treatment_name', 'pic_url', 'treatment_description', 'comment', 'doctor', 'id')


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        # depth = 1

# class ReservationDepthSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reservation
#         fields = '__all__'
#         depth = 1
