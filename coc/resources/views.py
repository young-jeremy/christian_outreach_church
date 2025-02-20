from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from services.models import BibleStudyMaterial
from services.forms import BibleStudyMaterialForm

class BibleStudyMaterialListView(LoginRequiredMixin, ListView):
    model = BibleStudyMaterial
    template_name = 'resources/bible_study/list.html'
    context_object_name = 'materials'

class BibleStudyMaterialDetailView(LoginRequiredMixin, DetailView):
    model = BibleStudyMaterial
    template_name = 'resources/bible_study/detail.html'
    context_object_name = 'material'

class BibleStudyMaterialCreateView(LoginRequiredMixin, CreateView):
    model = BibleStudyMaterial
    form_class = BibleStudyMaterialForm
    template_name = 'resources/bible_study/form.html'
    success_url = reverse_lazy('bible-study-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BibleStudyMaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = BibleStudyMaterial
    form_class = BibleStudyMaterialForm
    template_name = 'resources/bible_study/form.html'
    success_url = reverse_lazy('bible-study-list')

class BibleStudyMaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = BibleStudyMaterial
    template_name = 'resources/bible_study/confirm_delete.html'
    success_url = reverse_lazy('bible-study-list')