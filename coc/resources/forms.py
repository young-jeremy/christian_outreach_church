from django import forms

from .models import *


class DailyDevotionForm(forms.ModelForm):
    class Meta:
        model = DailyDevotion
        fields = ['title', 'scripture_reference', 'scripture_text',
                  'devotional_content', 'prayer_focus', 'publication_date']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }
