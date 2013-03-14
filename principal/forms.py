#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from principal.models import Empresa, Sucursal, Platillo

class BusquedaForm(forms.Form):
	platillo = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Tengo ganas de...'}))
	ciudad = forms.CharField(label='', widget=forms.TextInput(attrs={'readonly': 'readonly', 'value': 'Colima'}), required=False)


class PerfilForm(ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')


class EmpresaForm(ModelForm):
	class Meta:
		model = Empresa
		exclude = ('slug', 'usuario')


class SucursalForm(ModelForm):
	class Meta:
		model = Sucursal
		exclude = ('empresa')


class PlatilloForm(ModelForm):
	class Meta:
		model = Platillo
		exclude = ('empresa', 'slug')