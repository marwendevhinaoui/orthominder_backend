from django.urls import path

from face_detection import views

urlpatterns = [
    path('face', views.face_detection, name='face'),
]
