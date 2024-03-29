from core.models import  User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics 
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer, LoginSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user, restrict who can see Todo"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UpdateUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user

class DeleteUserView(generics.DestroyAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user

# class Login(APIView):
#     serializer_class = LoginSerializer
#     authentication_classes = [NormalAuthentication,]
#     def post(self, request, *args, **kwargs):
#         return Response({"token": request.user})