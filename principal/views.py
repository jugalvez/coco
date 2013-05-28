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
from django.template.defaultfilters import slugify
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage

#from django.utils import simplejson
#from django.utils import simplejson



def inicio(request):
	formBuscar = BusquedaForm()	
	return render_to_response('inicio.html', {'formulario': formBuscar}, context_instance=RequestContext(request))


def acerca(request):
	formBuscar = BusquedaForm()	
	return render_to_response('acerca.html', {'formulario': formBuscar}, context_instance=RequestContext(request))


def contacto(request):
	formBuscar = BusquedaForm()
	
	if request.method=='POST':
		formContacto = ContactoForm(request.POST)
		if formContacto.is_valid():
			titulo = 'Mensaje desde Cocoscore.com'
			contenido = formContacto.cleaned_data['nombre'] + ' te envio este mensaje: \n\n'
			contenido += formContacto.cleaned_data['mensaje'] + '\n'
			contenido += 'Contactar con ' + formContacto.cleaned_data['correo']
			correo = EmailMessage(titulo, contenido, to = ['info@grupogalco.net'])
			correo.send()
			return render_to_response('contacto_ok.html', {'formulario': formBuscar}, context_instance=RequestContext(request))
		else:
			formContacto = ContactoForm()
			return render_to_response('contacto.html', {'formulario': formBuscar, 'contacto': ContactoForm}, context_instance=RequestContext(request))	
	else:
		formContacto = ContactoForm()
		return render_to_response('contacto.html', {'formulario': formBuscar, 'contacto': ContactoForm}, context_instance=RequestContext(request))


def busqueda(request):
	if request.method=='POST':
		formBuscar = BusquedaForm(request.POST)
		if formBuscar.is_valid():
			q = formBuscar.cleaned_data['platillo']
			qe = formBuscar.cleaned_data['ciudad']
			platillos = Platillo.objects.filter(nombre_platillo__contains = q).order_by('nombre_platillo')
		else:
			formBuscar = BusquedaForm()
			platillos = Platillo.objects.all().order_by('nombre_platillo')
	else:
		formBuscar = BusquedaForm()
		platillos = Platillo.objects.all().order_by('nombre_platillo')
	return render_to_response('busqueda.html', {'platillos': platillos, 'formulario': formBuscar}, context_instance = RequestContext(request))


def platillo(request, restaurant, platillo):
	empresa = get_object_or_404(Empresa, slug = restaurant)
	plato = get_object_or_404(Platillo, slug = platillo)
	hora = Horario.objects.get(empresa = empresa)
	lugar = Sucursal.objects.filter(empresa = plato.empresa)[:1]
	hoy = datetime.now()
	dia = datetime.strftime(hoy, '%w')
	#estrellas = Calificacion_platillo(platillo=plato)
	#otros = Platillo.objects.filter(empresa=plato.empresa).exclude(pk=id_platillo)
	formBuscar = BusquedaForm()	
	#return render_to_response('platillo.html', {'dato': plato, 'hora': horario, 'lugar': lugar, 'estrellas': estrellas, 'otros': otros, 'formulario': formBuscar}, context_instance=RequestContext(request))
	return render_to_response('platillo.html', {'dato': plato, 'formulario': formBuscar, 'lugar': lugar, 'hora': hora, 'dia': dia}, context_instance=RequestContext(request))


def sitio(request, restaurant):
	negocio = get_object_or_404(Empresa, slug = restaurant)
	hora = Horario.objects.get(empresa = negocio)
	lugar = Sucursal.objects.filter(empresa = negocio)
	formBuscar = BusquedaForm()
	platillos = Platillo.objects.filter(empresa = negocio)
	hoy = datetime.now()
	dia = datetime.strftime(hoy, '%w')
	#categorias = Categoria_platillo.objects.filter(platillo=platillos).order_by('nombre_categoria')
	return render_to_response('sitio.html', {'negocio': negocio, 'hora': hora, 'lugar': lugar, 'platillo': platillos ,'formulario': formBuscar, 'hoy': hoy, 'dia': dia}, context_instance=RequestContext(request))


def login(request):
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
					
					''' Buscamos al usuario, y guardamos la sesión '''
					usuario_encuentra = User.objects.get(username = usuario)
					request.session['tipo'] = 2

					return HttpResponseRedirect('/clientes')
				#else:
					#return render_to_response('noactivo.html', context_instance = RequestContext(request))
			#else:
			#	return render_to_response('nousuario.html', context_instance = RequestContext(request))
	titulo = 'Iniciar Sesión'
	return render_to_response('login.html', {'formulario': formBuscar, 'titulo': titulo}, context_instance=RequestContext(request))


def registro(request):
	formBuscar = BusquedaForm()

	if request.method == 'POST':
		formRegistro = UserCreationForm(request.POST)
		if formRegistro.is_valid():
			
			'''		Guardamos el registro, tomamos el usuario y password para hacer magia negra	 '''
			formRegistro.save()
			usuario = request.POST['username']
			clave = request.POST['password1']

			''' Tomamos el registro del nuevo usuario, guardamos un registro en Clientes, y la sesión '''
			usuario_registro = User.objects.get(username = usuario)
			cliente = Cliente(usuario = usuario_registro)
			cliente.save()
			request.session['tipo'] = 2

			''' Hacemos LogIn y enviamos al usuario al Panel de control '''
			acceso = authenticate(username = usuario, password = clave)
			if acceso is not None:
				if acceso.is_active:
					auth_login(request, acceso)				
					return HttpResponseRedirect('/clientes')
			else:
				return HttpResponseRedirect('/login')
	else:
		formRegistro = UserCreationForm()
	return render_to_response('registro.html', { 'formulario': formBuscar, 'formRegistro': formRegistro }, context_instance = RequestContext(request))


@login_required(login_url='/login')
def salir(request):
	pkt = request.session.get('tipo')	
	logout(request)
	if pkt == 2:
		return HttpResponseRedirect('/login/')
	else:
		return HttpResponseRedirect('/mi-negocio/')




def add_Pedido(cliente, platillo, cantidad):
	num_pedido = 200
	busca = Compra.objects.filter(num_pedido = num_pedido, platillo = platillo)
	
	if busca:
		actualiza = Compra(cantidad = cantidad)
		actualiza.save()
	else:
		add = Compra(cliente = cliente, platillo = platillo, cantidad = cantidad, num_pedido = num_pedido)
		add.save()








'''
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
'''
