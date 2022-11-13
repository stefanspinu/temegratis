from django.contrib.auth.models import User, Group

from rest_framework import permissions, generics, filters, viewsets

from .models import *
from .serializers import UserSerializer, GroupSerializer
from .permissions import *


class UserList(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]