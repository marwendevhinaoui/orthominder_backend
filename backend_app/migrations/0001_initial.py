# Generated by Django 5.2 on 2025-05-25 17:36

import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('password', models.CharField(max_length=300)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='admin_groups', related_query_name='admin', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='admin_permissions', related_query_name='admin', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registiration_number', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)])),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('password', models.CharField(max_length=300)),
                ('state', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('office_adress', models.CharField(max_length=200)),
                ('phone_number', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(99999999)])),
                ('zip_code', models.IntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(9999)])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='doctor_groups', related_query_name='doctor', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='doctor_permissions', related_query_name='doctor', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('password', models.CharField(max_length=300)),
                ('phone_number', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(99999999)])),
                ('state', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('patient_adress', models.CharField(max_length=200)),
                ('zip_code', models.IntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(9999)])),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_app.doctor')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='patient_groups', related_query_name='patient', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='patient_permissions', related_query_name='patient', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Appointement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('treatment_duration', models.IntegerField()),
                ('appointemnt_day', models.DateField()),
                ('next_appointemnt_day', models.DateField()),
                ('aligner_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(222)])),
                ('is_paid', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('IN PROGRESS', 'IN PROGRESS'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='IN PROGRESS', max_length=20)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_app.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_app.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Aligner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_aligner', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(222)])),
                ('wearing_day', models.DateField()),
                ('weared_hours', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)])),
                ('photo', models.ImageField(upload_to='aligner_photos/')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Under review', 'Under review'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_app.appointement')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_app.patient')),
            ],
        ),
        migrations.CreateModel(
            name='SuperAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('password', models.CharField(max_length=300)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='superadmin_groups', related_query_name='superadmin', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='superadmin_permissions', related_query_name='superadmin', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
