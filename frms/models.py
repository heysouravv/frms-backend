from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.apps import apps
from django.utils import timezone
# from .tax_categories import TaxSlab, ProductCategory
from django.utils.translation import gettext_lazy as _
import datetime
from django.contrib.auth.base_user import BaseUserManager

def generate_company_id(company_name, year):
    # Get the first 2, 3, or 4 characters of the company name based on its length
    if len(company_name) >= 4:
        company_prefix = company_name[:4].upper()
    elif len(company_name) == 3:
        company_prefix = company_name[:3].upper()
    else:
        company_prefix = company_name[:2].upper()
    # Generate the company ID in the desired format
    company_id = f"{company_prefix}-{year}"
    return company_id

class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    company_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate the company ID if it doesn't exist
        if not self.company_id:
            current_year = datetime.date.today().year
            self.company_id = generate_company_id(self.name, current_year)
        super().save(*args, **kwargs)

class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

# class Customer(models.Model):
#     prefix = models.CharField(max_length=10)
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#     name = models.CharField(max_length=100)
#     address = models.TextField()
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)

#     def __str__(self):
#         return self.name

class Product(models.Model):
    branches = models.ManyToManyField(Branch, through='BranchStock')
    name = models.CharField(max_length=100, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    hsn_code = models.CharField(max_length=100, default='')
    min_order_level = models.IntegerField(default=0)
    max_order_level = models.IntegerField(default=0)
    re_order_level = models.IntegerField(default=0)
    purchase_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sale_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    damage_stock = models.IntegerField(default=0)
    empty_stock = models.IntegerField(default=0)
    stokable_flag = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class BranchStock(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('branch', 'product')

class ProductPriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-effective_date']

    def __str__(self):
        return f"{self.product.name} - {self.price} (Effective: {self.effective_date})"

# class DiscountMaster(models.Model):
#     DISCOUNT_TYPE_CHOICES = [
#         ('customer', 'Customer'),
#         ('product', 'Product'),
#         ('category', 'Product Category'),
#     ]

#     DISCOUNT_MODE_CHOICES = [
#         ('percentage', 'Percentage'),
#         ('fixed', 'Fixed Amount'),
#         ('min_order', 'Minimum Order Quantity'),
#     ]

#     discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
#     customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True)
#     product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True)
#     product_category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, null=True, blank=True)
#     discount_mode = models.CharField(max_length=20, choices=DISCOUNT_MODE_CHOICES)
#     discount_value = models.DecimalField(max_digits=10, decimal_places=2)
#     min_order_quantity = models.PositiveIntegerField(null=True, blank=True)
#     effective_date = models.DateField(default=timezone.now)
#     expires_on = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.get_discount_type_display()} - {self.discount_mode}"


class CustomUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('finance', 'Finance'),
        ('cashier', 'Cashier'),
    )
    role = models.CharField(max_length=20, choices=USER_ROLES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',  # Add this line
        related_query_name='customuser',  # Add this line
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',  # Add this line
        related_query_name='customuser',  # Add this line
    )
