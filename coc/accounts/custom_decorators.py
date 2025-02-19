from django.shortcuts import redirect

from .models import UserProfile
from django.contrib import messages

def channel_verified_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            try:
                channel = user.profile.channel_id
                if channel == 'verified':
                    return view_func(request, *args, **kwargs)
            except UserProfile.DoesNotExist:
                messages.error('You should verify your channel before uploading videos')

        return redirect('videos:upload_video')  # You can redirect to a different URL or show an error message
    return _wrapped_view
