# forms.py
from django import forms

class ImageUploadForm(forms.Form):
    file = forms.FileField(label='uploadDataSet', widget=forms.ClearableFileInput(attrs={'multiple': True, 'webkitdirectory': True, 'mozdirectory': True}))

class ImageSearchForm(forms.Form):
    file = forms.FileField(label='uploadSearch')