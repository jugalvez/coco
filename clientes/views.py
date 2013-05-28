#encoding: utf-8
from principal.models import Cliente, Calificacion_pedido, Calificacion_usuario, Compra, Favorito
from principal.forms import BusquedaForm, DatosClienteForm, PerfilClienteForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime, timedelta
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required


''' 
	Panel de Clientes 
'''

@login_required(login_url='/login')
def perfilClientes(request):

	pkt = request.session.get('tipo')
	formBuscar = BusquedaForm()
	Qdatos = User.objects.get(pk = request.user.id)

	if request.method == 'POST':
		form = PerfilClienteForm(request.POST, instance = Qdatos)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/clientes/')
	else:
		form = PerfilClienteForm(instance = Qdatos)
	titulo = 'Datos Personales'
	return render_to_response('clientes/datos.html', { 'formulario': formBuscar, 'form': form, 'titulo': titulo, 'pkt': pkt }, context_instance = RequestContext(request))


@login_required(login_url='/login')
def datosClientes(request):

	pkt = request.session.get('tipo')
	formBuscar = BusquedaForm()
	Qdatos = Cliente.objects.get(usuario = request.user)

	if request.method == 'POST':
		form = DatosClienteForm(request.POST, instance = Qdatos)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/clientes/domicilio')

	else:
		form = DatosClienteForm(instance = Qdatos)
	titulo = 'Mi Ubicación'
	return render_to_response('clientes/datos.html', { 'formulario': formBuscar, 'form': form, 'titulo': titulo, 'pkt': pkt }, context_instance = RequestContext(request))

