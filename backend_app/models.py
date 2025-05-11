from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class SuperAdmin(AbstractUser):
    username = None
    last_name = None 
    first_name = None
    is_superuser = None 
    last_login = None 
    is_staff = None 
    date_joined = None 
    full_name = models.CharField(max_length=200, blank=False)
    email = models.EmailField('email address', unique=True, blank=False)
    password = models.CharField(max_length=300, blank=False)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="superadmin_groups",
        related_query_name="superadmin",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="superadmin_permissions",
        related_query_name="superadmin",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Admin(AbstractUser):
    username = None
    last_name = None 
    first_name = None
    is_superuser = None 
    last_login = None 
    is_staff = None 
    date_joined = None 
    full_name = models.CharField(max_length=200, blank=False)
    email = models.EmailField('email address', unique=True, blank=False)
    password = models.CharField(max_length=300, blank=False)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="admin_groups",
        related_query_name="admin",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="admin_permissions",
        related_query_name="admin",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Doctor(models.Model):
    username = None
    last_name = None 
    first_name = None
    is_superuser = None 
    last_login = None 
    is_staff = None 
    date_joined = None 
    registiration_number = models.IntegerField(
        validators=[
            MinValueValidator(1000000000),
            MaxValueValidator(9999999999)
        ],
        unique=True,
        blank=False,
    )
    full_name = models.CharField(max_length=200, blank=False)
    email = models.EmailField('email address', unique=True, blank=False)
    password = models.CharField(max_length=300, blank=False)
    state = models.CharField(max_length=200, blank=False)
    city = models.CharField(max_length=200, blank=False)
    office_adress = models.CharField(max_length=200, blank=False)
    zip_code = models.IntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(9999)
        ],
        blank=False
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="doctor_groups",
        related_query_name="doctor",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="doctor_permissions",
        related_query_name="doctor",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Patient(AbstractUser):
    username = None
    last_name = None 
    first_name = None
    is_superuser = None 
    last_login = None 
    is_staff = None 
    date_joined = None 
    full_name = models.CharField(max_length=200, blank=False)
    email = models.EmailField('email address', unique=True, blank=False)
    password = models.CharField(max_length=300, blank=False)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patients')
    status = models.CharField(
        max_length=20,
        choices=[
            ('IN PROGRESS', 'IN PROGRESS'),
            ('COMPLETED', 'Completed'),
            ('CANCELLED', 'Cancelled'),
        ],
        default='IN PROGRESS'
    )
    state = models.CharField(max_length=200, blank=False)
    city = models.CharField(max_length=200, blank=False)
    patient_adress = models.CharField(max_length=200, blank=False)
    zip_code = models.IntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(9999)
        ],
        blank=False
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="patient_groups",
        related_query_name="patient",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="patient_permissions",
        related_query_name="patient",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Aligner(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='aligners')
    aligner_number = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(222)
        ],
        blank=False
    )
    wearing_day = models.DateField()
    weared_hours = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(24)
        ],
        blank=False
    )
    photo = models.CharField(max_length=9999)

class Appointement (models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    treatment_duration = models.IntegerField()
    appointemnt_day = models.DateField() # Bech ye5o rendez vous kol mara ------->  ya3ni yekml treatment_duration y3awed ya5o rendez vous
    is_paid = models.BooleanField(default=False)




