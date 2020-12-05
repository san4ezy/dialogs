from django.urls import path
from rest_framework import routers
from . import views


urlpatterns = [
]

router = routers.DefaultRouter()
router.register('messages', views.MessageViewSet, basename='messages')
router.register('dialogs', views.DialogViewSet, basename='dialogs')

urlpatterns += router.urls
