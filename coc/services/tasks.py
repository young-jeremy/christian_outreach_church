from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import BibleStudy, YouthMinistry, ChildrenMinistry
from django.core.mail import send_mail

from django.utils import timezone
from datetime import timedelta
from .models import BibleStudy, YouthMinistry, ChildrenMinistry
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import BibleStudy, YouthMinistry, ChildrenMinistry
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags  # Add this import
from django.utils import timezone
from .models import CoupleProfile, MarriageMinistry, MarriageCounseling


@shared_task
def send_anniversary_reminders():
    today = timezone.now().date()
    couples = CoupleProfile.objects.filter(
        anniversary_reminder=True,
        marriage_date__month=today.month,
        marriage_date__day=today.day
    )

    for couple in couples:
        context = {
            'couple': couple,
            'years': today.year - couple.marriage_date.year
        }

        html_message = render_to_string('services/marriage/email/anniversary_reminder.html', context)

        send_mail(
            subject='Anniversary Reminder',
            message=strip_tags(html_message),
            from_email='noreply@church.com',
            recipient_list=[couple.user1.email, couple.user2.email],
            html_message=html_message
        )


@shared_task
def send_counseling_reminders():
    tomorrow = timezone.now().date() + timezone.timedelta(days=1)
    sessions = MarriageCounseling.objects.filter(
        scheduled_time__date=tomorrow,
        status='scheduled'
    )

    for session in sessions:
        context = {
            'session': session,
            'couple': session.couple
        }

        html_message = render_to_string('services/marriage/email/counseling_reminder.html', context)

        send_mail(
            subject='Counseling Session Reminder',
            message=strip_tags(html_message),
            from_email='noreply@church.com',
            recipient_list=[session.couple.user1.email, session.couple.user2.email],
            html_message=html_message
        )


def clean_inactive_registrations():
    # Your existing task code...
    pass


def send_reminder_emails():
    # Send reminders for upcoming events
    upcoming_studies = BibleStudy.objects.filter(is_active=True)
    for study in upcoming_studies:
        for participant in study.participants.all():
            send_mail(
                'Reminder: Upcoming Bible Study',
                f'Don\'t forget about {study.title} tomorrow!',
                'from@example.com',
                [participant.email],
                fail_silently=False,
            )


def notify_prayer_warriors(prayer_id, update_id):
    """
    Notify all prayer warriors when a prayer request is updated
    """
    from .models import PrayerRequest, PrayerUpdate

    prayer = PrayerRequest.objects.get(id=prayer_id)
    update = PrayerUpdate.objects.get(id=update_id)

    for warrior in prayer.prayer_warriors.all():
        if warrior.email:
            context = {
                'warrior': warrior,
                'prayer': prayer,
                'update': update
            }

            html_message = render_to_string(
                'email/prayer_update_notification.html',
                context
            )

            send_mail(
                subject=f'New Update: {prayer.title}',
                message=strip_tags(html_message),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[warrior.email],
                html_message=html_message
            )


def notify_new_prayer_warrior(prayer_id, warrior_id):
    """
    Notify prayer requester when someone commits to pray
    """
    from .models import PrayerRequest

    prayer = PrayerRequest.objects.get(id=prayer_id)
    warrior = settings.objects.get(id=warrior_id)

    if prayer.requester.email:
        context = {
            'prayer': prayer,
            'warrior': warrior
        }

        html_message = render_to_string(
            'email/new_prayer_warrior_notification.html',
            context
        )

        send_mail(
            subject=f'Someone is Praying for You',
            message=strip_tags(html_message),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[prayer.requester.email],
            html_message=html_message
        )
