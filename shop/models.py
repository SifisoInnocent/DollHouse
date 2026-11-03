import uuid
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('frontals', 'Frontals'),
        ('hair-products', 'Hair Products'),
        ('consumables', 'Consumables'),
        ('tripods', 'Tripods'),
    ]
    STATUS_CHOICES = [
        ('in-stock', 'In Stock'),
        ('unavailable', 'Unavailable'),
        ('date', 'Coming Soon'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    inches = models.CharField(max_length=50, blank=True, default="")
    size = models.CharField(max_length=50, blank=True, default="")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='in-stock')
    avail_date = models.CharField(max_length=50, blank=True, default="")
    desc = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    name = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating} stars"

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_summary = models.TextField()
    customer = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True, default="")
    notes = models.TextField(blank=True, default="")
    channel = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer}"

class StoreSettings(models.Model):
    # Singleton settings model
    email_config_key = models.CharField(max_length=255, blank=True, default="")
    email_config_service = models.CharField(max_length=255, blank=True, default="")
    email_config_template = models.CharField(max_length=255, blank=True, default="")
    email_config_owner_email = models.EmailField(blank=True, default="")
    salon_image_1 = models.ImageField(upload_to='salon/', blank=True, null=True, verbose_name="Salon Image 1")
    salon_image_2 = models.ImageField(upload_to='salon/', blank=True, null=True, verbose_name="Salon Image 2")
    salon_image_3 = models.ImageField(upload_to='salon/', blank=True, null=True, verbose_name="Salon Image 3")
    salon_image_4 = models.ImageField(upload_to='salon/', blank=True, null=True, verbose_name="Salon Image 4")

    def __str__(self):
        return "Store Settings"

    class Meta:
        verbose_name = "Store Settings"
        verbose_name_plural = "Store Settings"
