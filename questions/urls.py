from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('ask/', views.submit_question, name='submit'),
    path('questions/', views.view_questions, name='list'),
]