# Generated by Django 4.2.8 on 2023-12-13 14:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0007_purchaseorder_prev_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 20, 16, 2, 611838)),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='prev_status',
            field=models.CharField(default='', max_length=10),
        ),
    ]