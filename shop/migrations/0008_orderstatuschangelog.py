# Generated by Django 5.1.1 on 2024-09-14 08:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_customer_is_active_order_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatusChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.CharField(max_length=20)),
                ('new_status', models.CharField(max_length=20)),
                ('changed_at', models.DateField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.order')),
            ],
        ),
    ]