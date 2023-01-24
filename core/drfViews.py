from django.contrib.auth.models import User, Group

from rest_framework import permissions, generics, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .permissions import *


class UserList(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class FreelancerList(generics.ListAPIView):
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nickname']
    filterset_fields = ['work_type', 'work_category', 'lessons', 'languages']


class ClientList(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]


class FreelancerDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]


class OrdersList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.GroupPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, client=self.request.user.client, in_auction=True)


class AcceptedOrdersList(viewsets.ReadOnlyModelViewSet):
    queryset = AcceptedOrder.objects.all()
    serializer_class = AcceptedOrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class WorkTypesList(viewsets.ReadOnlyModelViewSet):
    queryset = Work_Type.objects.all()
    serializer_class = WorkTypeSerializer


class WorkCategoriesList(viewsets.ReadOnlyModelViewSet):
    queryset = Work_Category.objects.all()
    serializer_class = WorkCategorySerializer


class LanguagesList(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class FeedbacksList(viewsets.ReadOnlyModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer