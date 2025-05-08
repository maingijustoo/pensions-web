import datetime
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Sum, Count
from django.http import HttpResponse
import csv
from .models import Contributions, Members, Dependents, Payments, Employers
from django.db.models.functions import TruncMonth
from django.contrib.humanize.templatetags.humanize import intcomma
from .forms import AdminAddDependentForm
from django.shortcuts import render
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta 

def admin_dashboard(request):
    # Basic Stats
    total_contributions = Contributions.objects.count()
    total_amount_contributed = Contributions.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_payments = Payments.objects.count()
    total_amount_paid = Payments.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_members = Members.objects.count()
    total_dependents = Dependents.objects.count()
    total_employers = Employers.objects.count()
    active_employers = Employers.objects.filter(contributions__isnull=False).distinct().count()

    # Monthly contributions data for line chart
    monthly_data = (
        Contributions.objects
        .annotate(month=TruncMonth('contributiondate'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    months = [entry['month'].strftime('%Y-%m') for entry in monthly_data]
    totals = [float(entry['total']) for entry in monthly_data]

    # Payment methods distribution for doughnut chart
    payment_methods = (
        Contributions.objects
        .values('paymentmethod')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    payment_methods_labels = [method['paymentmethod'] for method in payment_methods]
    payment_methods_data = [float(method['total']) for method in payment_methods]

    # Recent contributions for table
    recent_contributions = (
        Contributions.objects
        .select_related('memberid', 'employerid')
        .order_by('-contributiondate')[:10]
    )

    # Handle dependent addition if form submitted
    form = None
    if request.method == 'POST' and 'add_dependent' in request.POST:
        form = AdminAddDependentForm(request.POST)
        if form.is_valid():
            member_id = request.POST.get('member_id')
            member = get_object_or_404(Members, id=member_id)
            dependent = form.save(commit=False)
            dependent.memberid = member
            dependent.save()
            messages.success(request, f'Dependent {dependent.dependentname} added successfully!')
            return redirect('admin_dashboard')
    
    # Initialize form if not already created from POST
    form = form or AdminAddDependentForm()
    
    context = {
        # Basic stats
        'total_contributions': total_contributions,
        'total_amount_contributed': total_amount_contributed,
        'total_payments': total_payments,
        'total_amount_paid': total_amount_paid,
        'total_members': total_members,
        'total_dependents': total_dependents,
        'total_employers': total_employers,
        'active_employers': active_employers,
        
        # Chart data
        'months': months,
        'totals': totals,
        'payment_methods_labels': payment_methods_labels,
        'payment_methods_data': payment_methods_data,
        
        # Recent data
        'recent_contributions': recent_contributions,
        'recent_members': Members.objects.order_by('-registrationdate')[:10],
        
        # Forms
        'add_dependent_form': form,
        
        # Formatting helpers
        'intcomma': intcomma,
    }

    return render(request, 'admin/dashboard.html', context)


def admin_reports(request):
    # Date filters
    today = datetime.now().date()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    # Contribution reports
    contributions_all = Contributions.objects.all()
    contributions_week = contributions_all.filter(contributiondate__gte=last_week)
    contributions_month = contributions_all.filter(contributiondate__gte=last_month)
    
    # Payment reports
    payments_all = Payments.objects.all()
    payments_week = payments_all.filter(paymentdate__gte=last_week)
    payments_month = payments_all.filter(paymentdate__gte=last_month)
    
    # Member reports
    members_all = Members.objects.all()
    new_members_week = members_all.filter(registrationdate__gte=last_week)
    new_members_month = members_all.filter(registrationdate__gte=last_month)
    
    # Employer reports
    employers_all = Employers.objects.all()
    active_employers = employers_all.filter(contributions__isnull=False).distinct()
    
    # Prepare report data
    reports = {
        'contributions': {
            'total': contributions_all.count(),
            'week': contributions_week.count(),
            'month': contributions_month.count(),
            'total_amount': contributions_all.aggregate(Sum('amount'))['amount__sum'] or 0,
            'week_amount': contributions_week.aggregate(Sum('amount'))['amount__sum'] or 0,
            'month_amount': contributions_month.aggregate(Sum('amount'))['amount__sum'] or 0,
        },
        'payments': {
            'total': payments_all.count(),
            'week': payments_week.count(),
            'month': payments_month.count(),
            'total_amount': payments_all.aggregate(Sum('amount'))['amount__sum'] or 0,
            'week_amount': payments_week.aggregate(Sum('amount'))['amount__sum'] or 0,
            'month_amount': payments_month.aggregate(Sum('amount'))['amount__sum'] or 0,
        },
        'members': {
            'total': members_all.count(),
            'week': new_members_week.count(),
            'month': new_members_month.count(),
            'employed': members_all.filter(employmentstatus='Employed').count(),
            'self_employed': members_all.filter(employmentstatus='Self-Employed').count(),
            'unemployed': members_all.filter(employmentstatus='Unemployed').count(),
        },
        'employers': {
            'total': employers_all.count(),
            'active': active_employers.count(),
            'inactive': employers_all.count() - active_employers.count(),
        }
    }
    
    # Top 10 lists
    top_lists = {
        'top_contributors': contributions_all.values(
            'memberid__fullname'
        ).annotate(
            total=Sum('amount'),
            count=Count('contributionid')
        ).order_by('-total')[:10],
        
        'top_employers': contributions_all.values(
            'employerid__employername'
        ).annotate(
            total=Sum('amount'),
            count=Count('contributionid')
        ).order_by('-total')[:10],
        
        'recent_contributions': contributions_all.select_related(
            'memberid', 'employerid'
        ).order_by('-contributiondate')[:10],
        
        'recent_payments': payments_all.select_related(
            'memberid'
        ).order_by('-paymentdate')[:10],
    }
    
    context = {
        'reports': reports,
        'top_lists': top_lists,
        'today': today,
        'last_week': last_week,
        'last_month': last_month,
    }
    
    return render(request, 'admin/reports.html', context)

def export_contributions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contributions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Member', 'Employer', 'Date', 'Amount', 'Payment Method'])

    contributions = Contributions.objects.select_related('memberid', 'employerid').order_by('-contributiondate')
    
    for contribution in contributions:
        writer.writerow([
            contribution.memberid.fullname if contribution.memberid else '',
            contribution.employerid.employername if contribution.employerid else 'N/A',
            contribution.contributiondate.strftime('%Y-%m-%d'),
            contribution.amount,
            contribution.paymentmethod
        ])

    return response

