import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Topic, Post

class ForumConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.topic_id = self.scope['url_route']['kwargs']['topic_id']
        self.topic_group_name = f'topic_{self.topic_id}'

        # Join topic group
        await self.channel_layer.group_add(
            self.topic_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave topic group
        await self.channel_layer.group_discard(
            self.topic_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to topic group
        await self.channel_layer.group_send(
            self.topic_group_name,
            {
                'type': 'topic_message',
                'message': message
            }
        )

    async def topic_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))