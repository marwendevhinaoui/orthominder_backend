from django.urls import include, path
from .views import shared_views, doctor_views, patient_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #doctor URL
    path('doctor/register', doctor_views.register_doctor, name='register_doctor'),
    path('doctor/login', doctor_views.login_doctor, name='login_doctor'),
    path('get_doctor', doctor_views.get_doctor_data, name='get_doctor'),
    path('get_doctor_id_from_refresh', doctor_views.get_doctor_id_from_refresh, name='get_doctor_id_from_refresh'),
    # path('delete_doctor/<int:doctor_id>', doctor_views.delete_doctor, name='delete_doctor'),
    path('get_all_appointements', doctor_views.get_all_appointements, name='get_all_appointements'),
    path('get_all_patient', doctor_views.get_all_patient, name='get_all_patient'),


    #patient URL
    path('patient/register', patient_view.register_patient, name='register_patient'),
    path('patient/login', patient_view.login_patient, name='login_patient'),
    path('add_appointement', patient_view.add_appointement, name='add_appointement'),
    path('add_aligner', patient_view.add_aligner, name='add_aligner'),
    path('get_appointements_by_patient_id/<int:patient_id>', patient_view.get_appointements_by_patient_id, name='get_appointements_by_patient_id'),
    path('get_patient_by_id/<int:patient_id>', patient_view.get_patient_by_id, name='get_patient_by_id'),
    path('get_appointements_details/<int:appointement_id>', patient_view.get_appointements_details, name='get_appointements_details'),
    path('get_appointements_details_by_patient/<int:patient_id>', patient_view.get_appointements_details_by_patient, name='get_appointements_details_by_patient'),


    #shared URL
    path('ref', shared_views.refresh_token, name='refresh_token'),
    path('logout', shared_views.logout, name='logout'),
    path('detect/', include('face_detection.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
