"""tienda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Juegos.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('registro',registro, name='registro'),
    path('tienda',shop, name='tienda'),
    path('noticias',noticias, name='noticias'),
    path('nosotros',nosotros, name='nosotros'),
    path('carrito',carrito, name='carrito'),
    path('producto',detalles_producto, name='producto'),
    path('sesion',iniciarSesion,name='sesion'),
    path('salir',cerrarSesion,name='cerrarSesion'),
    path('datos',datos,name='datos'),
    path('perfil',perfil,name='perfil'),
    path('pagar',pagar,name='pagar'),

]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
