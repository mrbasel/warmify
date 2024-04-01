# Generated by Django 5.0.2 on 2024-03-08 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warmify_core', '0003_alter_iotdevice_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='metadata',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='iotdevice',
            name='metadata',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
