# import form class from django
from django import forms
from .models import Document
from .models import Surveys, Questions, Choices, Questionnaires


# create a ModelForm
class CreateSurveyForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Surveys
        fields = "__all__"

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ( 'model_type', 'description', 'document', )