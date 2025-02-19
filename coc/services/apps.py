from django.apps import AppConfig
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils import timezone


class MinistriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ministries'

    def ready(self):
        try:
            from django_celery_beat.models import PeriodicTask, IntervalSchedule

            # Create daily schedule
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.DAYS,
            )

            # Create reminder task
            PeriodicTask.objects.get_or_create(
                name='Send Event Reminders',
                task='ministries.tasks.send_reminder_emails',
                interval=schedule,
                start_time=timezone.now()
            )

            # Create cleanup task
            PeriodicTask.objects.get_or_create(
                name='Clean Inactive Registrations',
                task='ministries.tasks.clean_inactive_registrations',
                interval=schedule,
                start_time=timezone.now()
            )
        except:
            pass

class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services'
