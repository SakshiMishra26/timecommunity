# Generated by Django 5.1.4 on 2025-02-15 08:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0029_remove_servicelog_duration_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timecredit',
            name='hours_available',
        ),
        migrations.RemoveField(
            model_name='timecredit',
            name='service',
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='credit_requested',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='servicelog',
            name='request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='demo.servicerequest'),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
