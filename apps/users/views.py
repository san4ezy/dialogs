from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.mixins import SerializersMixin
from . import serializers
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import CustomTokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    JWT authorization!!!
    """
    serializer_class = CustomTokenObtainPairSerializer


class AuthViewSet(SerializersMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializers = {
        'default': serializers.UserSerializer,
        'signup': serializers.SignupUserSerializer,
    }

    @action(methods=['post'], detail=False, permission_classes=(AllowAny,))
    def signup(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data.get('password'))
        data = self.get_serializer(user, serializer_name='default').data
        data.update({
            'token': user.get_tokens(),
        })
        return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['get', 'post'], detail=False, permission_classes=(IsAuthenticated,))
    def signout(self, request, *args, **kwargs):
        Token.objects.get(user=request.user).delete()
        return Response()


class UsersViewSet(SerializersMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """User viewset"""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializers = {
        "default": serializers.UserSerializer,
        "me": serializers.UserSerializer,
    }
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.request.user.pk)

    @action(methods=('get',), detail=False)
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)
