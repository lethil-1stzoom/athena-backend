from rest_framework.response import Response
from rest_framework import status

def is_exec(api_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_exec:
            return api_func(request, *args, **kwargs)
        else:
            return Response({"status": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper
