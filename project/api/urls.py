from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/generate', views.generate, name='generate'),
    path('api/v1/download', views.download, name='download'),
    path('api/v1/send_mq', views.download, name='send_mq'),
]