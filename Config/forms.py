from django.forms import ModelForm
from .models import Constantes

class ConstantesForm(ModelForm):
    class Meta:
        model = Constantes
        fields = ['nombre', 'valor']