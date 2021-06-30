from django.urls import path, include
from rest_framework import routers

from foodlink_back.apps.authentication.views import AuthenticateViewSet, RegistrationAPIView, UserDetailsView, \
    UserUpdateProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register('auth', AuthenticateViewSet)

urlpatterns = []

app_name = 'authentication'
urlpatterns += router.urls
urlpatterns += [
    path('registration/', RegistrationAPIView.as_view(), name='user-registration'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<str:phone>/details/', UserDetailsView.as_view(), name='user-details'),
    path('user/<str:phone>/update/', UserUpdateProfileView.as_view(), name='user-update-profile'),
]
