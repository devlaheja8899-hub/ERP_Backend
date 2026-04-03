from rest_framework import serializers
from django.utils import timezone
from .models import Quotation, QuotationItem


class QuotationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = "__all__"


class QuotationSerializer(serializers.ModelSerializer):
    items = QuotationItemSerializer(many=True, read_only=True)
    quotation_date = serializers.DateField(required=False, allow_null=True)
    
    class Meta:
        model = Quotation
        fields = "__all__"
        read_only_fields = ['quotation_no', 'created_at']
    
    def create(self, validated_data):
        # If quotation_date is not provided or is None, use today's date
        if not validated_data.get('quotation_date'):
            validated_data['quotation_date'] = timezone.now().date()
        return super().create(validated_data)