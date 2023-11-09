from rest_framework import generics
from rest_framework import generics, permissions

from user_management.models import MyUser
from .serializers import UserSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):  # new
    permission_classes = (permissions.IsAuthenticated,)
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
