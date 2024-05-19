# Generated by Django 5.0.6 on 2024-05-19 12:13

from django.db import migrations


def update_priorities(apps, schema_editor):
    Event = apps.get_model('event', 'Event')

    # Обновление значений
    Event.objects.filter(priority='low').update(priority=0)
    Event.objects.filter(priority='medium').update(priority=1)
    Event.objects.filter(priority='high').update(priority=2)


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_event_priority'),
    ]

    operations = [
        migrations.RunPython(update_priorities),
    ]
