# Generated by Django 4.0.3 on 2022-04-08 18:47

import DenzelProject.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogPost', '0004_dislike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='header',
            field=models.CharField(max_length=30, verbose_name=DenzelProject.validators.MinValidator(3)),
        ),
        migrations.AlterField(
            model_name='post',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
