from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    address = models.TextField()
    gst_no = models.CharField(max_length=20)
    state_name = models.CharField(max_length=100)
    state_code = models.CharField(max_length=10)
    cin_no = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    contact_no = models.CharField(max_length=15)
    pan_no = models.CharField(max_length=20)

    bank_name = models.CharField(max_length=100)
    bank_account_no = models.CharField(max_length=50)
    bank_ifsc = models.CharField(max_length=20)
    bank_branch = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Customer(models.Model):

    # -------------------------------
    # CHOICE DEFINITIONS
    # -------------------------------
    CURRENCY_CHOICES = [
        ('INR', 'Indian Rupee (INR)'),
        ('USD', 'US Dollar (USD)'),
    ]
    TERRITORY_CHOICES = [
        ('WEST', 'West'),
        ('EAST', 'East'),
        ('NORTH', 'North'),
        ('SOUTH', 'South'),
    ]

    INDUSTRY_CHOICES = [
        ('CONSUMER', 'Consumer'),
        ('INDUSTRIAL', 'Industrial'),
        ('AUTOMOTIVE', 'Automotive'),
        ('DEFENCE', 'Defence / Space / Navy'),
        ('MEDICAL', 'Medical'),
        ('RAILWAYS', 'Railways & Transportation'),
        ('LIGHTNING', 'Lightning'),
        ('EMS', 'EMS'),
        ('PREMIUM', 'Premium'),
        ('LOW_COST', 'Low Cost'),
        ('TRADER', 'Trader'),
    ]

    COURIER_MODE_CHOICES = [
        ('AIR', 'Air'),
        ('SURFACE', 'Surface'),
    ]

    LEAD_SOURCE_CHOICES = [
        ('EXHIBITION', 'Exhibition'),
        ('EMAIL', 'Email'),
        ('WEBSITE', 'Website'),
        ('CALL', 'Call'),
        ('LINKEDIN', 'LinkedIn'),
        ('OLD_CUSTOMER', 'Old Customer'),
        ('MARKET', 'Market'),
    ]

    CREDIT_RATING_CHOICES = [
        ('A+', 'A+'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
 
    PAYMENT_TERMS_CHOICES = [
        ('ADVANCE', 'Advance'),
        ('ADVANCE_PDC', 'Advance PDC'),
        ('30_DAYS', '30 Days'),
        ('45_DAYS', '45 Days'),
        ('60_DAYS', '60 Days'),
        ('90_DAYS', '90 Days'),
    ]

    CREDIT_DAYS_CHOICES = [
        ('30', '30 Days'),
        ('45', '45 Days'),
        ('60', '60 Days'),
        ('90', '90 Days'),
    ]

    TURNOVER_SOURCE_CHOICES = [
        ('VERBAL', 'Verbal'),
        ('ONLINE', 'Online (MCA)'),
    ]

    # -------------------------------
    # CUSTOMER MASTER
    # -------------------------------

    company_name = models.CharField(max_length=200)
    customer_id = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=200)

    contact_person_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    currency = models.CharField(
       max_length=3,
       choices=CURRENCY_CHOICES
    )
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    pan_no = models.CharField(max_length=20, blank=True, null=True)
    state_code = models.CharField(max_length=10, blank=True, null=True)
    buyer_project_name = models.CharField(max_length=200, blank=True, null=True)

    preferred_courier_name = models.CharField(
       max_length=100,
        blank=True,
        null=True
    )

    preferred_courier_mode = models.CharField(
        max_length=10,
        choices=COURIER_MODE_CHOICES,
        blank=True,
        null=True
    )

    industry = models.CharField(
        max_length=20,
        choices=INDUSTRY_CHOICES,
        blank=True,
        null=True
    )

    customer_products = models.TextField(blank=True, null=True)

    sales_person = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    territory = models.CharField(
        max_length=10,
        choices=TERRITORY_CHOICES,
        blank=True,
        null=True
    )

    dispatch_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)

    date_of_enrollment = models.DateField(blank=True, null=True)

    lead_source = models.CharField(
        max_length=20,
        choices=LEAD_SOURCE_CHOICES,
        blank=True,
        null=True
    )

    annual_purchase_potential = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    creditability_rating = models.CharField(
        max_length=2,
        choices=CREDIT_RATING_CHOICES,
        blank=True,
        null=True
    )

    credit_review_required = models.BooleanField(default=False)

    last_financial_turnover = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True
    )

    customer_turnover = models.CharField(
        max_length=10,
        choices=TURNOVER_SOURCE_CHOICES,
        blank=True,
        null=True
    )

    payment_terms = models.CharField(
       max_length=20,
       choices=PAYMENT_TERMS_CHOICES,
       blank=True,
       null=True
    )

    lc_terms = models.CharField(
        max_length=5,
        choices=CREDIT_DAYS_CHOICES,
        blank=True,
        null=True
    )

    oc_terms = models.CharField(
       choices=CREDIT_DAYS_CHOICES,
        blank=True,
        null=True
    )

    # -------------------------------
    # SYSTEM
    # -------------------------------

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.customer_name}"