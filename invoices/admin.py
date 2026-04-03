from django.contrib import admin
from invoices.models import Invoice, InvoiceItem
from invoices.models.items import Item


# =========================
# ITEM MASTER
# =========================
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ('item_name', 'manufacturer_part_number')
    list_display = ('item_id', 'item_name', 'stock_quantity')


# =========================
# INVOICE ITEM INLINE
# =========================
class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    autocomplete_fields = ['item']

    def has_add_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.status == 'DRAFT'

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.status == 'DRAFT'

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.status == 'DRAFT'


# =========================
# INVOICE ADMIN
# =========================
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_no',
        'customer',
        'status',
        'taxable_value',
        'gst_amount',
        'grand_total',
    )

    readonly_fields = ('invoice_no', 'created_at')
    inlines = [InvoiceItemInline]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != 'DRAFT':
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False  # NEVER delete invoices