from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from .models import Podcast


class iTunesPodcastsFeedGenerator(Rss201rev2Feed):
    """
    Custom feed generator that adds iTunes-specific tags
    """

    def root_attributes(self):
        attrs = super().root_attributes()
        attrs['xmlns:itunes'] = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
        return attrs

    def add_root_elements(self, handler):
        super().add_root_elements(handler)

        handler.addQuickElement('itunes:subtitle', self.feed['subtitle'])
        handler.addQuickElement('itunes:author', self.feed['author'])
        handler.addQuickElement('itunes:summary', self.feed['description'])

        handler.startElement('itunes:category', {'text': self.feed['category']})
        handler.endElement('itunes:category')

        handler.addQuickElement('itunes:image', '', {'href': self.feed['image_url']})
        handler.addQuickElement('itunes:explicit', 'no')

    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)

        handler.addQuickElement('itunes:duration', item['duration'])
        handler.addQuickElement('itunes:subtitle', item['subtitle'])
        handler.addQuickElement('itunes:summary', item['description'])
        handler.addQuickElement('itunes:image', '', {'href': item['image_url']})


class PodcastRSSFeed(Feed):
    feed_type = iTunesPodcastsFeedGenerator
    title = "Church Podcast"
    link = "/podcasts/"
    description = "Your church's podcast feed"
    subtitle = "Inspiring messages and teachings"
    author = "Your Church Name"
    category = "Religion & Spirituality"

    def feed_extra_kwargs(self, obj):
        return {
            'subtitle': self.subtitle,
            'author': self.author,
            'category': self.category,
            'image_url': 'https://your-domain.com/static/images/podcast-cover.jpg',  # Update this
        }

    def items(self):
        return Podcast.objects.filter(is_published=True).order_by('-publish_date')[:50]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_extra_kwargs(self, item):
        return {
            'duration': str(item.duration),
            'subtitle': item.subtitle,
            'image_url': item.cover_image.url if item.cover_image else '',
        }

    def item_enclosure_url(self, item):
        return item.audio_file.url

    def item_enclosure_length(self, item):
        return item.file_size

    def item_enclosure_mime_type(self, item):
        return item.audio_type

    def item_pubdate(self, item):
        return item.publish_date

    def item_guid(self, item):
        return str(item.id)

    def item_categories(self, item):
        return [item.get_category_display()]
