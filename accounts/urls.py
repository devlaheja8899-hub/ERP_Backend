from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, CompanyViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'companies', CompanyViewSet, basename='companies')

urlpatterns = [
    path('', include(router.urls)),
]