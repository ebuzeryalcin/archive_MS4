from django.urls import path
from . import views

# The root url
urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<book_id>/', views.add_to_bag, name='add_to_bag'),
]