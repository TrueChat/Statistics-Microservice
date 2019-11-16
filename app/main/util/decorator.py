from functools import wraps
from flask import request
from requests import get
from json import loads

from .. import BASE_URL


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        user_check = get(
            BASE_URL + '/rest-auth/user/',
            headers={'Authorization': request.headers.get('Authorization')}
        )

        response_object = loads(user_check.content)

        if user_check.status_code != 200:
            return response_object, user_check.status_code

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        user_check = get(
            BASE_URL + '/rest-auth/user/',
            headers={'Authorization': request.headers.get('Authorization')}
        )

        response_object = loads(user_check.content)

        if user_check.status_code != 200:
            return response_object, user_check.status_code
        
        if not response_object['is_superuser']:
            response_object = {
                "detail": "Current user is not a superuser"
            }
            return response_object, 403

        return f(*args, **kwargs)

    return decorated
