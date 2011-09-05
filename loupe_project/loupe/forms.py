from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from loupe.models import Image, Corkboard, Note, Project

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ('created_on', 'updated_on', 'user',)
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ProjectForm, self).__init__(*args, **kwargs)

class CorkboardForm(forms.ModelForm):

    class Meta:
        model = Corkboard
        exclude = ('created_on', 'updated_on', 'user', 'images', 'project',)
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(CorkboardForm, self).__init__(*args, **kwargs)

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        exclude = ('created_on', 'updated_on', 'user', 'num_views', 'corkboard',)
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ImageForm, self).__init__(*args, **kwargs)

class NoteForm(forms.ModelForm):

    note = forms.CharField(label="Note")
    x1 = forms.IntegerField(widget=forms.HiddenInput)
    y1 = forms.IntegerField(widget=forms.HiddenInput)
    height = forms.IntegerField(widget=forms.HiddenInput)
    width = forms.IntegerField(widget=forms.HiddenInput)
    
    class Meta:
        model = Note
        exclude = ('created_on', 'updated_on', 'user', 'image',)
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(NoteForm, self).__init__(*args, **kwargs)
