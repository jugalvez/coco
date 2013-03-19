#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from principal.models import Empresa, Sucursal, Platillo, Horario

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
		exclude = ('slug', 'usuario', 'estatus', 'paquete')


class SucursalForm(ModelForm):
	class Meta:
		model = Sucursal
		exclude = ('empresa')


class PlatilloForm(ModelForm):
	class Meta:
		model = Platillo
		exclude = ('empresa', 'slug')


class HorarioForm(ModelForm):
	class Meta:
		model = Horario
		exclude = ('empresa')
		

class ContactoForm(forms.Form):
	nombre = forms.CharField(label = 'Nombre')
	correo = forms.EmailField(label = 'E-mail')
	mensaje = forms.CharField(widget = forms.Textarea)