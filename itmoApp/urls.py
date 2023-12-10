from django.urls import path
from . import views

urlpatterns = [
    path('learn-model/', views.upload_model, name='learn_model'),
    path('predict/', views.model_selection_view, name='predict')
]