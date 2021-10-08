# Generated by Django 3.2.8 on 2021-10-08 16:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0065_auto_20211008_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operator',
            name='company_number',
            field=models.CharField(blank=True, default='CO-TMP', help_text='Company number if avaiable', max_length=25, null=True, validators=[django.core.validators.RegexValidator(message='No special characters allowed in this field.', regex='^[-, ,_\\w]*$')]),
        ),
        migrations.AlterField(
            model_name='operator',
            name='country',
            field=models.CharField(choices=[('IN', 'INDIA')], default='IN', help_text='At the moment only India is configured, you can setup your own country', max_length=2),
        ),
        migrations.AlterField(
            model_name='operator',
            name='insurance_number',
            field=models.CharField(blank=True, default='INS-TMP', help_text='Insurance number if avaialble', max_length=25, null=True, validators=[django.core.validators.RegexValidator(message='No special characters allowed in this field.', regex='^[-, ,_\\w]*$')]),
        ),
        migrations.AlterField(
            model_name='operator',
            name='vat_number',
            field=models.CharField(blank=True, default='VAT-TMP', help_text='VAT / Tax number if available', max_length=25, null=True, validators=[django.core.validators.RegexValidator(message='No special characters allowed in this field.', regex='^[-, ,_\\w]*$')]),
        ),
    ]