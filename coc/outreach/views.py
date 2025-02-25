from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from .forms import *

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Mission, Project, ProjectUpdate
from .forms import MissionForm, ProjectForm, ProjectUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Mission, Project, ProjectUpdate
from .forms import MissionForm, ProjectForm, ProjectUpdateForm
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Mission
from .forms import MissionForm

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Mission, Project, ProjectUpdate
from .forms import MissionForm, ProjectForm, ProjectUpdateForm
# Add to your existing views.py
from django.http import FileResponse
from django.db.models import F, Q


class ToolListView(ListView):
    model = EvangelismTool
    template_name = 'outreach/evangelism_tools/tool_list.html'
    context_object_name = 'tools'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = dict(EvangelismTool.CATEGORY_CHOICES)
        context['featured_tools'] = EvangelismTool.objects.filter(is_featured=True)[:4]
        return context

    def get_queryset(self):
        queryset = EvangelismTool.objects.all()
        category = self.request.GET.get('category')
        language = self.request.GET.get('language')
        search = self.request.GET.get('search')

        if category:
            queryset = queryset.filter(category=category)
        if language:
            queryset = queryset.filter(language=language)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(author__icontains=search)
            )
        return queryset


class ToolDetailView(DetailView):
    model = EvangelismTool
    template_name = 'outreach/evangelism_tools/tool_detail.html'
    context_object_name = 'tool'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_tools'] = EvangelismTool.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context


class ToolCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = EvangelismTool
    template_name = 'outreach/evangelism_tools/tool_form.html'
    fields = ['title', 'description', 'category', 'language', 'file',
              'external_link', 'thumbnail', 'author', 'publisher',
              'publication_date', 'is_featured']

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, f'Tool "{form.instance.title}" has been created successfully.')
        return super().form_valid(form)


class ToolUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EvangelismTool
    template_name = 'outreach/tool_form.html'
    fields = ['title', 'description', 'category', 'language', 'file',
              'external_link', 'thumbnail', 'author', 'publisher',
              'publication_date', 'is_featured']

    def test_func(self):
        return self.request.user.is_staff


def download_tool(request, slug):
    tool = get_object_or_404(EvangelismTool, slug=slug)
    if tool.file:
        tool.download_count = F('download_count') + 1
        tool.save()
        return FileResponse(tool.file.open(), as_attachment=True)
    return redirect(tool.external_link)


class MissionListView(ListView):
    model = Mission
    template_name = 'outreach/missions/mission_list.html'
    context_object_name = 'missions'
    ordering = ['-start_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_missions'] = Mission.objects.filter(status='active')
        context['planned_missions'] = Mission.objects.filter(status='planned')
        return context


class MissionDetailView(DetailView):
    model = Mission
    template_name = 'outreach/missions/mission_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.projects.all()
        return context


class MissionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Mission
    form_class = MissionForm
    template_name = 'outreach/missions/mission_form.html'

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
    template_name = 'outreach/missions/mission_form.html'

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
    template_name = 'outreach/missions/mission_confirm_delete.html'
    success_url = reverse_lazy('outreach:mission_list')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        mission = self.get_object()
        messages.success(self.request, f'Mission "{mission.title}" has been deleted.')
        return super().delete(request, *args, **kwargs)


class MissionEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mission
    form_class = MissionForm
    template_name = 'outreach/missions/mission_form.html'

    def test_func(self):
        """Only allow staff members to edit missions"""
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Mission: {self.object.title}'
        context['is_edit'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Mission "{form.instance.title}" has been updated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('outreach:mission_detail', kwargs={'slug': self.object.slug})

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to edit missions.')
        return super().handle_no_permission()


class ProjectListView(ListView):
    model = Project
    template_name = 'outreach/missions/project_list.html'
    context_object_name = 'projects'
    ordering = ['-start_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = dict(Project.CATEGORY_CHOICES)
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'outreach/missions/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['updates'] = self.object.updates.all()
        return context


class ProjectUpdateCreateView(LoginRequiredMixin, CreateView):
    model = ProjectUpdate
    form_class = ProjectUpdateForm
    template_name = 'outreach/missions/project_update_form.html'

    def form_valid(self, form):
        form.instance.project_id = self.kwargs['project_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('outreach:project_detail', kwargs={'slug': self.object.project.slug})


# Project Views
class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'outreach/missions/project_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        initial = super().get_initial()
        mission_id = self.request.GET.get('mission')
        if mission_id:
            initial['mission'] = get_object_or_404(Mission, id=mission_id)
        return initial


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'outreach/missions/project_form.html'

    def test_func(self):
        return self.request.user.is_staff


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'outreach/missions/project_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('outreach:mission_detail',
                            kwargs={'slug': self.object.mission.slug})


# Project Update Views
class ProjectUpdateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProjectUpdate
    form_class = ProjectUpdateForm
    template_name = 'outreach/missions/project_update_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('outreach:project_detail',
                            kwargs={'slug': self.object.project.slug})


class ProjectUpdateDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProjectUpdate
    template_name = 'outreach/missions/project_update_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('outreach:project_detail',
                            kwargs={'slug': self.object.project.slug})
