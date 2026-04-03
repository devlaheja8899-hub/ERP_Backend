from decimal import Decimal
from django.db import models
from django.utils import timezone
from accounts.models import Customer
from invoices.models.items import Item


class Quotation(models.Model):

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CONVERTED', 'Converted to Invoice'),
    ]

    INQUIRY_SOURCE_CHOICES = [
        ('EMAIL', 'Email'),
        ('WHATSAPP', 'WhatsApp / Messenger'),
        ('PHONE', 'Phone'),
        ('EXHIBITION', 'Exhibition'),
        ('WEBSITE', 'Website'),
        ('REFERENCE', 'Reference'),
    ]

    CURRENCY_CHOICES = [
        ('INR', 'INR'),
        ('USD', 'USD'),
    ]

    quotation_no = models.CharField(max_length=20, unique=True, editable=False)
    quotation_date = models.DateField(default=timezone.now)

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    contact_person = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)

    inquiry_source = models.CharField(
        max_length=20,
        choices=INQUIRY_SOURCE_CHOICES
    )

    sales_person = models.CharField(max_length=255)

    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        default='INR'
    )

    freight_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    validity_days = models.PositiveIntegerField(default=7)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    # Delivery details
    lead_time = models.CharField(max_length=100, blank=True, null=True)
    delivery_docket_details = models.TextField(blank=True, null=True)
    dispatch_mode = models.CharField(max_length=100, blank=True, null=True)

    # Totals
    taxable_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    gst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def generate_quotation_no(self):
        year = timezone.now().year
        prefix = f"VIQ-{year}-"
        last = Quotation.objects.filter(
            quotation_no__startswith=prefix
        ).order_by('-quotation_no').first()

        if last:
            last_number = int(last.quotation_no.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"{prefix}{str(new_number).zfill(4)}"

    def save(self, *args, **kwargs):
        if not self.quotation_no:
            self.quotation_no = self.generate_quotation_no()
        super().save(*args, **kwargs)

    def recalculate_totals(self):
        taxable = sum(i.amount for i in self.items.all())
        gst = sum(i.gst_amount for i in self.items.all())

        self.taxable_value = taxable
        self.gst_amount = gst
        self.grand_total = taxable + gst + self.freight_charges

        super().save(update_fields=[
            'taxable_value',
            'gst_amount',
            'grand_total'
        ])

    def __str__(self):
        return self.quotation_no