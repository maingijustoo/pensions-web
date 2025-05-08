from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django import forms
from kua import models
from .forms import CitizenRegistrationForm
from kua.models import Members
from django.contrib.auth.decorators import login_required
from kua.models import Contributions, Dependents
from django.shortcuts import render, redirect
from django.contrib.auth.backends import ModelBackend

def citizen_register(request):
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('citizen_login')
    else:
        form = CitizenRegistrationForm()
    return render(request, 'citizens/register.html', {'form': form})


class MembersBackend(ModelBackend):
    def authenticate(self, request, email=None):
        try:
            return Members.objects.get(email=email)
        except Members.DoesNotExist:
            return None
"""
def citizen_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = Members.objects.get(email=username)  # or email=username
        except Members.DoesNotExist:
            user = None

        if user and check_password(password, user.password):
            # ✅ Set backend manually
            backend = get_backends()[0]
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            
            login(request, user)  # manually log in the user
            messages.success(request, "Login successful.")
            return redirect('citizen_dashboard')  # or your dashboard route
        else:
            messages.error(request, "Invalid login credentials.")

    return render(request, 'citizens/login.html')
"""


def citizen_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Try to get the member with this email
        try:
            user = Members.objects.get(email=email)

            # Set session manually since it's a custom user model
            request.session['member_id'] = user.id
            request.session['member_name'] = user.fullname  # optional: store name for later

            #return redirect('citizen_dashboard')
            return render(request, 'citizen/dashboard.html', {'member': user})

        except Members.DoesNotExist:
            error = 'No member found with this email.'
            return render(request, 'citizens/login.html', {'error': error})

    return render(request, 'citizens/login.html')



"""def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful! Welcome back.')
            return redirect('citizen_dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'login.html')

    def citizen_login(request):
    if request.method == 'POST':
        username = request.POST['username']  # this is your email field

        try:
            user = Members.objects.get(email=username)
            login(request, user)  # manually log in the user
            messages.success(request, 'Login successful! Welcome back.')
            return redirect('citizen_dashboard')
        except Members.DoesNotExist:
            messages.error(request, 'Invalid username or password. TRY AGAIN')

    return render(request, 'citizens/login.html')

    """

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Sum, Count
from kua.models import Contributions, Members, Dependents
#from kua.forms import AddDependentForm
from django import forms
import logging

logger = logging.getLogger(__name__)

# Public Member Search Views
def member_search(request):
    """Public search page for members to find their profile"""
    if request.method == 'POST':
        search_term = request.POST.get('search_term', '').strip()
        search_type = request.POST.get('search_type', 'id')
        
        try:
            if search_type == 'id':
                member = Members.objects.get(id=search_term)
            elif search_type == 'nssf':
                member = Members.objects.get(nssfcardnumber=search_term)
            elif search_type == 'kra':
                member = Members.objects.get(krapin=search_term)
            else:
                member = None
            
            if member:
                return redirect('public_member_profile', member_id=member.id)
        
        except Members.DoesNotExist:
            return render(request, 'public/member_search.html', {
                'error': 'No member found with those details',
                'search_term': search_term,
                'search_type': search_type
            })
        except Exception as e:
            logger.error(f"Member search error: {e}")
            return render(request, 'public/member_search.html', {
                'error': 'An error occurred during search'
            })
    
    return render(request, 'public/member_search.html')

def public_member_profile(request, member_id):
    """Public view of member profile without authentication"""
    member = get_object_or_404(Members, id=member_id)
    
    # Basic stats (limited info for public view)
    total_contributions = Contributions.objects.filter(
        memberid=member
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_dependents = Dependents.objects.filter(
        memberid=member
    ).count()
    
    # Limited contributions list (last 3 only)
    contributions = Contributions.objects.filter(
        memberid=member
    ).order_by('-contributiondate')[:3]
    
    context = {
        'member': member,
        'total_contributions': total_contributions,
        'total_dependents': total_dependents,
        'contributions': contributions,
        'is_public_view': True  # Flag for template
    }
    return render(request, 'admin/member_profile.html', context)

# Authenticated Member Views
def citizen_logout(request):
    logout(request)
    return redirect('member_search')  # Redirect to public search after logout

@login_required
def citizen_dashboard(request):
    """Authenticated member dashboard with full details"""
    try:
        member = Members.objects.get(email=request.user.username)
        
        # Full stats
        total_contributions = Contributions.objects.filter(
            memberid=member
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_dependents = Dependents.objects.filter(
            memberid=member
        ).count()
        
        # Full contributions list
        contributions = Contributions.objects.filter(
            memberid=member
        ).order_by('-contributiondate')
        
        eligible = total_contributions >= 2  # Example eligibility criteria
        dependents = Dependents.objects.filter(memberid=member)

        context = {
            'member': member,
            'total_contributions': total_contributions,
            'total_dependents': total_dependents,
            'contributions': contributions,
            'eligible': eligible,
            'dependents': dependents,
            'is_public_view': False
        }
        return render(request, 'member/dashboard.html', context)
    
    except Members.DoesNotExist:
        logger.error(f"No member found for user {request.user.username}")
        logout(request)
        return redirect('member_search')
'''
@login_required
def add_dependent(request):
    """Authenticated view for adding dependents"""
    member = get_object_or_404(Members, email=request.user.username)
    
    if request.method == 'POST':
        form = AddDependentForm(request.POST)
        if form.is_valid():
            dependent = form.save(commit=False)
            dependent.memberid = member
            dependent.save()
            return redirect('citizen_dashboard')
    else:
        form = AddDependentForm()

    return render(request, 'member/add_dependent.html', {
        'form': form,
        'member': member
    })

'''

@login_required
def delete_membership(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('citizen_login')

    return render(request, 'citizens/delete_membership.html')
