# Generated by Django 5.1.3 on 2024-11-24 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0003_alter_cart_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
