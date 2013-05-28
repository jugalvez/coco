from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',

#Panel de control Django    
	url(r'^cocopanel/doc/', include('django.contrib.admindocs.urls')),
    url(r'^cocopanel/', include(admin.site.urls)),

#    url(r'^ajax/(?P<id>\d+)$', 'principal.views.ajax'),

# Vista de visitantes
    url(r'^$', 'principal.views.inicio'),
    url(r'^acerca/$', 'principal.views.acerca'),
    url(r'^contacto/$', 'principal.views.contacto'),
    url(r'^registro/$', 'principal.views.registro'),
    url(r'^login/$', 'principal.views.login'),
    url(r'^registro/$', 'principal.views.registro'),

#Busqueda, Detalle Platillo y Vista Negocio
    url(r'^buscar/$', 'principal.views.busqueda'),
    url(r'^negocio/(?P<restaurant>[-_\w]+)/(?P<platillo>[-_\w]+)/$', 'principal.views.platillo'),
    url(r'^negocio/(?P<restaurant>[-_\w]+)/$', 'principal.views.sitio'),


# Panel para Clientes
    url(r'^clientes/$', 'clientes.views.perfilClientes'),
    url(r'^clientes/domicilio/$', 'clientes.views.datosClientes'),


# Panel de control Restaurante
    url(r'^mi-negocio/$', 'restaurantes.views.miNegocio'),
    url(r'^mi-negocio/perfil/$', 'restaurantes.views.perfil'),
    url(r'^mi-negocio/datos/$', 'restaurantes.views.datos_negocio'),
    url(r'^mi-negocio/horarios/$', 'restaurantes.views.horario'),

# mi-negocio de control sucursales
    url(r'^mi-negocio/sucursales/nuevo/$', 'restaurantes.views.datos_sucursal'),
    url(r'^mi-negocio/sucursales/$', 'restaurantes.views.lista_sucursal'),
    url(r'^mi-negocio/sucursales/editar/(?P<id_sucursal>\d+)/$', 'restaurantes.views.edita_sucursal'),

# mi-negocio de control Platillos
    url(r'^mi-negocio/platillos/nuevo/$', 'restaurantes.views.nuevo_platillo'),
    url(r'^mi-negocio/platillos/$', 'restaurantes.views.lista_platillo'),
    url(r'^mi-negocio/platillos/editar/(?P<id_platillo>\d+)/$', 'restaurantes.views.edita_platillo'),

    url(r'^salir/$', 'principal.views.salir'),

    url(r'^media/(?P<path>.*)$','django.views.static.serve',
    	{'document_root':settings.MEDIA_ROOT,}
   	),
)
