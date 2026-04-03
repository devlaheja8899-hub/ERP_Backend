from rest_framework import serializers
from invoices.models import Item, Invoice, InvoiceItem
from accounts.models import Company, Customer
from accounts.serializers import CompanySerializer, CustomerSerializer


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class InvoiceItemSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), required=False)

    class Meta:
        model = InvoiceItem
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = "__all__"

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance = super().update(instance, validated_data)
        # Handle items update - this is simplified
        return instance