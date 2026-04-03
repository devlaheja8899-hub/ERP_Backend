from decimal import Decimal
from django.db import models, transaction
from accounts.models import Customer, Company
from django.db.models import Max


class Invoice(models.Model):

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ISSUED', 'Issued'),
        ('CANCELLED', 'Cancelled'),
    ]

    PAYMENT_MODE_CHOICES = [
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('ONLINE', 'Online Transfer'),
        ('CREDIT', 'Credit'),
    ]

    DISPATCH_MODE_CHOICES = [
        ('COURIER', 'Courier'),
        ('HAND_DELIVERY', 'Hand Delivery'),
        ('POST', 'Post'),
    ]

    invoice_no = models.PositiveIntegerField(
        unique=True,
        editable=False
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    invoice_date = models.DateField()
    due_date = models.DateField()
    delivery_date = models.DateField(blank=True, null=True)

    e_way_bill_no = models.CharField(max_length=50, blank=True, null=True)
    e_invoice_no = models.CharField(max_length=50, blank=True, null=True)
    insurance_no = models.CharField(max_length=50, blank=True, null=True)

    mode_of_payment = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE_CHOICES,
        blank=True, null=True
    )

    customer_po_no = models.CharField(max_length=50, blank=True, null=True)
    customer_po_date = models.DateField(blank=True, null=True)

    dispatch_docket_no = models.CharField(max_length=50, blank=True, null=True)
    dispatch_courier_name = models.CharField(max_length=100, blank=True, null=True)
    dispatch_mode = models.CharField(
        max_length=20,
        choices=DISPATCH_MODE_CHOICES,
        blank=True, null=True
    )

    taxable_value = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    gst_amount = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    discount = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    shipping_charges = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    round_off = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    grand_total = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )

    total_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    amount_in_words = models.TextField(blank=True)

    prepared_by = models.CharField(max_length=100, blank=True, null=True)
    verified_by = models.CharField(max_length=100, blank=True, null=True)
    authorized_by = models.CharField(max_length=100, blank=True, null=True)

    terms_conditions_original = models.TextField(blank=True)
    terms_conditions_duplicate = models.TextField(blank=True)
    terms_conditions_extra = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # =========================
    # AUTO INVOICE NUMBER LOGIC
    # =========================
    def save(self, *args, **kwargs):
        if not self.pk:
            with transaction.atomic():
                last_no = Invoice.objects.aggregate(
                    max_no=Max('invoice_no')
                )['max_no'] or 0
                self.invoice_no = last_no + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"INV-{self.invoice_no}"


class InvoiceItem(models.Model):
    GST_SLAB_CHOICES = [
        ('18_9_9', 'IGST 18%, CGST 9%, SGST 9%'),
        ('18_2.5_2.5', 'IGST 18%, CGST 2.5%, SGST 2.5%'),
        ('12_6_6', 'IGST 12%, CGST 6%, SGST 6%'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey('Item', on_delete=models.PROTECT, blank=True, null=True)
    description = models.TextField(blank=True)
    hsn_code = models.CharField(max_length=20, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    gst_slab = models.CharField(max_length=20, choices=GST_SLAB_CHOICES, default='18_9_9')

    manufacture_name = models.CharField(max_length=100, blank=True, null=True)
    date_code = models.CharField(max_length=50, blank=True, null=True)
    customer_item_code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.description} - {self.quantity}"