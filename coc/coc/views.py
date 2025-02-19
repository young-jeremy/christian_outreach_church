from django.views.generic import TemplateView
from django.db.models import Count
from members.models import Member
from events.models import Event
from outreach.models import OutreachProgram
from resources.models import Resource


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_members'] = Member.objects.count()
        context['upcoming_events'] = Event.objects.filter(date__gte=timezone.now()).count()
        context['active_outreach_programs'] = OutreachProgram.objects.filter(is_active=True).count()
        context['total_resources'] = Resource.objects.count()
        return context
