from django.contrib import admin
from .models import Quotation, QuotationItem


class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 1
    autocomplete_fields = ['item']


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = (
        'quotation_no',
        'customer',
        'quotation_date',
        'currency',
        'grand_total',
    )
    readonly_fields = ('quotation_no',)
    inlines = [QuotationItemInline]


@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['item']