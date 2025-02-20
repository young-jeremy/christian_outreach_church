class BibleStudyMaterialForm(forms.ModelForm):
    class Meta:
        model = BibleStudyMaterial
        fields = ['title', 'description', 'file', 'category']