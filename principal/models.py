#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters

# Campos extras para modelo User

#User.add_to_class('direccion', models.CharField(max_length = 150, null = False, blank = False))
#User.add_to_class('estado', models.CharField(max_length = 50, null = False, blank = False))
#User.add_to_class('municipio', models.CharField(max_length = 50, null = False, blank = False))
#User.add_to_class('pais', models.CharField(max_length = 30, default = 'México'))
#User.add_to_class('tipo_usuario', models.SmallIntegerField(null = False, blank = False))


class Empresa(models.Model):
	usuario = models.ForeignKey(User)
	empresa = models.CharField(max_length = 100, unique = True, verbose_name = 'Nombre del Restaurant')
	slug = models.SlugField(max_length = 80, unique = True)
	slogan =  models.CharField(max_length = 250, null = True, blank = True, verbose_name = 'Eslogan')
	logotipo = models.ImageField(upload_to = 'logos', null = True, blank = True)
	descripcion = models.TextField(verbose_name = 'Descripción')
	compra_minima = models.FloatField(verbose_name = 'Compra Mínima')
	costo_envio = models.FloatField(verbose_name = 'Costo de Envío')

	def save(self, *args, **kwargs):
		self.slug = defaultfilters.slugify(self.empresa)
		super(Empresa, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.empresa


class Sucursal(models.Model):
	usuario = models.ForeignKey(User)
	calle = models.CharField(max_length = 200, null = False)
	colonia = models.CharField(max_length = 200, null = False)
	municipio = models.CharField(max_length = 30, null = False)
	estado = models.CharField(max_length = 30, null = False)

	def __unicode__(self):
		return self.usuario.username


class Platillo(models.Model):
	usuario = models.ForeignKey(User)
	nombre_platillo = models.CharField(max_length = 100, null = False, blank = False, verbose_name = 'Nombre del Platillo')
	slug = models.SlugField(max_length = 80, unique = False)
	fotografia = models.ImageField(upload_to = 'platillos', verbose_name = 'Fotografía')
	descripcion = models.TextField()
	precio = models.FloatField()
	#dia_existencia = models.CharField(max_length = 150)
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
	dia = models.CharField(max_length = 15)
	hora_abre = models.CharField(max_length = 10)
	hora_cierra = models.CharField(max_length = 10)

	def __unicode__(self):
		return self.hora_abre


class Calificacion_platillo(models.Model):
	usuario = models.ForeignKey(User)
	platillo = models.ForeignKey(Platillo)
	sabor = models.IntegerField()
	precio = models.IntegerField()
	entrega = models.IntegerField()
	comentario = models.TextField(null = True, blank = True)

	def __unicode__(self):
		return self.comentario


class Calificacion_usuario(models.Model):
	usuario = models.ForeignKey(User)
	empresa = models.ForeignKey(Empresa)
	calificacion = models.SmallIntegerField(null = False)
	comentario = models.TextField(null = True, blank = True)

	def __unicode__(self):
		return self.calificacion


class Compra(models.Model):
	usuario = models.ForeignKey(User)
	platillo = models.ForeignKey(Platillo)
	fecha_compra = models.DateTimeField(auto_now = True)
	cantidad = models.SmallIntegerField(null = False)
	calificaion = models.BooleanField(null = False, default = False)
	sesion = models.CharField(max_length = 200)
	estatus = models.BooleanField(null = False, default = False)

	def __unicode__(self):
		return self.fecha_compra


class Favorito(models.Model):
	usuario = models.ForeignKey(User)
	platillo = models.ForeignKey(Platillo)

	def __unicode__(self):
		return self.usuario


