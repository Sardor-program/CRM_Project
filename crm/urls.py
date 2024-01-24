from django.urls import path
from .views import home, logout_user, register_user, customer_record, delete_record, add_record, update_record

urlpatterns = [
    path('', home, name='home'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('record/<int:pk>/', customer_record, name='record'),
    path('delete_record/<int:pk>/', delete_record, name='delete_record'),
    path('add_record/', add_record, name='add'),
    path('update_record/<int:pk>/', update_record, name='update_record'),


]
