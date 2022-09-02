from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Categorias(models.Model):
    nombre=models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria=models.ForeignKey(Categorias,on_delete=models.CASCADE,null=True,blank=True)
    nombre=models.CharField(max_length=200)
    descripcion=models.TextField(null=True,blank=True)
    descripcion_corta=models.TextField(null=True,blank=True)
    imagen=models.ImageField(upload_to='juegos',null=True,blank=True)
    precio=models.DecimalField(default=0,max_digits=9, decimal_places=2)

    def __str__(self):
        return self.nombre

class Noticias(models.Model):
    autor=models.CharField(max_length=60, default="Administrador")
    tipo=models.ForeignKey(Categorias,on_delete=models.CASCADE,null=True,blank=True)
    fecha=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    imagen=models.ImageField(upload_to='noticias')
    nombre=models.CharField(max_length=200)
    descripcion=models.TextField()
    visitas=models.IntegerField(default=0)


class Pedidos(models.Model):
    usuario=models.ForeignKey(User, on_delete=models.CASCADE)
    fecha=models.DateField(auto_now_add=True)
    subtotal=models.DecimalField(max_digits=9, decimal_places=2,default=0)
    iva=models.DecimalField(max_digits=9, decimal_places=2,default=0)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    detalle=models.TextField(default="Compra en línea")


class DetallePedido(models.Model):
    pedido=models.ForeignKey(Pedidos,on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        subtotal=float(self.producto.precio)*float(self.cantidad)
        iva=float(subtotal)*0.12
        self.subtotal=subtotal-iva
        self.iva=iva
        self.total=subtotal
        super(DetallePedido,self).save()


class Perfil(models.Model):
    usuario=models.ForeignKey(User, on_delete=models.CASCADE)
    direccion=models.CharField(max_length=200)
    ciudad=models.CharField(max_length=60)
    provincia=models.CharField(max_length=60)
    telefono=models.CharField(max_length=20)

class SobreNosotros(models.Model):
    categoria=models.CharField(max_length=60)
    imagen=models.ImageField(upload_to="nosotros")
    nombre=models.CharField(max_length=60)
    descripcion=models.TextField()

class Pregunta(models.Model):
    titulo=models.CharField(max_length=150)

class Respuesta(models.Model):
    pregunta=models.ForeignKey(Pregunta,on_delete=models.CASCADE)
    respuesta=models.TextField()

