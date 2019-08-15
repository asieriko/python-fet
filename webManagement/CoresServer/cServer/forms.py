from django import forms
from .models import File, Assignment

class AssignementForm(forms.Form):
    
    files = forms.ModelChoiceField(
        queryset = File.objects.all(),
    )
    
    assignements = forms.ModelMultipleChoiceField(
        queryset = Assignment.objects.all(),
        widget  = forms.CheckboxSelectMultiple,
    )
    
#     name.widget.attrs.update({'class': 'form-control'})
#     assignements.widget.attrs.update({'class': 'form-control'})
    
class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name','fetfile']