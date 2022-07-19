# from typing import Optional
# from io import BytesIO
# from urllib import parse
# from django.core.handlers.wsgi import WSGIRequest
# from rest_framework.authtoken.models import Token
# from drfpasswordless.views import ObtainAuthTokenFromCallbackToken
# from drfpasswordless.models import CallbackToken
# from base.exceptions import TokenException
# from base.error_messages import ErrorMessage
# from projectapp.models import User
# from projectapp.repository import TokenRepository, UserRepository, MTokenRepository
#
#
# class TokenService:
#
#     @staticmethod
#     def create_by_email_and_mtoken_with_request_params(email: str, mtoken: str, *args, **kwargs) -> Token:
#         # Create token using the drfpasswordless app
#         environ_input = f'email={parse.quote(email)}&token={mtoken}'
#         wsgi_request = WSGIRequest({
#             'REQUEST_METHOD': 'POST',
#             'PATH_INFO': '/auth/token/',
#             'CONTENT_TYPE': 'application/x-www-form-urlencoded',
#             'ACCEPT': 'application/json',
#             'CONTENT_LENGTH': len(environ_input),
#             'wsgi.input': BytesIO(environ_input.encode('utf-8')),
#         })
#
#         view = ObtainAuthTokenFromCallbackToken.as_view()
#         result = view(wsgi_request, *args, **kwargs)
#
#         # Get token object based on the result from the drfpasswordless app
#         token = result.data.get('token', None)
#         if token is None:
#             error = ErrorMessage.token_error()
#             error['message'] = result.data.get('message', '')
#             raise TokenException(error)
#
#         return TokenRepository.select_by_token(result.data['token'])
#
#     @staticmethod
#     def get_by_email(email: str) -> Optional[User]:
#         try:
#             user = UserRepository.get_by_email(email)
#         except User.DoesNotExist:
#             user = None
#         return user
#
#
# class MTokenService:
#
#     @staticmethod
#     def get_active_by_key(key: str) -> CallbackToken:
#         return MTokenRepository.select_active_by_key(key)
#
#     @staticmethod
#     def deactivate_by_key(key: str):
#         token = MTokenService.get_active_by_key(key)
#         token.is_active = False
#         token.save()
