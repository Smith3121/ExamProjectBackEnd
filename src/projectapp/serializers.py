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
    , Reservation, Dates, TokenRequest, IneligibleDomain


from projectapp.services.user_service import UserService


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



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id']
#

# class TrainingSpaceSerializer(serializers.ModelSerializer):
#     creator = UserSerializer(read_only=True)
#
#     class Meta:
#         model = TrainingSpace
#         fields = ['id', 'name', 'creator']


class IneligibleDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = IneligibleDomain
        fields = ['name']
