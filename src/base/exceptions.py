from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.views import exception_handler


class EmailAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT


class TokenException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class FormInvalid(ValidationError):
    pass


class DomainIsNotEligibleAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class UserDoesNotExistAPIException(APIException):
    status_code = status.HTTP_404_NOT_FOUND


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Update the structure of the response data.
    if response is not None:
        if type(exc) == ValidationError:
            customized_response = {'message': exc.detail[list(exc.detail)[0]][0].title()}
            response.data = customized_response

    return response


class DomainIsNotEligibleException(Exception):
    pass
