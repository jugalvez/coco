from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^cocopanel/doc/', include('django.contrib.admindocs.urls')),
    url(r'^cocopanel/', include(admin.site.urls)),

    url(r'^ajax/(?P<id>\d+)$', 'principal.views.ajax'),

    url(r'^$', 'principal.views.acerca'),
    url(r'^buscar/$', 'principal.views.busqueda'),
    url(r'^registro/$', 'principal.views.registro'),
    url(r'^login/$', 'principal.views.login'),
    url(r'^registro/$', 'principal.views.registro'),

    url(r'^panel/perfil/$', 'principal.views.perfil'),
    url(r'^panel/datos/$', 'principal.views.datos_negocio'),
    
    url(r'^panel/sucursales/nuevo/$', 'principal.views.datos_sucursal'),
    url(r'^panel/sucursales/$', 'principal.views.lista_sucursal'),
    url(r'^panel/sucursales/editar/(?P<id_sucursal>\d+)/$', 'principal.views.edita_sucursal'),

    url(r'^panel/platillos/nuevo/$', 'principal.views.nuevo_platillo'),
    url(r'^panel/platillos/$', 'principal.views.lista_platillo'),
    url(r'^panel/platillos/editar/(?P<id_platillo>\d+)/$', 'principal.views.edita_platillo'),

    url(r'^salir/$', 'principal.views.salir'),

    url(r'^(?P<restaurant>[-_\w]+)/(?P<platillo>[-_\w]+)/$', 'principal.views.platillo'),
    url(r'^sitio/(?P<id_negocio>\d+)$', 'principal.views.sitio'),

    url(r'^media/(?P<path>.*)$','django.views.static.serve',
    	{'document_root':settings.MEDIA_ROOT,}
   	),
)
