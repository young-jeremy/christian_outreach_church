from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/prayer/(?P<prayer_id>\w+)/$', consumers.PrayerRequestConsumer.as_asgi()),
]
