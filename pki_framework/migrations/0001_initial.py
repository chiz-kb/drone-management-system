# Generated by Django 4.0.4 on 2022-04-26 09:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AerobridgeCredential',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Provide a friendly name / description for the type of credential you are storing e.g. eBee Public Key', max_length=100, validators=[django.core.validators.RegexValidator(message='No special characters allowed in this field.', regex='^[-, ,_\\w]*$')])),
                ('token_type', models.IntegerField(choices=[(0, 'Public Key'), (2, 'Authentication Token'), (3, 'Other'), (4, 'x509 Digital Certificate')], help_text='Set the type of credential this is, e.g Public / Private Key etc.')),
                ('association', models.IntegerField(choices=[(0, 'Operator'), (1, 'Manufacturer'), (2, 'Pilot'), (3, 'RFM'), (4, 'Company'), (5, 'Management Server')], default=4, help_text='Set the entity this credential is associated with. The association will be used when calling external servers.')),
                ('token', models.BinaryField()),
                ('extension', models.IntegerField(choices=[(0, 'other'), (1, '.der'), (2, '.csr'), (3, '.key'), (4, '.cer'), (5, '.pem')], default=0, help_text='Specify the data format for this credential, if known')),
                ('is_active', models.BooleanField(default=True, help_text='Set whether the credential is still active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('aircraft', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registry.aircraft')),
                ('manufacturer', models.ForeignKey(blank=True, limit_choices_to={'role': 1}, null=True, on_delete=django.db.models.deletion.CASCADE, to='registry.company')),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registry.operator')),
            ],
        ),
    ]
