# Generated by Django 5.0.6 on 2024-05-22 21:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_notification_url_alter_notification_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='event.event'),
        ),
    ]