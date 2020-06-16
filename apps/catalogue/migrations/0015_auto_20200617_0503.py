# Generated by Django 2.1.1 on 2020-06-16 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0014_auto_20200529_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tag',
        ),
        migrations.AddField(
            model_name='product',
            name='certified',
            field=models.BooleanField(default=False, help_text='This flag indicates if this product is certified organic or not. Specify for only child product.', verbose_name='Is Certified Organic'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.IntegerField(blank=True, help_text='Total weight of this Product Purchase. Empty for Parent', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_unit',
            field=models.CharField(choices=[('Kg', 'Kg'), ('g', 'g'), ('Ltr', 'Ltr'), ('ML', 'ML')], default='', help_text='Unit used to measure Weight. Ex. Kilogram used to measure quanitity of Pulses. Optional for child product. For parent specify it.', max_length=20),
        ),
    ]
