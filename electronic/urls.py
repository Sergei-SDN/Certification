from django.urls import path, include
from rest_framework.routers import DefaultRouter

from electronic.apps import ElectronicConfig
from electronic.views import NetworkViewSet

app_name = ElectronicConfig.name

router = DefaultRouter()
router.register(r'networks', NetworkViewSet, basename='network')

urlpatterns = [
    path('api/', include(router.urls))
]
