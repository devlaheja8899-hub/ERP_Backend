from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Quotation
from .serializers import QuotationSerializer


class QuotationViewSet(viewsets.ModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = [IsAuthenticated]