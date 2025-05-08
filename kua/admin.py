from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib import admin
from .models import Members, Employers, Contributions, Payments, Dependents
from kua import models


@admin.register(Employers)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('employerid', 'employername', 'employerkrapin', 'contactperson', 'contactemail', 'contactphone')
    search_fields = ('employername', 'employerkrapin', 'contactemail')
    list_filter = ('employername',)

@admin.register(Members)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('memberid', 'fullname', 'email', 'contactnumber', 'employerid', 'employmentstatus')
    search_fields = ('fullname', 'email', 'krapin', 'nssfcardnumber')
    list_filter = ('employmentstatus', 'employerid')

@admin.register(Contributions)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('contributionid', 'memberid', 'employerid', 'contributiondate', 'amount', 'paymentmethod')
    search_fields = ('memberid__fullname',)
    list_filter = ('paymentmethod', 'contributiondate')

@admin.register(Dependents)
class DependentAdmin(admin.ModelAdmin):
    list_display = ('dependentid', 'memberid', 'dependentname', 'relationship', 'dateofbirth')
    search_fields = ('dependentname', 'memberid__fullname')

@admin.register(Payments)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('paymentid', 'memberid', 'paymentdate', 'amount', 'paymenttype', 'processedby')
    search_fields = ('memberid__fullname',)
    list_filter = ('paymenttype', 'paymentdate')

class CustomAdminSite(admin.AdminSite):
    site_header = 'Pension Management System - Staff Dashboard'
    site_title = 'Pension Admin'
    index_title = 'Welcome to the Staff Dashboard'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Sample data aggregation
        total_contributions = Contributions.objects.all().count()
        total_payments = Payments.objects.all().count()
        total_amount_contributed = Contributions.objects.all().aggregate(models.Sum('amount'))['amount__sum'] or 0
        total_amount_paid = Payments.objects.all().aggregate(models.Sum('amount'))['amount__sum'] or 0

        context = dict(
            self.each_context(request),
            total_contributions=total_contributions,
            total_payments=total_payments,
            total_amount_contributed=total_amount_contributed,
            total_amount_paid=total_amount_paid,
        )
        return TemplateResponse(request, "admin/dashboard.html", context)

# Use the custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')