from django.db.models import Avg
from django.forms import IntegerField
from rest_framework import serializers
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import EmailField
from rest_framework.validators import UniqueValidator

# from base.error_messages import ErrorMessage
# from base.exceptions import EmailAlreadyExists, FormInvalid
# from projectapp.models import User, TokenRequest
# from projectapp.services.user_service import UserService
from base.error_messages import ErrorMessage
from base.exceptions import FormInvalid, EmailAlreadyExists
from projectapp.models import User, Treatment \
    , Reservation, TokenRequest, IneligibleDomain, Rating
from projectapp.services.user_service import UserService


class RatingSerializer(serializers.ModelSerializer):
    # average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = '__all__'

    # def get_average_rating(self, instance):
    #     return instance.rating.aggregate(average_rating=Avg('rating'))['average_rating']


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
        fields = ['id', 'username']
        extra_kwargs = {
            'username': {'validators': []},
        }

    # def doctors(self):
    #     return User.objects.filter(usertype=3)


class TreatmentSerializer(serializers.ModelSerializer):
    # number = IntegerField(source='', required=False, allow_null=True)
    # rating_count = serializers.SerializerMethodField()
    # average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Treatment
        fields = ('treatment_name', 'pic_url', 'treatment_description', 'id', "doctor")

    # def get_rating_count(self, instance):
    #     return instance.treatment.rating_set.count()

    # def get_average_rating(self, instance):
    #     return instance.rating.treatment.aggregate(average_rating=Avg('rating'))['average_rating']

    def to_representation(self, value):
        data = super().to_representation(value)
        doctor_data = DoctorSerializer(value.doctor)
        data['doctor'] = doctor_data.data
        return data

    # def avg_rating(self):
    #     return Treatment.objects.annotate(avg_rating=Avg('rating_set__rating'))

    # def to_representation(self, value):
    #     data = super().to_representation(value)
    #     doctor_data = DoctorSerializer(value.doctor)
    #     data['doctor'] = doctor_data.data
    #     return data

    # def create(self, validated_data):
    #     doctor = validated_data.pop('doctor')
    #     doctor = User.objects.get(**doctor)
    #     # treatment = validated_data.pop('treatment')
    #     # treatment = Treatment.objects.get(**treatment)
    #     # user = validated_data.pop('user')
    #     # user = User.objects.get(**user)
    #
    #     return Treatment.objects.create(doctor=doctor, **validated_data)

    # def create(self, validated_data):
    #     print(validated_data)
    #     user_data = User.objects.get(id=validated_data.pop('user'))
    #     treatment_data = Treatment.objects.get(id=validated_data.pop('treatment'))
    #     doctor_data = User.objects.get(id=validated_data.pop('doctor'))
    #     instance = Reservation.objects.create(**validated_data)
    #     instance.user=user_data
    #     instance.treatment = treatment_data
    #     instance.doctor = doctor_data
    #     return instance

    # def create(self, validated_data):
    #     return Reservation.objects.create(
    #         **validated_data,
    #         user_id=validated_data.pop('user'),
    #         treatment_id=validated_data.pop('treatment'),
    #         doctor_id=validated_data.pop('doctor')
    #     )


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
