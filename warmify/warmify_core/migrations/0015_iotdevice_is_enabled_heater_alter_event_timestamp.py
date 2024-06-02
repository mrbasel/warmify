# Generated by Django 4.2.11 on 2024-05-16 15:13

from django.db import migrations, models
import warmify_core.models.event


class Migration(migrations.Migration):

    dependencies = [
        ("warmify_core", "0014_remove_event_metadata_event_usage_milliliters"),
    ]

    operations = [
        migrations.AddField(
            model_name="iotdevice",
            name="is_enabled_heater",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="timestamp",
            field=models.DateTimeField(
                default=warmify_core.models.event.default_datetime,
                verbose_name="event timestamp",
            ),
        ),
    ]