from django import forms
from . models import Chat

class messageForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['message']
