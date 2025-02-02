from django.contrib import admin
from .models import Categoria, Producto, PerfilUsuario, Pedido, DetallePedido, Pago

# Register your models here.


admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(PerfilUsuario)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Pago)
