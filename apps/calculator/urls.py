from django.urls import path
from apps.calculator import views

app_name = 'calculator'

urlpatterns = [
    path('', views.index, name='index'),
    path('calculate/', views.calculate, name='calculate'),
    path('compare/', views.compare_methods, name='compare'),
    path('export/', views.export_results, name='export'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
]