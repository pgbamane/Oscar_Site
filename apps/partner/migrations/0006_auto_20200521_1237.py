# Generated by Django 2.1.1 on 2020-05-21 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0005_stockrecord_pricing_strategy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockrecord',
            name='pricing_strategy',
            field=models.CharField(blank=True, choices=[('PREMIUM', 'Premium'), ('GOLD', 'Gold'), ('', 'None')], default='', help_text='Specify Premium or Gold for child products. Not neccessary for Parent', max_length=100),
        ),
    ]
