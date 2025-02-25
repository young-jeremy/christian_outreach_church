from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .forms import MissionForm, ProjectForm, ProjectUpdateForm
from .models import Mission, Project, ProjectUpdate


# Mission Views
class MissionListView(ListView):
    model = Mission
    template_name = 'outreach/mission_list.html'
    context_object_name = 'missions'
    ordering = ['-start_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_missions'] = Mission.objects.filter(status='active')
        context['planned_missions'] = Mission.objects.filter(status='planned')
        return context


class MissionDetailView(DetailView):
    model = Mission
    template_name = 'outreach/mission_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.projects.all()
        return context


class MissionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Mission
    form_class = MissionForm
    template_name = 'outreach/mission_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Mission'
        context['is_edit'] = False
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Mission "{form.instance.title}" has been created successfully.')
        return super().form_valid(form)


class MissionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mission
    form_class = MissionForm
    template_name = 'outreach/mission_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Mission: {self.object.title}'
        context['is_edit'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Mission "{form.instance.title}" has been updated successfully.')
        return super().form_valid(form)


class MissionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mission
    template_name = 'outreach/mission_confirm_delete.html'
    success_url = reverse_lazy('outreach:mission_list')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        mission = self.get_object()
        messages.success(self.request, f'Mission "{mission.title}" has been deleted.')
        return super().delete(request, *args, **kwargs)
