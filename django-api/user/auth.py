import time
import jwt
from todo_project.settings import SECRET_KEY
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from core.models import User

class NormalAuthentication(BaseAuthentication):
    def authenticate(self, request):
        email = request._request.POST.get("email")
        password = request._request.POST.get("password")
        user_obj = User.objects.filter(email=email).first()
        if not user_obj:
            raise exceptions.AuthenticationFailed('認証失敗')
        elif user_obj.password != password:
            raise exceptions.AuthenticationFailed('パスワードがあってません')
        token = generate_jwt(user_obj)
        return (token, None)

    def authenticate_header(self, request):
        pass

# ドキュメント: https://pyjwt.readthedocs.io/en/latest/usage.html?highlight=exp
def generate_jwt(user):
    timestamp = int(time.time()) + 60*60*24*7
    return jwt.encode(
        {"userid": user.pk, "email": user.email, "exp": timestamp},
        SECRET_KEY)