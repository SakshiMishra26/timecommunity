# Generated by Django 5.1.4 on 2025-01-22 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0013_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicerequest',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
