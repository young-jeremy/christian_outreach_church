from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CounselingRequestForm
from .models import CounselingRequest


def counseling_request(request):
    if request.method == 'POST':
        form = CounselingRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your counseling request has been submitted successfully.')
            return redirect('counseling_request')
    else:
        form = CounselingRequestForm()

    return render(request, 'counseling/counseling_request_form.html', {'form': form})
