import os

from environment.env import APP_ENV


def get_env_var(var_name: str) -> str:
    value = os.environ.get(var_name)
    if value is None:
        if APP_ENV.lower() == 'html':
            # it means the container will have only one application
            return ''

        value = os.environ.get(APP_ENV + '_' + var_name)
        if value is None:
            value = ''
    return value
