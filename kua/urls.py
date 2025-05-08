from django import views
from django.urls import path
from django.contrib import admin
from kua.admin import custom_admin_site
from kua.views import admin_dashboard, export_contributions_csv, admin_reports




urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('staff/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('reports/', admin_reports, name='admin_reports'),
    path('staff/export-contributions/', export_contributions_csv, name='export_contributions_csv'),

    # other urls...
]

'''urlpatterns = [
    #path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    #path('reports/', views.admin_reports, name='admin_reports'),
    path('export-contributions/', views.export_contributions_csv, name='export_contributions'),

]'''
