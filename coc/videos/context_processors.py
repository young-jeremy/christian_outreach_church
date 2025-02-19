from django.db.models import Count
from .models import Video

def video_counts(request):
    """
    Context processor to add video counts to all templates.
    Returns video counts for authenticated users:
    - total_videos: Number of videos uploaded by the user
    - total_likes: Number of videos liked by the user
    """
    if request.user.is_authenticated:
        return {
            'total_videos': Video.objects.filter(uploader=request.user).count(),
            'total_likes': Video.objects.filter(likes=request.user).count(),
        }
    return {
        'total_videos': 0,
        'total_likes': 0,
    }