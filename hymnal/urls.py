from django.urls import path
from . import views

app_name = 'hymnal'

urlpatterns = [
    path('', views.hymnal_home, name='home'),
    path('search/', views.search_hymn, name='search'),
]