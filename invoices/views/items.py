from rest_framework.viewsets import ModelViewSet
from invoices.models import Item
from invoices.serializers import ItemSerializer

class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer