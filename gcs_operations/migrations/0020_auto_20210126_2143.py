# Generated by Django 3.1.5 on 2021-01-26 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcs_operations', '0019_auto_20210123_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightoperation',
            name='name',
            field=models.CharField(default='Flight Operation rzgcsu', max_length=30),
        ),
        migrations.AlterField(
            model_name='flightplan',
            name='name',
            field=models.CharField(default='Flight Plan gxjxzh', max_length=30),
        ),
    ]