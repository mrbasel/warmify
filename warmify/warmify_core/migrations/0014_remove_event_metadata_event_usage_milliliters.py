# Generated by Django 4.2.11 on 2024-05-12 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("warmify_core", "0013_alter_event_timestamp_alter_ping_timestamp"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="metadata",
        ),
        migrations.AddField(
            model_name="event",
            name="usage_milliliters",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Usage in milliliters"
            ),
        ),
    ]
