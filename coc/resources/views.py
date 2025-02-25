from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.feeds import Feed
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import DailyDevotionForm
from .models import *
from .models import Artist
from .models import ChristianBook, BookReview, ReadingList
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import Book
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SermonNotes
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import TeachingResource
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Podcast
import json
from django.http import FileResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404


class CounselingResourceListView(ListView):
    template_name = 'resources/downloadable/counseling_resources.html'
    context_object_name = 'resources'
    paginate_by = 12

    def get_queryset(self):
        queryset = DownloadableResource.objects.filter(category='CNS')

        # Filter by type
        resource_type = self.request.GET.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)

        # Search functionality
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(tags__icontains=q)
            )

        # Access control for sensitive materials
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_public=True, requires_login=False)
        elif not self.request.user.is_staff:
            public_resources = Q(is_public=True)
            user_groups = Q(allowed_groups__in=self.request.user.groups.all())
            queryset = queryset.filter(public_resources | user_groups).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_types'] = dict(DownloadableResource.RESOURCE_TYPES)
        context['featured_resources'] = DownloadableResource.objects.filter(
            category='CNS', featured=True
        )[:3]
        return context


class DownloadableResourceListView(ListView):
    model = DownloadableResource
    template_name = 'resources/downloadable/downloadable_list.html'
    context_object_name = 'resources'
    paginate_by = 12

    def get_queryset(self):
        queryset = DownloadableResource.objects.all()

        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        # Filter by type
        resource_type = self.request.GET.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)

        # Search
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(tags__icontains=q)
            )

        # Access control
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_public=True, requires_login=False)
        elif not self.request.user.is_staff:
            public_resources = Q(is_public=True)
            user_groups = Q(allowed_groups__in=self.request.user.groups.all())
            queryset = queryset.filter(public_resources | user_groups).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = dict(DownloadableResource.CATEGORIES)
        context['resource_types'] = dict(DownloadableResource.RESOURCE_TYPES)
        context['featured_resources'] = DownloadableResource.objects.filter(featured=True)[:3]
        return context


class DownloadResourceView(View):
    def get(self, request, pk):
        resource = get_object_or_404(DownloadableResource, pk=pk)

        # Check permissions
        if not resource.can_user_download(request.user):
            raise Http404("You don't have permission to download this file")

        # Track download
        resource.increment_downloads()

        # Serve file
        response = FileResponse(resource.file, as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{resource.file.name}"'
        return response


class PodcastListView(ListView):
    model = Podcast
    template_name = 'resources/podcast/podcast_list.html'
    context_object_name = 'episodes'
    paginate_by = 12

    def get_queryset(self):
        queryset = Podcast.objects.filter(is_published=True)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_episodes'] = Podcast.objects.filter(
            is_featured=True, is_published=True
        )[:3]
        context['categories'] = dict(Podcast.PODCAST_CATEGORIES)
        return context


class PodcastDetailView(DetailView):
    model = Podcast
    template_name = 'resources/podcast/podcast_detail.html'
    context_object_name = 'episode'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_episodes'] = Podcast.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context


@method_decorator(csrf_exempt, name='dispatch')
class PodcastAnalyticsView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            episode_id = data.get('episode_id')
            action = data.get('action')

            episode = Podcast.objects.get(id=episode_id)

            if action == 'play':
                episode.increment_play_count()
            elif action == 'download':
                episode.increment_download_count()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


# RSS Feed for podcast platforms
class PodcastRSSFeed(Feed):
    title = "Church Podcast"
    link = "/podcasts/"
    description = "Your church's podcast feed"

    def items(self):
        return Podcast.objects.filter(is_published=True).order_by('-publish_date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_enclosure_url(self, item):
        return item.audio_file.url

    def item_enclosure_length(self, item):
        return item.file_size

    def item_enclosure_mime_type(self, item):
        return item.audio_type


class TeachingResourceListView(ListView):
    model = TeachingResource
    template_name = 'resources/teaching_resources/teaching_resources.html'
    context_object_name = 'resources'
    paginate_by = 12

    def get_queryset(self):
        queryset = TeachingResource.objects.all()

        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        # Filter by type
        resource_type = self.request.GET.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)

        # Search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(tags__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = dict(TeachingResource.CATEGORIES)
        context['resource_types'] = dict(TeachingResource.RESOURCE_TYPES)
        context['featured_resources'] = TeachingResource.objects.filter(is_featured=True)[:3]
        return context


class TeachingResourceDetailView(DetailView):
    model = TeachingResource
    template_name = 'resources/teaching_resources/teaching_resource_detail.html'
    context_object_name = 'resource'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related resources
        context['related_resources'] = TeachingResource.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context


class SermonListView(ListView):
    model = SermonNotes
    template_name = 'services/sermon/sermon_list.html'
    context_object_name = 'sermons'
    paginate_by = 10
    ordering = ['-date_preached']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_sermons'] = SermonNotes.objects.filter(is_featured=True)[:3]
        context['categories'] = dict(SermonNotes.SERMON_CATEGORIES)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset


class SermonDetailView(DetailView):
    model = SermonNotes
    template_name = 'resources/sermon/sermon_notes.html'
    context_object_name = 'sermon'


