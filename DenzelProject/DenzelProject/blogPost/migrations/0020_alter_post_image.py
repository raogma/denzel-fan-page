# Generated by Django 4.0.3 on 2022-04-15 13:36

import DenzelProject.validators
import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogPost', '0019_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, validators=[DenzelProject.validators.MaxSizeValidatorMB(2)]),
        ),
    ]
