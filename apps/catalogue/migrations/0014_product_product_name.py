# Generated by Django 2.1.1 on 2020-04-26 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0013_auto_20170821_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
