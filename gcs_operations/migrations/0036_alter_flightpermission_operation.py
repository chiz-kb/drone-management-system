# Generated by Django 3.2.5 on 2021-07-13 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gcs_operations', '0035_cloudfile_upload_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightpermission',
            name='operation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Operation', to='gcs_operations.flightoperation'),
        ),
    ]
