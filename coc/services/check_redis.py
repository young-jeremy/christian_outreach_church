from django.core.management.base import BaseCommand
from utils.redis import check_redis_connection


class Command(BaseCommand):
    help = 'Check Redis connection status'

    def handle(self, *args, **kwargs):
        if check_redis_connection():
            self.stdout.write(self.style.SUCCESS('Redis connection successful'))
        else:
            self.stdout.write(self.style.ERROR('Redis connection failed'))
