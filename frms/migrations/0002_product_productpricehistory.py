# Generated by Django 5.0.6 on 2024-06-18 05:06

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('hsn_code', models.CharField(default='', max_length=100)),
                ('min_order_level', models.IntegerField(default=0)),
                ('max_order_level', models.IntegerField(default=0)),
                ('re_order_level', models.IntegerField(default=0)),
                ('purchase_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sale_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('damage_stock', models.IntegerField(default=0)),
                ('empty_stock', models.IntegerField(default=0)),
                ('stokable_flag', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('quantity', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='frms.branch')),
                ('company', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='frms.company')),
            ],
        ),
        migrations.CreateModel(
            name='ProductPriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('effective_date', models.DateField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_history', to='frms.product')),
            ],
            options={
                'ordering': ['-effective_date'],
            },
        ),
    ]
