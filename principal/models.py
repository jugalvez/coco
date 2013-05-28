#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters
from django_resized import ResizedImageField

# Campos extras para modelo User

#User.add_to_class('direccion', models.CharField(max_length = 150, null = False, blank = False))
#User.add_to_class('estado', models.CharField(max_length = 50, null = False, blank = False))
#User.add_to_class('municipio', models.CharField(max_length = 50, null = False, blank = False))
#User.add_to_class('pais', models.CharField(max_length = 30, default = 'México'))
#User.add_to_class('tipo_usuario', models.SmallIntegerField(null = False, blank = False))


class Cliente(models.Model):
	usuario = models.ForeignKey(User)
	calle = models.CharField(max_length = 250, verbose_name = 'Calle y Número', blank = True, null = True)
	telefono = models.CharField(max_length = 30, null = True, blank = True, verbose_name = 'Teléfono')
	colonia = models.CharField(max_length = 100, blank = True, null = True)
	municipio = models.CharField(max_length = 30, blank = True, null = True)
	estado = models.CharField(max_length = 30, default = 'Colima')

	def __unicode__(self):
		return usuario.username


class Empresa(models.Model):
	usuario = models.ForeignKey(User)
	empresa = models.CharField(max_length = 100, unique = True, verbose_name = 'Nombre del Restaurant')
	slug = models.SlugField(max_length = 80, unique = True)
	slogan =  models.CharField(max_length = 250, null = True, blank = True, verbose_name = 'Eslogan')
	logotipo = models.ImageField(upload_to = 'logos', null = True, blank = True, help_text = 'De 240x98px se ve mejor :)')
	descripcion = models.TextField(verbose_name = 'Descripción', blank = True, null = True ,help_text = 'Crea una descripción corta, a nadie le gusta ver mucho texto en internet')
	entrega = models.BooleanField(null = False, default = False, verbose_name = 'Entrega a domicilio', help_text = '¿Tienes entrega a domicilio?')
	compra_minima = models.FloatField(default = 0, verbose_name = 'Compra Mínima', help_text = 'Compra mínina para servicio a domicilio, NO colocar signo de precio $')
	costo_envio = models.FloatField(verbose_name = 'Costo de Envío', default = 0, help_text = 'Costo de entrega a domicilio, NO colocar signo de precio $')
	estatus = models.BooleanField(default = True)
	paquete = models.IntegerField()

	def save(self, *args, **kwargs):
		self.slug = defaultfilters.slugify(self.empresa)
		super(Empresa, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.empresa


class Sucursal(models.Model):
	empresa = models.ForeignKey(Empresa)
	usuario = models.ForeignKey(User)
	nombre = models.CharField(max_length = 50, blank = True, null = True)
	telefono = models.CharField(max_length = 30, null = True, blank = True, verbose_name = 'Teléfono')
	calle = models.CharField(max_length = 200, null = False)
	colonia = models.CharField(max_length = 200, null = False)
	municipio = models.CharField(max_length = 30, null = False)
	estado = models.CharField(max_length = 30, null = False, default = 'Colima')
	matriz = models.BooleanField(default = False, verbose_name = '¿Es la sucursal principal?')
	usuario = models.CharField(max_length = 150)
	password = models.CharField(max_length = 150)

	def __unicode__(self):
		return self.usuario.username


class Contrato(models.Model):
	empresa = models.ForeignKey(Empresa)
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField()

	def __unicode__(self):
		return self.usuario.username


class Platillo(models.Model):
	empresa = models.ForeignKey(Empresa)
	nombre_platillo = models.CharField(max_length = 100, null = False, blank = False, verbose_name = 'Nombre del Platillo')
	slug = models.SlugField(max_length = 80, unique = False)
	fotografia = ResizedImageField(max_width = 413, max_height = 287, upload_to = 'platillos', help_text = 'Puede ser JPG o PNG')
	descripcion = models.TextField(help_text = 'Describe el platillo, acompañamientos, especias, ingredientes, etc..')
	precio = models.FloatField(help_text = 'NO colocar signo de precio $')
	fecha_publicacion = models.DateTimeField(auto_now = True)
	tags = models.CharField(max_length = 250, verbose_name = 'Categorías')
	estatus = models.BooleanField(null = False, default = True, verbose_name = '¿Disponible?')

	def save(self, *args, **kwargs):
		self.slug = defaultfilters.slugify(self.nombre_platillo)
		super(Platillo, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.nombre_platillo


class Horario(models.Model):
	empresa = models.ForeignKey(Empresa)
	lunes_abre = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'Lunes')
	lunes_cierra = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'a')
	martes_abre = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'Martes')
	martes_cierra = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'a')
	miercoles_abre = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'Miércoles')
	miercoles_cierra = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'a')
	jueves_abre = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'Jueves')
	jueves_cierra = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'a')
	viernes_abre = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'Viernes')
	viernes_cierra = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'a')
	sabado_abre = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'Sábado')
	sabado_cierra = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'a')
	domingo_abre = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'Domingo')
	domingo_cierra = models.CharField(max_length = 24, blank = True, null = True, verbose_name = 'a')

	def __unicode__(self):
		return self.lunes


class Calificacion_pedido(models.Model):
	cliente = models.ForeignKey(User)
	platillo = models.ForeignKey(Platillo)
	num_pedido = models.CharField(max_length = 200)
	sabor = models.IntegerField(null = False, default = 1)
	precio = models.IntegerField(null = False, default = 1)
	entrega = models.IntegerField(null = False, default = 1)
	comentario = models.TextField(null = True, blank = True)
	fecha = models.DateTimeField(auto_now = True)
	estatus = models.BooleanField(default = False)

	def __unicode__(self):
		return self.comentario


class Calificacion_usuario(models.Model):
	cliente = models.ForeignKey(User)
	empresa = models.ForeignKey(Empresa)
	num_pedido = models.CharField(max_length = 200)
	calificacion = models.SmallIntegerField(null = False)   #Bueno = 2, Regualar = 1, malo = 0
	comentario = models.TextField(null = True, blank = True)
	fecha = models.DateTimeField(auto_now = True)
	estatus = models.BooleanField(default = False)

	def __unicode__(self):
		return self.calificacion


class Compra(models.Model):
	cliente = models.ForeignKey(User)
	platillo = models.ForeignKey(Platillo)
	sucursal = models.ForeignKey(Sucursal)
	fecha = models.DateTimeField(auto_now = True)
	cantidad = models.SmallIntegerField(null = False, default = 0)
	num_pedido = models.CharField(max_length = 200)
	estatus = models.BooleanField(null = False, default = False)

	def __unicode__(self):
		return self.fecha_compra



class Favorito(models.Model):
	cliente = models.ForeignKey(User)
	platillo = models.ForeignKey(Platillo)

	def __unicode__(self):
		return self.usuario


