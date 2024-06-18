from django.db import models

class TaxSlab(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @classmethod
    def create_default_tax_slabs(cls):
        default_tax_slabs = [
            {'name': 'GST 0%', 'tax_rate': 0.0, 'is_default': True},
            {'name': 'GST 5%', 'tax_rate': 5.0, 'is_default': False},
            {'name': 'GST 12%', 'tax_rate': 12.0, 'is_default': False},
            {'name': 'GST 18%', 'tax_rate': 18.0, 'is_default': False},
            {'name': 'GST 28%', 'tax_rate': 28.0, 'is_default': False},
        ]

        for tax_slab_data in default_tax_slabs:
            tax_slab, created = cls.objects.get_or_create(
                name=tax_slab_data['name'],
                defaults={
                    'tax_rate': tax_slab_data['tax_rate'],
                    'is_default': tax_slab_data['is_default'],
                }
            )
            if created:
                print(f"Created default tax slab: {tax_slab.name}")
            else:
                print(f"Default tax slab already exists: {tax_slab.name}")

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    tax_slab = models.ForeignKey(TaxSlab, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
