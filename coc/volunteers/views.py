from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Opportunity, Volunteer
from .forms import OpportunityForm, VolunteerSignupForm

def opportunity_list(request):
    opportunities = Opportunity.objects.filter(
        date__gte=timezone.now(),
        status='open'
    ).order_by('date')
    return render(request, 'volunteers/opportunity_list.html', {
        'opportunities': opportunities
    })

@login_required
def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    user_signed_up = Volunteer.objects.filter(
        user=request.user,
        opportunity=opportunity
    ).exists()
    
    return render(request, 'volunteers/opportunity_detail.html', {
        'opportunity': opportunity,
        'user_signed_up': user_signed_up
    })

@login_required
def opportunity_create(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save()
            messages.success(request, 'Opportunity created successfully!')
            return redirect('volunteers:opportunity_detail', pk=opportunity.pk)
    else:
        form = OpportunityForm()
    
    return render(request, 'volunteers/opportunity_form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
def opportunity_edit(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    
    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            opportunity = form.save()
            messages.success(request, 'Opportunity updated successfully!')
            return redirect('volunteers:opportunity_detail', pk=opportunity.pk)
    else:
        form = OpportunityForm(instance=opportunity)
    
    return render(request, 'volunteers/opportunity_form.html', {
        'form': form,
        'opportunity': opportunity,
        'action': 'Edit'
    })

@login_required
def volunteer_signup(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    
    # Check if user is already signed up
    if Volunteer.objects.filter(user=request.user, opportunity=opportunity).exists():
        messages.warning(request, 'You are already signed up for this opportunity.')
        return redirect('volunteers:opportunity_detail', pk=pk)
    
    if request.method == 'POST':
        form = VolunteerSignupForm(request.POST)
        if form.is_valid():
            volunteer = form.save(commit=False)
            volunteer.user = request.user
            volunteer.opportunity = opportunity
            volunteer.save()
            messages.success(request, 'Thank you for signing up!')
            return redirect('volunteers:opportunity_detail', pk=pk)
    else:
        form = VolunteerSignupForm()
    
    return render(request, 'volunteers/volunteer_signup.html', {
        'form': form,
        'opportunity': opportunity
    })

@login_required
def volunteer_withdraw(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    signup = get_object_or_404(Volunteer, user=request.user, opportunity=opportunity)
    
    if request.method == 'POST':
        signup.delete()
        messages.success(request, 'You have withdrawn from this opportunity.')
        return redirect('volunteers:opportunity_detail', pk=pk)
    
    return render(request, 'volunteers/volunteer_withdraw.html', {
        'opportunity': opportunity
    }) 