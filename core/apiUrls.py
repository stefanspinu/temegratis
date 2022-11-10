from django.urls import path, include

from rest_framework import routers

from . import drfViews


router = routers.DefaultRouter()
router.register(r'users', drfViews.UserViewSet)
router.register(r'groups', drfViews.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


