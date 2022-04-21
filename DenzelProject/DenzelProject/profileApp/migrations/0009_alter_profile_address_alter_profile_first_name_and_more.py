# Generated by Django 4.0.3 on 2022-04-08 18:47

import DenzelProject.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileApp', '0008_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=DenzelProject.validators.MinValidator(3)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name=DenzelProject.validators.MinValidator(2)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name=DenzelProject.validators.MinValidator(2)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[DenzelProject.validators.validate_phone_only_numbers], verbose_name=DenzelProject.validators.MinValidator(5)),
        ),
    ]
