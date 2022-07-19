import enum


class ErrorMessage:

    @staticmethod
    def email_already_exists():
        return {
            'code': ErrorCodes.EMAIL_ALREADY_EXISTS.value,
            'message': ErrorMessages.EMAIL_ALREADY_EXISTS.value
        }

    @staticmethod
    def email_is_invalid():
        return {
            'code': ErrorCodes.EMAIL_IS_INVALID.value,
            'message': ErrorMessages.EMAIL_IS_INVALID.value
        }

    @staticmethod
    def token_error():
        return {
            'code': ErrorCodes.TOKEN_ERROR.value,
            'message': ''
        }

    @staticmethod
    def domain_is_not_eligible_api_exception():
        return {
            'code': int(ErrorCodes.DOMAIN_INELIGIBLE.value),
            'message': ErrorMessages.DOMAIN_IS_NOT_ELIGIBLE.value
        }

    @staticmethod
    def user_does_not_exist_api_exception():
        return {
            'code': int(ErrorCodes.USER_DOES_NOT_EXIST.value),
            'message': ErrorMessages.USER_DOES_NOT_EXIST_API_EXCEPTION.value
        }


class ErrorCodes(enum.Enum):
    EMAIL_ALREADY_EXISTS = 1
    EMAIL_IS_INVALID = 2
    TOKEN_ERROR = 3
    DOMAIN_INELIGIBLE = 4
    USER_DOES_NOT_EXIST = 5


class ErrorMessages(enum.Enum):
    EMAIL_ALREADY_EXISTS = 'This email is already taken.'
    EMAIL_IS_INVALID = 'Please enter a valid email address.'
    DOMAIN_IS_NOT_ELIGIBLE = 'Please use an email address with an eligible domain.'
    USER_DOES_NOT_EXIST_API_EXCEPTION = 'User does not exist with this email address.'
