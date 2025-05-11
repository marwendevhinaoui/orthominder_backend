from rest_framework import serializers

from backend_app.models import Patient, SuperAdmin, Admin, Doctor

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['id', 'full_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'full_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'id', 'full_name', 'registiration_number', 'email', 'password',
            'state', 'city', 'office_adress', 'zip_code'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }


class PatientSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())

    class Meta:
        model = Patient
        fields = [
            'id', 'full_name', 'email', 'password',
            'current_appointemnt_day', 'next_appointemnt_day', 'doctor',
            'state', 'city', 'patient_adress', 'zip_code'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }