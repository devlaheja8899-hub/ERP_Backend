from rest_framework.viewsets import ModelViewSet
from invoices.models import Invoice
from invoices.serializers import InvoiceSerializer

class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer