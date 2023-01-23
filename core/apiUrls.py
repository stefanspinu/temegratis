from django.urls import path, include

from rest_framework import routers

from . import drfViews


router = routers.DefaultRouter()
router.register(r'users', drfViews.UserList)
router.register(r'groups', drfViews.GroupViewSet)
router.register(r'orders', drfViews.OrdersList)
router.register(r'accepted-orders', drfViews.AcceptedOrdersList)
router.register(r'work-types', drfViews.WorkTypesList)
router.register(r'work-categories', drfViews.WorkCategoriesList)
router.register(r'languages', drfViews.LanguagesList)
router.register(r'feedbacks', drfViews.FeedbacksList)

urlpatterns = [
    path('', include(router.urls)),
    path('clients/<str:pk>', drfViews.ClientDetails.as_view(), name='client-details'),
    path('freelancers/<str:pk>', drfViews.FreelancerDetails.as_view(), name='freelancer-details'),
]


