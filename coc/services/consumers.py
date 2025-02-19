from channels.generic.websocket import AsyncWebsocketConsumer
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


class BibleStudyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.study_id = self.scope['url_route']['kwargs']['study_id']
        self.room_group_name = f'study_{self.study_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'study_message',
                'message': message
            }
        )

    async def study_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


class PrayerRequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(
            f"user_{self.user.id}_prayers",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"user_{self.user.id}_prayers",
            self.channel_name
        )

    async def prayer_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "prayer.update",
            "prayer_id": event["prayer_id"],
            "message": event["message"]
        }))

    async def new_prayer_warrior(self, event):
        await self.send(text_data=json.dumps({
            "type": "prayer.warrior",
            "prayer_id": event["prayer_id"],
            "warrior_name": event["warrior_name"],
            "count": event["count"]
        }))
