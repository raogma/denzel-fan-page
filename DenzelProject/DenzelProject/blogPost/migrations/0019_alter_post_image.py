# Generated by Django 4.0.3 on 2022-04-10 20:47

import DenzelProject.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogPost', '0018_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', validators=[DenzelProject.validators.MaxSizeValidatorMB(2)]),
        ),
    ]
