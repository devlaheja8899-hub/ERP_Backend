from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'company_name',
        'customer_id',
        'customer_name',
        'contact_person_name',
        'contact_number',
        'sales_person',  
        'territory',
        'industry',
        'is_active',
    )

    list_filter = (
        'territory',
        'industry',
        'is_active',
    )

    search_fields = (
        'company_name',
        'customer_name',
        'customer_id',
        'contact_person_name',
        'contact_number',
        'gst_number',
    )