# Generated by Django 5.1.1 on 2024-09-25 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_cart_cart_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_key',
            field=models.CharField(blank=True, default='', max_length=255, null=True, unique=True),
        ),
    ]
