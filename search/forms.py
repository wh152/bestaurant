from django import forms
from search.models import Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(help_text="Please enter the category name")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)