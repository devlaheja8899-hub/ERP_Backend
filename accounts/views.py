from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Company
from .serializers import CustomerSerializer, CompanySerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = []

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]