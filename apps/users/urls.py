from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views


urlpatterns = [
    path('auth/signin/', views.CustomTokenObtainPairView.as_view(), name='signin'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verification/', TokenVerifyView.as_view(), name='token_verification'),
]

router = routers.DefaultRouter()
router.register('auth', views.AuthViewSet, basename='auth')

urlpatterns += router.urls
