# Generated by Django 2.1.1 on 2020-05-29 07:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('customer_final', '0004_email_save'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name='Last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='Staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='Active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(blank=True, choices=[('female', 'Female'), ('male', 'Male')], default='', max_length=20)),
                ('address', models.CharField(default='', help_text='Flat No, Building, Street, Area', max_length=255)),
                ('locality', models.CharField(default='', help_text='Locality/Town', max_length=50)),
                ('state', models.CharField(default='', max_length=50)),
                ('district', models.CharField(default='', max_length=50)),
                ('city', models.CharField(default='', help_text='City or Taluka', max_length=50)),
                ('pincode', models.CharField(default='', help_text='Pincode stored as Chars', max_length=10)),
                ('phone_number', models.CharField(blank=True, max_length=13, null=True, unique=True)),
                ('is_superuser', models.BooleanField(db_column='Is Superuser', default=False, help_text='Designates whether this customer_final has all permissions in the admin page or not', verbose_name='is_superuser')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'swappable': 'AUTH_USER_MODEL',
            },
        ),
    ]
