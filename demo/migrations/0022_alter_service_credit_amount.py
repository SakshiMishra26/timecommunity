# Generated by Django 5.1.4 on 2025-01-26 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0021_service_credit_amount_service_is_completed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='credit_amount',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=10),
        ),
    ]
