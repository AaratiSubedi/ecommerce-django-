# Generated by Django 5.0.6 on 2024-05-31 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_product_orderitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping',
            field=models.BooleanField(default=False),
        ),
    ]
