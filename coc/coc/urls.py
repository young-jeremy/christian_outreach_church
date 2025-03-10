from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('account/', include('django.contrib.auth.urls')),
    path("", include("videos.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("accounts/", include("accounts.urls")),
    path("blog/", include("blog.urls")),
    path('education/', include('education.urls')),
    path("products/", include("products.urls")),
    path("services/", include("services.urls")),
    path("account/", include("allauth.urls")),
    path("social-auth/", include("social_django.urls", namespace="social")),
    # E
    path("events/", include("events.urls")),
    path("home/", include("home.urls")),
    path("comments/", include("comments.urls")),
    path("notifications/", include("notifications.urls")),
    path("payments/", include("payments.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("volunteers/", include("volunteers.urls", namespace="volunteers")),
    path('resources/', include('resources.urls')),
    path('outreach/', include('outreach.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Christian Outreach Church Admin"
admin.site.site_title = "Welcome to the Hub of Gospel"
admin.site.index_title = "Welcome to Christian Outreach Church Admin System"
