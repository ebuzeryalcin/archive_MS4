from django.urls import path
from . import views

# The root url
urlpatterns = [
    path('', views.index, name='home')
]