from django.db import models

class Item(models.Model):

    CATEGORY_CHOICES = [
        ("resistor", "Resistor"),
        ("capacitor", "Capacitor"),
        ("ics", "ICs"),
        ("conductors", "Conductors"),
        ("diode", "Diode"),
        ("connector", "Connector"),
        ("mosfets", "Mosfets"),
    ]

    SALES_UNIT_CHOICES = [
        ("nos", "Nos"),
        ("reel", "Reel"),
        ("tray", "Tray"),
    ]

    item_id = models.CharField(max_length=50, unique=True)
    item_name = models.CharField(max_length=255)

    manufacturer_part_number = models.CharField(max_length=100)
    manufacturer_name = models.CharField(max_length=255)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    name = models.CharField(
      max_length=255,
      null=True,
      blank=True
    )
    description = models.TextField(blank=True, null=True)
    hsn_code = models.CharField(max_length=20)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    stock_quantity = models.PositiveIntegerField(default=0)
    last_purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order_quantity = models.PositiveIntegerField()

    sales_unit = models.CharField(
        max_length=10,
        choices=SALES_UNIT_CHOICES
    )

    datasheet_link = models.URLField(blank=True, null=True)
    hsn_code = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_id} - {self.item_name}"
