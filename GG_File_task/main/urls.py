from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    #path('', views.home, name='home'),
    #path('files/', views.file_list, name='file_list'),
    #path('files/<str:file_name>/download/', views.file_download, name='file_download'),
    #path('files/<str:file_name>/open/', views.file_open, name='file_open'),
]
