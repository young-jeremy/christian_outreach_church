from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Topic, Post

@registry.register_document
class TopicDocument(Document):
    title = fields.TextField()
    content = fields.TextField()
    category = fields.ObjectField(properties={
        'name': fields.TextField(),
        'slug': fields.TextField(),
    })
    creator = fields.ObjectField(properties={
        'username': fields.TextField(),
    })
    created_at = fields.DateField()

    class Index:
        name = 'topics'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Topic
        fields = [
            'id',
            'slug',
            'views',
        ]