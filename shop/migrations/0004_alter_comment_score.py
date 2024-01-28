# Generated by Django 4.1.3 on 2022-12-16 09:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_comment_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
    ]
