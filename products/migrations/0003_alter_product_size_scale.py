# Generated by Django 5.0.3 on 2024-03-23 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_rename_city_company_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size_scale',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.sizescale'),
        ),
    ]