class BookDetailView(DetailView):
    model = ChristianBook
    template_name = 'resources/christian_books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.bookreview_set.all()[:5]
        if self.request.user.is_authenticated:
            context['user_review'] = self.object.bookreview_set.filter(
                user=self.request.user
            ).first()
        return context


class AddToReadingListView(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        list_id = request.POST.get('list_id')

        book = get_object_or_404(ChristianBook, pk=book_id)
        reading_list = get_object_or_404(ReadingList, pk=list_id, user=request.user)

        reading_list.books.add(book)

        return JsonResponse({
            'status': 'success',
            'message': f'Added {book.title} to {reading_list.name}'
        })


class BookReviewCreateView(LoginRequiredMixin, CreateView):
    model = BookReview
    fields = ['rating', 'review_text']
    template_name = 'resources/christian_books/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book = get_object_or_404(ChristianBook, pk=self.kwargs['pk'])
        return super().form_valid(form)




class BibleStudyMaterialListView(LoginRequiredMixin, ListView):
    model = BibleStudyMaterial
    template_name = 'resources/bible_study/list.html'
    context_object_name = 'materials'

class BibleStudyMaterialDetailView(LoginRequiredMixin, DetailView):
    model = BibleStudyMaterial
    template_name = 'resources/bible_study/detail.html'
    context_object_name = 'material'


class BibleStudyMaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = BibleStudyMaterial
    template_name = 'resources/bible_study/confirm_delete.html'
    success_url = reverse_lazy('resources:bible-study-list')


class DailyDevotionListView(ListView):
    model = DailyDevotion
    template_name = 'resources/daily_devotions/list.html'
    context_object_name = 'devotions'
    paginate_by = 10


class DailyDevotionDetailView(DetailView):
    model = DailyDevotion
    template_name = 'resources/daily_devotions/detail.html'
    context_object_name = 'devotion'


class DailyDevotionCreateView(LoginRequiredMixin, CreateView):
    model = DailyDevotion
    form_class = DailyDevotionForm
    template_name = 'resources/daily_devotions/form.html'
    success_url = reverse_lazy('resources:devotion-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DailyDevotionUpdateView(LoginRequiredMixin, UpdateView):
    model = DailyDevotion
    form_class = DailyDevotionForm
    template_name = 'resources/daily_devotions/form.html'
    success_url = reverse_lazy('resources:devotion-list')


class DailyDevotionDeleteView(LoginRequiredMixin, DeleteView):
    model = DailyDevotion
    template_name = 'resources/daily_devotions/confirm_delete.html'
    success_url = reverse_lazy('resources:devotion-list')


class ArtistListView(ListView):
    model = Artist
    template_name = 'resources/music/artist_list.html'
    context_object_name = 'artists'
    paginate_by = 12


class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'resources/music/artist_detail.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = self.object.albums.all()
        context['songs'] = self.object.songs.all()
        return context


class BibleStudyListView(ListView):
    model = BibleStudy
    template_name = 'resources/bible_study/list.html'
    context_object_name = 'bible_studies'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        study_type = self.request.GET.get('type')
        search = self.request.GET.get('search')

        if study_type:
            queryset = queryset.filter(study_type=study_type)
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset.order_by('-created_at')


class BibleStudyDetailView(DetailView):
    model = BibleStudy
    template_name = 'resources/bible_study/detail.html'
    context_object_name = 'bible_study'


class BibleStudyCreateView(LoginRequiredMixin, CreateView):
    model = BibleStudy
    template_name = 'resources/bible_study/form.html'
    fields = ['title', 'description', 'study_type', 'scripture_reference',
              'start_date', 'end_date', 'materials', 'video_link']
    success_url = reverse_lazy('bible_study_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@login_required
@require_POST
def toggle_helpful_vote(request, review_id):
    review = get_object_or_404(ReviewableMixin, id=review_id)
    user = request.user

    if user == review.user:
        return JsonResponse({
            'status': 'error',
            'message': 'You cannot vote on your own review'
        }, status=400)

    if user in review.helpful_votes.all():
        review.unmark_as_helpful(user)
        is_helpful = False
    else:
        review.mark_as_helpful(user)
        is_helpful = True

    return JsonResponse({
        'status': 'success',
        'helpful_count': review.helpful_votes_count,
        'is_helpful': is_helpful
    })




class BookListView(ListView):
    model = Book
    template_name = 'resources/christian_books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        queryset = Book.objects.filter(is_active=True)
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__name__icontains=search) |
                Q(description__icontains=search)
            )
        if category:
            queryset = queryset.filter(category=category)

        return queryset.order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Book.CATEGORY_CHOICES
        context['current_category'] = self.request.GET.get('category', '')
        context['search_term'] = self.request.GET.get('search', '')
        return context


class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    template_name = 'resources/christian_books/book_form.html'
    fields = ['title', 'author', 'category', 'description', 'cover_image',
              'publication_date', 'isbn', 'publisher']

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Book created successfully!')
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    template_name = 'resources/christian_books/book_form.html'
    fields = ['title', 'author', 'category', 'description', 'cover_image',
              'publication_date', 'isbn', 'publisher', 'is_active']

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'resources/christian_books/book_confirm_delete.html'
    success_url = reverse_lazy('resources:book_list')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Book deleted successfully!')
        return super().delete(request, *args, **kwargs)
