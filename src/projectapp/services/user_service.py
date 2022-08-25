from typing import Optional
from io import BytesIO
from urllib import parse
from django.core.handlers.wsgi import WSGIRequest
from drfpasswordless.views import ObtainEmailCallbackToken

from base.exceptions import DomainIsNotEligibleException
from projectapp.models import User, IneligibleDomain
from projectapp.repository import UserRepository


class UserService:

    @staticmethod
    def create_by_email_with_request_params(email: str, rtype: str, base_url: str, *args, **kwargs) -> User:
        """
        Type: 'r' - register or
              'l' - login
        """

        # Create user using the drfpasswordless app
        environ_input = f'email={parse.quote(email)}'

        wsgi_request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': '/auth/email/',
            'CONTENT_TYPE': 'application/x-www-form-urlencoded',
            'ACCEPT': 'application/json',
            'CONTENT_LENGTH': len(environ_input),
            'wsgi.input': BytesIO(environ_input.encode('utf-8')),
        })

        view = ObtainEmailCallbackToken.as_view(message_payload={'type': rtype, 'base_url': base_url})
        view(wsgi_request, *args, **kwargs)


        return UserService.get_by_email(email)

    @staticmethod
    def get_by_email(email: str, raise_exception=False) -> Optional[User]:
        try:
            user = UserRepository.get_by_email(email)
        except User.DoesNotExist as exc:
            if raise_exception:
                raise exc
            else:
                user = None
        return user

    @staticmethod
    def get_by_id(user_id: str) -> Optional[User]:
        try:
            user = UserRepository.select_by_id(user_id)
        except User.DoesNotExist:
            user = None
        return user


class IneligibleDomainService:

    @staticmethod
    def test_domain_by_name(name: str) -> None:
        try:
            IneligibleDomain.objects.get(name=name)
            raise DomainIsNotEligibleException()
        except IneligibleDomain.DoesNotExist:
            # Do nothing, the domain is eligible
            pass
