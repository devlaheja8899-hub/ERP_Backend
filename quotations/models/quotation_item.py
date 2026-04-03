from decimal import Decimal
from django.db import models
from .quotation import Quotation
from invoices.models.items import Item


class QuotationItem(models.Model):

    PACKAGING_CHOICES = [
        ('REEL', 'Reel'),
        ('TRAY', 'Tray'),
        ('TUBE', 'Tube'),
        ('LOOSE', 'Loose'),
    ]

    quotation = models.ForeignKey(
        Quotation,
        related_name='items',
        on_delete=models.CASCADE
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT
    )

    manufacturer = models.CharField(max_length=255, blank=True)
    mpn = models.CharField(max_length=255, blank=True)
    date_code = models.CharField(max_length=50, blank=True)

    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    gst_percentage = models.PositiveIntegerField(default=18)

    packaging_type = models.CharField(
        max_length=10,
        choices=PACKAGING_CHOICES
    )

    description = models.TextField(blank=True)

    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    gst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_with_gst = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.unit_price
        self.gst_amount = (self.amount * Decimal(self.gst_percentage)) / Decimal('100')
        self.total_with_gst = self.amount + self.gst_amount

        super().save(*args, **kwargs)
        self.quotation.recalculate_totals()

    def __str__(self):
        return f"{self.quotation.quotation_no} - {self.item}"