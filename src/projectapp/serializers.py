from django.db.models import Avg
from django.forms import IntegerField
from rest_framework import serializers
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import EmailField
from rest_framework.validators import UniqueValidator
from django.db.models import Avg, Count

# from base.error_messages import ErrorMessage
# from base.exceptions import EmailAlreadyExists, FormInvalid
# from projectapp.models import User, TokenRequest
# from projectapp.services.user_service import UserService
from base.error_messages import ErrorMessage
from base.exceptions import FormInvalid, EmailAlreadyExists
from projectapp.models import User, Treatment \
    , Reservation, TokenRequest, IneligibleDomain, Rating, FAQ
from projectapp.services.user_service import UserService


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('comment', 'rating', 'treatment', 'user', 'id')


class TreatmentSerializerForRes(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ('id', 'treatment_name')
        extra_kwargs = {
            'treatment_name': {'validators': []},
        }


class UserSerializer(serializers.ModelSerializer):
    reservations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    treatment = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # treatment = serializers.PrimaryKeyRelatedField(queryset=Treatment.objects.all())
    # treatment = TreatmentSerializerForRes(many=True)
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
                  'presentation', 'pic_url', 'reservations', 'specialisation', "doctor", "treatment"]

    # def to_representation(self, value):
    #     data = super().to_representation(value)
    #     treatment_data = TreatmentSerializerForRes(value.treatment)
    #     data['treatment'] = treatment_data.data
    #     return data

    def is_valid(self, raise_exception=False):
        try:
            super(UserSerializer, self).is_valid(raise_exception)

        except ValidationError as e:
            email_error = e.detail.get('email')

            if email_error:
                if email_error[0].code == 'unique':
                    raise EmailAlreadyExists(ErrorMessage.email_already_exists())
                elif email_error[0].code == 'invalid':
                    raise FormInvalid(ErrorMessage.email_is_invalid())

            raise e


class UserSerializerForRes(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        extra_kwargs = {
            'username': {'validators': []},
        }


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'pic_url', 'specialisation', 'presentation']
        extra_kwargs = {
            'username': {'validators': []},
        }


class TreatmentSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SerializerMethodField(read_only=True)

    def get_comment(self, treatment):
        print("This is the prinnttttttt", Rating.objects.filter(treatment_id=treatment.pk))
        return Rating.objects.filter(treatment_id=treatment.pk).values('comment', 'id')

    def get_rating(self, treatment):
        return Treatment.objects.filter(id=treatment.pk).aggregate(Avg('rating__rating'))

    class Meta:
        model = Treatment
        fields = ('treatment_name', 'pic_url', 'treatment_description', 'id', "doctor", 'rating', 'comment')

    def to_representation(self, value):
        data = super().to_representation(value)
        doctor_data = DoctorSerializer(value.doctor)
        data['doctor'] = doctor_data.data
        return data


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('user', 'treatment', 'doctor', 'medical_note', 'problem_description', 'reservation_status', 'date',
                  'id')

    def to_representation(self, value):
        data = super().to_representation(value)
        doctor_data = DoctorSerializer(value.doctor)
        user_data = UserSerializerForRes(value.user)
        treatment_data = TreatmentSerializerForRes(value.treatment)
        data['user'] = user_data.data
        data['doctor'] = doctor_data.data
        data['treatment'] = treatment_data.data
        return data


class TokenRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenRequest
        fields = ['email', 'mtoken', 'userId']
        extra_kwargs = {
            'userId': {'source': 'user_id'},
        }

    def validate(self, attrs):
        result = super(TokenRequestSerializer, self).validate(attrs)
        if result.get('email', None) is None and result.get('user_id', None) is None:
            # TODO: raise the proper exception
            raise ValidationError('This Field Is Required.')
        return result

    def is_valid(self, raise_exception=False):
        super(TokenRequestSerializer, self).is_valid(raise_exception)


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField(source='token.key')
    user = UserSerializer(read_only=True)

    class Meta:
        fields = ['token', 'user']


class MTokenRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenRequest
        fields = ['email']

    def is_valid(self, raise_exception=False):
        try:
            serializer = super(MTokenRequestSerializer, self)
            serializer.is_valid(raise_exception)

            UserService.get_by_email(serializer.validated_data['email'], raise_exception=True)
        except ValidationError as e:
            email_error = e.detail.get('email')

            if email_error and email_error[0].code == 'invalid':
                raise FormInvalid(ErrorMessage.email_is_invalid())

            raise e


class MTokenResponseSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)

    class Meta:
        fields = ['user']


class IneligibleDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = IneligibleDomain
        fields = ['name']
