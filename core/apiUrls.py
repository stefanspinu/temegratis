from django.urls import path, include

from rest_framework import routers

from . import drfViews


router = routers.DefaultRouter()
router.register(r'users', drfViews.UserList)
router.register(r'groups', drfViews.GroupViewSet)
# router.register(r'orders', drfViews.OrdersList)
router.register(r'accepted-orders', drfViews.AcceptedOrdersList)
router.register(r'work-types', drfViews.WorkTypesList)
router.register(r'work-categories', drfViews.WorkCategoriesList)
router.register(r'languages', drfViews.LanguagesList)
router.register(r'feedbacks', drfViews.FeedbacksList)

# api-auth needs to be called api-auth/login/ for example or else it won't work because of the viewsets from above.

urlpatterns = [
    path('', include(router.urls)),
    path('clients/', drfViews.ClientList.as_view(), name='clients'),
    path('clients/<str:pk>', drfViews.ClientDetails.as_view(), name='client-details'),
    path('freelancers/', drfViews.FreelancerList.as_view(), name='freelancers'),
    path('freelancers/<str:pk>', drfViews.FreelancerDetails.as_view(), name='freelancer-details'),
    path('orders/', drfViews.OrdersList.as_view(), name='orders'),
]


