from principal.models import Empresa, Sucursal, Platillo, Horario, Calificacion_platillo, Calificacion_usuario, Compra, Favorito
from principal.forms import BusquedaForm, EmpresaForm, SucursalForm, PlatilloForm, PerfilForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
#from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
#from django.utils import simplejson
from django.core import serializers
#from django.utils import simplejson

from django.template.defaultfilters import slugify
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required



def acerca(request):
	formBuscar = BusquedaForm()	
	return render_to_response('acerca.html', {'formulario': formBuscar}, context_instance=RequestContext(request))

def busqueda(request):
	if request.method=='POST':
		formBuscar = BusquedaForm(request.POST)
		if formBuscar.is_valid():
			q = '%'+ formBuscar.cleaned_data['platillo']  +'%'
			if formBuscar.cleaned_data['ciudad']!='':
				qe = '%'+ formBuscar.cleaned_data['ciudad']  +'%'
				platillos = Empresa.objects.raw("SELECT DISTINCT nombre_platillo, precio, fotografia, principal_platillo.id, calle, estado, municipio, hora_abre, hora_cierra, empresa, principal_empresa.id as id_empresa FROM  principal_empresa, principal_platillo, principal_sucursal, principal_horario WHERE (nombre_platillo LIKE %s OR empresa LIKE %s) AND principal_empresa.id=principal_platillo.usuario_id AND principal_empresa.id=principal_horario.empresa_id AND principal_empresa.id=principal_sucursal.usuario_id AND principal_sucursal.estado like %s",  [q, q, qe])
			else:
				platillos = Empresa.objects.raw("SELECT DISTINCT nombre_platillo, precio, fotografia, principal_platillo.id, calle, estado, municipio, hora_abre, hora_cierra, empresa, principal_empresa.id as id_empresa FROM  principal_empresa, principal_platillo, principal_sucursal, principal_horario WHERE (nombre_platillo LIKE %s OR empresa LIKE %s) AND principal_empresa.id=principal_platillo.usuario_id AND principal_empresa.id=principal_horario.empresa_id",  [q, q])
	else:
		formBuscar = BusquedaForm()
		q = '%%'
		#empresas = Empresa.objects.raw("SELECT DISTINCT nombre_platillo, precio, fotografia, principal_platillo.id, calle, estado, municipio, hora_abre, hora_cierra, empresa, principal_empresa.id as id_empresa FROM  principal_empresa, principal_platillo, principal_sucursal, principal_horario WHERE (nombre_platillo LIKE %s OR empresa LIKE %s) AND principal_empresa.id=principal_platillo.usuario_id AND principal_empresa.id=principal_horario.empresa_id",  [q, q])
		platillos = Platillo.objects.all()
	return render_to_response('busqueda.html', {'platillos': platillos, 'formulario': formBuscar}, context_instance=RequestContext(request))


def platillo(request, id_platillo):
	plato = get_object_or_404(Platillo, pk=id_platillo)
	horario = Horario.objects.filter(empresa=plato.empresa)
	lugar = Sucursal.objects.filter(empresa=plato.empresa)[:1]
	estrellas = Calificacion_platillo(platillo=plato)
	otros = Platillo.objects.filter(empresa=plato.empresa).exclude(pk=id_platillo)
	formBuscar = BusquedaForm()	
	return render_to_response('platillo.html', {'dato': plato, 'hora': horario, 'lugar': lugar, 'estrellas': estrellas, 'otros': otros, 'formulario': formBuscar}, context_instance=RequestContext(request))


def sitio(request, id_negocio):
	negocio = get_object_or_404(Empresa, pk=id_negocio)
	horario = Horario.objects.filter(empresa=negocio)
	lugar = Sucursal.objects.filter(empresa=negocio)[:1]
	formBuscar = BusquedaForm()
	#platillos = Platillo.objects.filter(empresa=negocio)
	#categorias = Categoria_platillo.objects.filter(platillo=platillos).order_by('nombre_categoria')
	return render_to_response('sitio.html', {'negocio': negocio, 'horario': horario, 'lugar': lugar, 'formulario': formBuscar}, context_instance=RequestContext(request))


def login(request):
	if request.method == 'POST':
		formLogin = AuthenticationForm(request.POST)

		if formLogin.is_valid:
			usuario = request.POST['usuario']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)

			if acceso is not None:
				if acceso.is_active:
					auth_login(request, acceso)
					return HttpResponseRedirect('/panel/datos')
				#else:
					#return render_to_response('noactivo.html', context_instance = RequestContext(request))
			#else:
			#	return render_to_response('nousuario.html', context_instance = RequestContext(request))
	else:
		formLogin = AuthenticationForm()
		formBuscar = BusquedaForm()
	return render_to_response('login.html',{'formulario': formBuscar},context_instance=RequestContext(request))


