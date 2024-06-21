from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path('user_login', views.user_login, name="user_login"),
    path('user_registration', views.user_registration, name="user_registration"),
    path('user_logout', views.user_logout, name="user_logout"),
    path('houses/<int:street_id>/<int:user_id>', views.houses, name="houses"),
    path('user_request', views.user_request, name="user_request"),
    path('delete_request/<int:req_id>', views.delete_request, name="delete_request"),
    path('reg_hwo', views.reg_hwo, name="reg_hwo"), 
]