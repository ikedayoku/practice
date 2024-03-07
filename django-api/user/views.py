from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import  User
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, authentication 
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import viewsets

from .auth import NormalAuthentication
from user.serializers import UserSerializer, AuthTokenSerializer, LoginSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user, restrict who can see Todo"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, )

class Login(APIView):
    serializer_class = LoginSerializer
    authentication_classes = [NormalAuthentication,]
    def post(self, request, *args, **kwargs):
        return Response({"token": request.user})