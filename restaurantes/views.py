#encoding: utf-8
from principal.models import Cliente, Empresa, Sucursal, Platillo, Horario, Contrato, Calificacion_pedido, Calificacion_usuario, Compra, Favorito
from principal.forms import BusquedaForm, EmpresaForm, EmpresaAnunciaForm, SucursalForm, PlatilloForm, PerfilForm, ContactoForm, HorarioForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime, timedelta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required


def miNegocio(request):
	formBuscar = BusquedaForm()
	
	if request.method == 'POST':
		formLogin = AuthenticationForm(request.POST)

		if formLogin.is_valid:
			usuario = request.POST['usuario']
			clave = request.POST['password']
			acceso = authenticate(username = usuario, password = clave)

			if acceso is not None:
				if acceso.is_active:
					auth_login(request, acceso)
					
					''' Buscamos al usuario '''
					usuario_encuentra = User.objects.get(username = usuario)

					''' Lo buscamos en la lista de empresas, si está guardamos el tipo de sesion '''
					usuario_cliente = Empresa.objects.get(usuario_id = usuario_encuentra.pk)
					request.session['tipo'] = 1

					return HttpResponseRedirect('/mi-negocio/perfil')
				#else:
					#return render_to_response('noactivo.html', context_instance = RequestContext(request))
			#else:
			#	return render_to_response('nousuario.html', context_instance = RequestContext(request))
	titulo = 'Inicio de Sesión Restauranteros'
	return render_to_response('login.html', {'formulario': formBuscar, 'titulo': titulo}, context_instance=RequestContext(request))



@login_required(login_url='/login')
def perfil(request):

	pkt = request.session.get('tipo')
	formBuscar = BusquedaForm()
	Qdatos = User.objects.get(pk = request.user.id)

	if request.method == 'POST':
		form = PerfilForm(request.POST, instance = Qdatos)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/mi-negocio/perfil')

	else:
		form = PerfilForm(instance = Qdatos)
	return render_to_response('panel/perfil.html', { 'formulario': formBuscar, 'form': form, 'pkt': pkt }, context_instance = RequestContext(request))


@login_required(login_url='/login')
def horario(request):
	
	pkt = request.session.get('tipo')
	formBuscar = BusquedaForm()

	empresa = Empresa.objects.get(usuario = request.user)
	Qdatos = Horario.objects.filter(empresa = empresa)

	if request.method == 'POST':
		if Qdatos:
			Qdata = Horario.objects.get(empresa = empresa)
			horas = HorarioForm(request.POST, instance = Qdata)	
		else:
			quien = Horario(empresa = empresa)
			horas = HorarioForm(request.POST, instance = quien)	

		if horas.is_valid():
			horas.save()
			return HttpResponseRedirect('/mi-negocio/horarios')
	else:
		if Qdatos:
			Gdatos = Horario.objects.get(empresa = empresa)
			horas = HorarioForm(instance = Gdatos)
		else:
			horas = HorarioForm()
	return render_to_response('panel/horario.html', { 'formulario': formBuscar, 'form': horas, 'pkt': pkt } ,context_instance = RequestContext(request))


@login_required(login_url='/login')
def datos_negocio(request):

	pkt = request.session.get('tipo')

	formBuscar = BusquedaForm()
	Qdatos = Empresa.objects.get(usuario = request.user)

	if request.method == 'POST':	
		form = EmpresaForm(request.POST, request.FILES, instance = Qdatos)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/mi-negocio/datos')
	else:
		form = EmpresaForm(instance = Qdatos)
	return render_to_response('panel/negocio.html', { 'formulario': formBuscar, 'form': form, 'pkt': pkt }, context_instance = RequestContext(request))



@login_required(login_url='/login')
def lista_sucursal(request):
	empresa = Empresa.objects.get(usuario = request.user)
	listaSucursal = Sucursal.objects.filter(empresa = empresa)
	formBuscar = BusquedaForm()
	return render_to_response('panel/lista_sucursal.html', { 'formulario': formBuscar, 'lista': listaSucursal }, context_instance = RequestContext(request))


@login_required(login_url='/login')
def datos_sucursal(request):
	
	formBuscar = BusquedaForm()

	if request.method == 'POST':
		empresa = Empresa.objects.get(usuario = request.user)
		sucursal = Sucursal(empresa = empresa)
		form = SucursalForm(request.POST, instance = sucursal)
	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/mi-negocio/sucursales')
	else:
		form = SucursalForm()
	return render_to_response('panel/sucursal.html', { 'formulario': formBuscar, 'form': form }, context_instance = RequestContext(request))


@login_required(login_url='/login')
def edita_sucursal(request, id_sucursal):
	formBuscar = BusquedaForm()
	Qdatos = Sucursal.objects.get(pk = id_sucursal)
	
	if request.method == 'POST':
		form = SucursalForm(request.POST, instance = Qdatos)
	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/mi-negocio/sucursales')
	else:
		form = SucursalForm(instance = Qdatos)
	return render_to_response('panel/sucursal.html', { 'formulario': formBuscar, 'form': form }, context_instance = RequestContext(request))



@login_required(login_url='/login')
def lista_platillo(request):
	
	formBuscar = BusquedaForm()
	empresa = Empresa.objects.filter(usuario = request.user)[:1]
	listaPlatillo = Platillo.objects.filter(empresa = empresa)
	return render_to_response('panel/lista_platillo.html', { 'formulario': formBuscar, 'lista': listaPlatillo }, context_instance = RequestContext(request))


@login_required(login_url='/login')
def nuevo_platillo(request):
	formBuscar = BusquedaForm()
	
	if request.method == 'POST':
		empresa = Empresa.objects.get(usuario = request.user)
		platillo = Platillo(empresa = empresa)
		form = PlatilloForm(request.POST, request.FILES, instance = platillo)
	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/mi-negocio/platillos/')
	else:
		form = PlatilloForm()
	return render_to_response('panel/platillo.html', { 'formulario': formBuscar, 'form': form }, context_instance = RequestContext(request))


@login_required(login_url='/login')
def edita_platillo(request, id_platillo):
	
	formBuscar = BusquedaForm()
	Qdatos = Platillo.objects.get(pk = id_platillo)
	
	if request.method == 'POST':
		form = PlatilloForm(request.POST, request.FILES, instance = Qdatos)
	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/mi-negocio/platillos/')
	else:
		form = PlatilloForm(instance = Qdatos)
	return render_to_response('panel/platillo.html', { 'formulario': formBuscar, 'form': form }, context_instance = RequestContext(request))








@csrf_exempt
def ajax(request, id):
	if request.is_ajax:
		if request.method == 'POST':
			platillo = Platillo.objects.filter(pk=id)
			JSONSerializer = serializers.get_serializer("json")
			json = JSONSerializer()
			json.serialize(platillo)
			data = json.getvalue()

			#json = serializers.serialize("json", data)
			#json = simplejson.dumps(platillo)
			return HttpResponse(data, mimetype='application/json')



