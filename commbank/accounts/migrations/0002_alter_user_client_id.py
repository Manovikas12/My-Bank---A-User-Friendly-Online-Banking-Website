# Generated by Django 5.0 on 2024-02-22 07:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='client_id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(5)]),
        ),
    ]
