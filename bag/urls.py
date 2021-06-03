from django.urls import path
from . import views

# The root url
urlpatterns = [
    path('', views.view_bag, name='view_bag')
]