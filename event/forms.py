from django import forms
from django.forms import DateInput, ModelForm

from .models import Event

class EventForm(ModelForm):
    """ Форма создания события """
    
    class Meta:
        model = Event
        fields = ["title", "description", "location", "type" , "start_time", "end_time"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите название события"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Введите описание события"}),
            "start_time": DateInput(attrs={"type": "datetime-local", "class": "form-control"}, format="%Y-%m-%dT%H:%M"),
            "end_time": DateInput(attrs={"type": "datetime-local", "class": "form-control"},format="%Y-%m-%dT%H:%M"),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)