from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import EmailField
from rest_framework.validators import UniqueValidator

# from base.error_messages import ErrorMessage
# from base.exceptions import EmailAlreadyExists, FormInvalid
# from projectapp.models import User, TokenRequest
# from projectapp.services.user_service import UserService
from projectapp.models import User, Treatment


class UserSerializer(serializers.ModelSerializer):
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
                  'presentation', 'pic_url']


class TreatmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Treatment
        fields = ('treatment_name', 'pic_url', 'treatment_description', 'comment', 'rating', 'id')


#     def is_valid(self, raise_exception=False):
#         try:
#             super(UserSerializer, self).is_valid(raise_exception)
#
#         except ValidationError as e:
#             email_error = e.detail.get('email')
#
#             if email_error:
#                 if email_error[0].code == 'unique':
#                     raise EmailAlreadyExists(ErrorMessage.email_already_exists())
#                 elif email_error[0].code == 'invalid':
#                     raise FormInvalid(ErrorMessage.email_is_invalid())
#
#             raise e
#
#
# class TokenRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TokenRequest
#         fields = ['email', 'mtoken', 'userId']
#         extra_kwargs = {
#             'userId': {'source': 'user_id'},
#         }
#
#     def validate(self, attrs):
#         result = super(TokenRequestSerializer, self).validate(attrs)
#         if result.get('email', None) is None and result.get('user_id', None) is None:
#             # TODO: raise the proper exception
#             raise ValidationError('This Field Is Required.')
#         return result
#
#     def is_valid(self, raise_exception=False):
#         super(TokenRequestSerializer, self).is_valid(raise_exception)
#
#
# class TokenResponseSerializer(serializers.Serializer):
#     token = serializers.CharField(source='token.key')
#     user = UserSerializer(read_only=True)
#
#     class Meta:
#         fields = ['token', 'user']
#
#
# class MTokenRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TokenRequest
#         fields = ['email']
#
#     def is_valid(self, raise_exception=False):
#         try:
#             serializer = super(MTokenRequestSerializer, self)
#             serializer.is_valid(raise_exception)
#
#             UserService.get_by_email(serializer.validated_data['email'], raise_exception=True)
#         except ValidationError as e:
#             email_error = e.detail.get('email')
#
#             if email_error and email_error[0].code == 'invalid':
#                 raise FormInvalid(ErrorMessage.email_is_invalid())
#
#             raise e
#
#
# class MTokenResponseSerializer(serializers.Serializer):
#     user = UserSerializer(read_only=True)
#
#     class Meta:
#         fields = ['user']
