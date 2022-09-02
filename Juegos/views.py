from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from Juegos.models import Producto, Categorias, Noticias, Pedidos, Perfil, DetallePedido, SobreNosotros, Pregunta


def index(request):
    contexto={
        'juegos':Producto.objects.all().order_by("-id")
    }
    return render(request,'index.html',contexto)

@login_required(login_url='/')
def perfil(request):
    pedido=None
    if request.GET.get('id'):
        pedido=Pedidos.objects.get(id=request.GET.get('id'))
    if request.GET.get('pedido'):
        pedido = Pedidos.objects.get(id=request.GET.get('pedido'))
    contexto={
        'pedidos':Pedidos.objects.all(),
        'pedido':pedido,

    }
    return render(request, 'mispedidos.html',contexto)

def iniciarSesion(request):
    if request.POST:
        print(request.POST)
        email=request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request,user)
            messages.add_message(request,messages.INFO,'Bienvenido: %s'%user.username)
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Error al iniciar sesión intente nuevamente..!')
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

@login_required(login_url='/')
def cerrarSesion(request):
    logout(request)
    messages.add_message(request, messages.INFO,'La sesión se cerro existosamente')
    return HttpResponseRedirect('/')



def registro(request):
    if request.POST:
        email = request.POST.get('email')
        p1 = request.POST.get('p1')
        p2 = request.POST.get('p2')
        print(request.POST)
        if p1 == p2:
            try:
                usuario=User.objects.create(username=email,email=email)
                usuario.set_password(p1)
                usuario.save()
                usuario.is_active=True
                messages.add_message(request, messages.SUCCESS, 'El registro se ha creado exitosamente')
            except:
                messages.add_message(request,messages.INFO,'No es posible crear el usuario debido a que el email proporcionado ya esta registrado')
        else:
            messages.add_message(request,messages.ERROR,'Las contraseñas no coinciden, Reintente')

    return render(request,'registro.html')

def shop(request):
    productos=Producto.objects.all()
    if request.GET.get('id'):
        productos=productos.filter(categoria_id=request.GET.get('id'))
    if request.GET.get('s'):
        query=request.GET.get('s')
        productos=productos.filter(Q(nombre__icontains=query)|Q(descripcion__icontains=query))
    paginator = Paginator(productos, 15)  # ver 15 por pagina.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj,page_number)
    contexto={
        'categorias':Categorias.objects.all().order_by('nombre'),
        'productos':page_obj,
        'paginator':paginator,
    }
    print(paginator.num_pages)
    return render(request,'tienda.html',contexto)

def detalles_producto(request):
    contexto={
        'producto':Producto.objects.get(id=request.GET.get('id'))
    }
    return render(request,'producto.html',contexto)

def noticias(request):
    notas=Noticias.objects.all().order_by('-id')
    nota=None
    if request.GET.get('s'):
        nota=notas.filter(Q(nombre__icontains=request.GET.get('s'))|Q(descripcion__icontains=request.GET.get('s')))
    paginator = Paginator(notas, 15)  # ver 15 por pagina.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj, page_number)

    if request.GET.get('id'):
        nota=notas.get(id=request.GET.get('id'))
        nota.visitas+=1
        nota.save()


    contexto={
        'noticias':page_obj,
        'paginator':paginator,
        'noticia':nota,
    }
    return render(request,'noticias.html',contexto)

def obtenerCategorias():
    lista=[]
    for cat in SobreNosotros.objects.all():
        lista.append(cat.categoria)
    lista=list(set(lista))
    print(lista)
    return lista

def nosotros(request):
    obtenerCategorias()
    contexto={
        'nosotros':SobreNosotros.objects.all(),
        'categorias':obtenerCategorias(),
        'preguntas':Pregunta.objects.all().order_by('-id')
    }
    return render(request,'nosotros.html',contexto)

def carrito(request):
    contexto={

    }
    return render(request,'carrito.html',contexto)

def pagar(request):
    perfil=None
    try:
        perfil=Perfil.objects.get(usuario=request.user)
    except:
        return HttpResponseRedirect('/datos')
    if request.POST:
        ids = request.POST.get('ids').split(',')
        try:
            if len(request.POST.get('ids').split())>=1:
                pedido=Pedidos(
                    usuario=request.user,
                    subtotal=request.POST.get('subtotal'),
                    iva = request.POST.get('iva'),
                    total=request.POST.get('total')
                )
                pedido.save()

                cantidades=request.POST.get('cantidades').split(',')

                for i in range(len(ids)):
                    print(ids[i],cantidades[i])
                    deta=DetallePedido(
                        pedido=pedido,
                        producto_id=ids[i],
                        cantidad=cantidades[i]
                    ).save()
                messages.add_message(request,messages.INFO,"El pedido se registro correctamente.")
                return HttpResponseRedirect('/perfil')
            else:
                messages.add_message(request, messages.INFO, "Primero agregue productos al carrito.")
        except:
            messages.add_message(request, messages.INFO, "Primero agregue productos al carrito.")
    contexto={
        'perfil':perfil
    }
    return render(request,'pago.html',contexto)

@login_required(login_url='/')
def datos(request):
    perfil = None
    try:
        perfil = Perfil.objects.get(usuario=request.user)
    except:
        perfil = Perfil()

    if request.POST:
        print(request.POST)
        user=request.user
        user.first_name=request.POST.get('nombres')
        user.last_name=request.POST.get('apellidos')
        user.save()
        try:
            perfil=Perfil.objects.get(usuario=user)
        except:
            perfil=Perfil()
            perfil.usuario=user
        perfil.direccion=request.POST.get('direccion')
        perfil.ciudad = request.POST.get('ciudad')
        perfil.provincia = request.POST.get('provincia')
        perfil.telefono = request.POST.get('telefono')
        perfil.save()
        messages.add_message(request,messages.INFO,'Los datos del usuario han sido actualizados')
    contexto={
       'perfil':perfil
    }
    return render(request,'datos.html',contexto)