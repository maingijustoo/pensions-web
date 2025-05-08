from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.citizen_register, name='citizen_register'),
    path('login/', views.citizen_login, name='citizen_login'),
    path('logout/', views.citizen_logout, name='citizen_logout'),
    path('dashboard/', views.citizen_dashboard, name='citizen_dashboard'),# Dashboard view will come next!
    path('register/', views.citizen_register, name='citizen_register'),
    path('dashboard/', views.citizen_dashboard, name='citizen_dashboard'),
    path('delete-membership/', views.delete_membership, name='delete_membership'),
    path('search/', views.member_search, name='member_search'),
    path('profile/<int:member_id>/', views.public_member_profile, name='public_member_profile'),
]  


