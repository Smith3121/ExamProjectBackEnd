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
    , Reservation, TokenRequest, IneligibleDomain
from projectapp.services.user_service import UserService


class UserSerializer(serializers.ModelSerializer):
    # reservations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # treatment = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # doctor = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
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
                  'presentation', 'pic_url', 'reservations', 'treatment', 'specialisation', "doctor"]

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


class TreatmentSerializerForRes(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ('id', 'treatment_name')


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class TreatmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = Treatment
        fields = ('treatment_name', 'pic_url', 'treatment_description', 'comment', 'id', "doctor")

    def create(self, validated_data):
        treatment_data = validated_data.pop('treatment')
        doctor = User.objects.create(**validated_data)
        for tre_data in treatment_data:
            Treatment.objects.create(doctor=doctor, **tre_data)

        return doctor


class ReservationSerializer(serializers.ModelSerializer):
    # doctor = DoctorSerializer()
    # user = UserSerializerForRes()
    # treatment = TreatmentSerializerForRes()

    class Meta:
        model = Reservation
        fields = '__all__'


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
