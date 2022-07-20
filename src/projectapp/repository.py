# from drfpasswordless.models import CallbackToken
# from rest_framework.authtoken.models import Token
#
#
# from projectapp.models import User
#
#
# class UserRepository:
#
#     @staticmethod
#     def get_by_email(email: str) -> User:
#         return User.objects.get(email=email)
#
#     @staticmethod
#     def select_by_id(user_id: str) -> User:
#         return User.objects.get(pk=user_id)
#
#
# class TokenRepository:
#
#     @staticmethod
#     def select_by_token(token: str) -> Token:
#         return Token.objects.get(key=token)
#
#
# class MTokenRepository:
#
#     @staticmethod
#     def select_active_by_key(key: str) -> CallbackToken:
#         return CallbackToken.objects.get(key=key, is_active=True)
