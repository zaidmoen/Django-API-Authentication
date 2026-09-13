from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def require_json(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if request.method in ("POST", "PUT", "PATCH") and not request.content_type.startswith("application/json"):
            return Response({"detail": "Content-Type must be application/json."}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        return view_func(request, *args, **kwargs)
    return wrapped

