from django.contrib import admin

# Register your models here.
from Juegos.models import *
from tienda.snniper import Attr

@admin.register(Categorias)
class modelo(admin.ModelAdmin):
    list_display =Attr(Categorias)
    list_display_links =Attr(Categorias)

@admin.register(Producto)
class modelo(admin.ModelAdmin):
    list_display =Attr(Producto)
    list_display_links =Attr(Producto)

@admin.register(Noticias)
class modelo(admin.ModelAdmin):
    list_display =Attr(Noticias)
    list_display_links =Attr(Noticias)

class DetallePedidoInline(admin.StackedInline):
    model = DetallePedido
    extra = 0

@admin.register(Pedidos)
class modelo(admin.ModelAdmin):
    list_display =Attr(Pedidos)
    list_display_links =Attr(Pedidos)
    inlines = [DetallePedidoInline]

@admin.register(Perfil)
class modelo(admin.ModelAdmin):
    list_display =Attr(Perfil)
    list_display_links =Attr(Perfil)

@admin.register(SobreNosotros)
class modelo(admin.ModelAdmin):
    list_display =Attr(SobreNosotros)
    list_display_links =Attr(SobreNosotros)

class RepuestaInline(admin.StackedInline):
    model = Respuesta
    extra = 0

@admin.register(Pregunta)
class modelo(admin.ModelAdmin):
    list_display =Attr(Pregunta)
    list_display_links =Attr(Pregunta)
    inlines = [RepuestaInline]