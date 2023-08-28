from .models import User
from rest_framework import generics
from accounts.serializers import RegisterSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
