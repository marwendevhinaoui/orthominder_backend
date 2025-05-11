from django.urls import path
from .views import shared_views, doctor_views


urlpatterns = [
    #doctor URL
    path('register/doctor', doctor_views.register_doctor, name='register'),
    path('login/', doctor_views.login_doctor, name='login'),
    path('get_doctor/', doctor_views.get_doctor_data, name='get_doctor'),
    # path('get_doctor/<int:get_doctor>', doctor_views.get_doctor_data, name='get_doctor'),


    #patient URL
    # path('login/patient', patient_views.login_patient, name='login_patient'),


    #shared URL
    path('logout/', shared_views.logout, name='logout'),
    path('ref/', shared_views.refresh_token, name='refresh_token'),
    path('blacklisting/', shared_views.blacklisting, name='user_blacklisting'), #api ya3mel blacklist lel user fih mochkla mba3d gadih
    
]
