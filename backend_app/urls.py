from django.urls import path
from .views import shared_views, doctor_views, patient_view


urlpatterns = [
    #doctor URL
    path('doctor/register', doctor_views.register_doctor, name='register_doctor'),
    path('doctor/login', doctor_views.login_doctor, name='login_doctor'),
    path('get_doctor', doctor_views.get_doctor_data, name='get_doctor'),
    path('get_doctor_id_from_refresh', doctor_views.get_doctor_id_from_refresh, name='get_doctor_id_from_refresh'),
    path('delete_doctor/<int:doctor_id>', doctor_views.delete_doctor, name='delete_doctor'),


    #patient URL
    path('patient/register', patient_view.register_patient, name='register_patient'),
    path('patient/login', patient_view.login_patient, name='login_patient'),


    #shared URL
    path('ref', shared_views.refresh_token, name='refresh_token'),
    path('logout', shared_views.logout, name='logout'),
    
]
