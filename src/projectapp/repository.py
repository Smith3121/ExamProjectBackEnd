from django.db.models import QuerySet
from drfpasswordless.models import CallbackToken
from rest_framework.authtoken.models import Token

from projectapp.models import User, Treatment


class UserRepository:

    @staticmethod
    def get_by_email(email: str) -> User:
        return User.objects.get(email=email)

    @staticmethod
    def select_by_id(user_id: str) -> User:
        return User.objects.get(pk=user_id)


class TokenRepository:

    @staticmethod
    def select_by_token(token: str) -> Token:
        return Token.objects.get(key=token)


class MTokenRepository:

    @staticmethod
    def select_active_by_key(key: str) -> CallbackToken:
        return CallbackToken.objects.get(key=key, is_active=True)


# @staticmethod
# def select_by_name(username: str) -> User:
#     return User.objects.get(name=username)
#
# @staticmethod
# def select_by_type(usertype: int) -> QuerySet[User]:
#     return User.objects.filter(user_type=usertype)
#
# @staticmethod
# def delete_by_name(username: str):
#     username = User.objects.get(name=username)
#     username.delete()
#

# class TreatmentRepository:
#
#     @staticmethod
#     def select_by_id(id: int) -> Treatment:
#         return Treatment.objects.get(id=id)
#

