# Generated by Django 5.1.7 on 2025-04-13 08:53

import encrypted_fields.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_category_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=encrypted_fields.fields.EncryptedFloatField(),
        ),
    ]