def registro(request):
	if request.method == 'POST':
		formRegistro = UserCreationForm(request.POST)
		if formRegistro.is_valid():
			formRegistro.save()
			'''
				Guardamos el registro, hacemos login y lo enviamos al panel
			'''
			usuario = request.POST['username']
			clave = request.POST['password1']
			
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					auth_login(request, acceso)
					return HttpResponseRedirect('/panel/datos')
			else:
				return HttpResponseRedirect('/login')
	else:
		formRegistro = UserCreationForm()
		formBuscar = BusquedaForm()
	return render_to_response('registro.html', { 'formulario': formBuscar, 'formRegistro': formRegistro }, context_instance=RequestContext(request))


'''
	PANEL DE CONTROL
'''

@login_required(login_url='/login')
def perfil(request):

	Qdatos = User.objects.get(pk = request.user.id)

	if request.method == 'POST':
		form = PerfilForm(request.POST, instance = Qdatos)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/panel/perfil')

	else:
		form = PerfilForm(instance = Qdatos)
		formBuscar = BusquedaForm()
	return render_to_response('panel/perfil.html', { 'formulario': formBuscar, 'form': form}, context_instance = RequestContext(request))



@login_required(login_url='/login')
def datos_negocio(request):

	Qdatos = Empresa.objects.get(usuario = request.user)

	if request.method == 'POST':
		form = EmpresaForm(request.POST, request.FILES, instance = Qdatos)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/panel/datos')

	else:
		form = EmpresaForm(instance = Qdatos)
		formBuscar = BusquedaForm()

	return render_to_response('panel/negocio.html', { 'formulario': formBuscar, 'form': form}, context_instance = RequestContext(request))



@login_required(login_url='/login')
def lista_sucursal(request):
	listaSucursal = Sucursal.objects.filter(usuario = request.user)
	formBuscar = BusquedaForm()
	return render_to_response('panel/lista_sucursal.html', { 'formulario': formBuscar, 'lista': listaSucursal }, context_instance = RequestContext(request))


@login_required(login_url='/login')
def datos_sucursal(request):
	if request.method == 'POST':
		sucursal = Sucursal(usuario_id = request.user.id)
		form = SucursalForm(request.POST, instance = sucursal)
	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/panel/sucursales')
	else:
		form = SucursalForm()
		formBuscar = BusquedaForm()
	return render_to_response('panel/sucursal.html', { 'formulario': formBuscar, 'form': form }, context_instance = RequestContext(request))


@login_required(login_url='/login')
def edita_sucursal(request, id_sucursal):

	Qdatos = Sucursal.objects.get(pk = id_sucursal)
	
	if request.method == 'POST':
		form = SucursalForm(request.POST, instance = Qdatos)
	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/panel/sucursales')
	else:
		form = SucursalForm(instance = Qdatos)
		formBuscar = BusquedaForm()
	return render_to_response('panel/sucursal.html', { 'formulario': formBuscar, 'form': form }, context_instance = RequestContext(request))



@login_required(login_url='/login')
def lista_platillo(request):
	listaPlatillo = Platillo.objects.filter(usuario = request.user)
	formBuscar = BusquedaForm()
	return render_to_response('panel/lista_platillo.html', { 'formulario': formBuscar, 'lista': listaPlatillo }, context_instance = RequestContext(request))


@login_required(login_url='/login')
def nuevo_platillo(request):
	if request.method == 'POST':
		platillo = Platillo(usuario = request.user)
		form = PlatilloForm(request.POST, request.FILES, instance = platillo)
	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/panel/platillos/')
	else:
		form = PlatilloForm()
		formBuscar = BusquedaForm()
	return render_to_response('panel/platillo.html', { 'formulario': formBuscar, 'form': form }, context_instance = RequestContext(request))


@login_required(login_url='/login')
def edita_platillo(request, id_platillo):
	
	Qdatos = Platillo.objects.get(pk = id_platillo)
	
	if request.method == 'POST':
		form = PlatilloForm(request.POST, request.FILES, instance = Qdatos)
	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/panel/platillos/')
	else:
		form = PlatilloForm(instance = Qdatos)
		formBuscar = BusquedaForm()
	return render_to_response('panel/platillo.html', { 'formulario': formBuscar, 'form': form }, context_instance = RequestContext(request))




@login_required(login_url='/login')
def salir(request):
	logout(request)
	return HttpResponseRedirect('/')







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





















