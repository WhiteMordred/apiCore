from functools import wraps
from flask import request, abort, current_app
import jwt

def protected_route(algorithms=None):
    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if 'Authorization' not in request.headers:
                abort(401, description="Authorization header is missing.")
            
            token = request.headers.get('Authorization').split()[1]
            try:
                jwt.decode(token, current_app.secret_key, algorithms=[algorithms])
            except jwt.ExpiredSignatureError:
                abort(401, description="Token has expired.")
            except jwt.DecodeError:
                abort(401, description="Invalid token.")

            return function(*args, **kwargs)

        return decorated_function

    return decorator