from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from aplicacion.models import PerfilUsuario
from .forms import CustomAuthenticationForm
from .models import Producto, ItemCarrito, Pedido
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer



from transbank.webpay.webpay_plus.transaction import Transaction
 


# Vistas normales
def index(request):
    return render(request, 'index.html')

def quienes_somos(request):
    return render(request, 'quienes_somos.html')

def catalogo(request):
    productos = Producto.objects.all()  # Obtiene todos los productos disponibles
    return render(request, 'catalogo.html', {'productos': productos})

def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'producto_detalle.html', {'producto': producto})

def agregar_al_carrito(request):
    return render(request, 'agregar_al_carrito.html')

def buscar_producto(request):
    query = request.GET.get('q', '')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.none()

    return render(request, 'catalogo.html', {'productos': productos})


def proceder_pago(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirigir al login si el usuario no está autenticado

    items = ItemCarrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in items)

    if request.method == 'POST':
        # Aquí iría la lógica para procesar el pago
        # Por ejemplo, integrar con un sistema de pagos como PayPal o Stripe
        return redirect('confirmacion_pago')  # Suponiendo que existe una vista de confirmación de pago
    

    return render(request, 'proceder_pago.html', {'items': items, 'total': total})

def vision(request):
    return render(request, 'vision.html')

# Vista de registro
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Asegúrate de que los nombres de los campos coincidan con los definidos en tu formulario
            user.first_name = form.cleaned_data.get('first_name', '')  #  get para evitar KeyError
            user.last_name = form.cleaned_data.get('last_name', '')  # get para evitar KeyError
            user.save()

            # Si tienes un perfil u otra información para guardar, maneja eso aquí
            # Omitido para simplificación

            login(request, user)
            return redirect('index')  # Asume que 'index' es la URL a la que quieres redirigir después del registro
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Vista de login personalizada
def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Vista de logout
def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirige al login después de cerrar sesión


@login_required
def ver_carrito(request):
    items = ItemCarrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in items)
    
    # 🔹 Contador de productos en el carrito
    cart_count = sum(item.cantidad for item in items)  

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            item_id = request.POST.get('eliminar')
            item = ItemCarrito.objects.get(id=item_id, usuario=request.user)
            item.delete()
            return redirect('ver_carrito')
    
    if not items:
        return render(request, 'carrito_vacio.html', {"cart_count": cart_count})

    return render(request, 'carrito.html', {'items': items, 'total': total, 'cart_count': cart_count})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    item, created = ItemCarrito.objects.get_or_create(usuario=request.user, producto=producto)
    if not created:
        if item.cantidad < item.producto.stock:
            item.cantidad += 1
            item.save()

    request.session.modified = True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = ItemCarrito.objects.filter(usuario=request.user).count()
        return JsonResponse({'cart_count': cart_count})
    else:
        return redirect('ver_carrito')



@login_required
def eliminar_del_carrito(request, item_id):
    item = ItemCarrito.objects.get(id=item_id, usuario=request.user)
    item.delete()
    return redirect('ver_carrito')


#WEBPAY

def iniciar_pago(request):
    if not request.user.is_authenticated:
        return redirect("login")

    items = ItemCarrito.objects.filter(usuario=request.user)
    if not items:
        return redirect("ver_carrito")  # Si el carrito está vacío, redirige

    total = sum(item.producto.precio * item.cantidad for item in items)

    tx = Transaction()
    buy_order = f"Orden-{request.user.id}-01-{Pedido.objects.filter(usuario=request.user).count() + 1}2025"
    session_id = str(request.user.id)
    return_url = request.build_absolute_uri("/webpay/respuesta/")


    response = tx.create(buy_order, session_id, total, return_url)

    # Guardar transacción en la BD (opcional)
    pedido = Pedido.objects.create(usuario=request.user, total=total, estado="pendiente")
    
    return redirect(response["url"] + "?token_ws=" + response["token"])

def respuesta(request):
    token = request.GET.get("token_ws", None)
    if not token:
        return redirect("ver_carrito")  # Si no hay token, redirige al carrito

    tx = Transaction()
    response = tx.commit(token)

    if response["status"] == "AUTHORIZED":
        pedido = Pedido.objects.filter(usuario=request.user, estado="pendiente").first()

        pedido.estado = "pagado"
        pedido.transaction_id = token
        pedido.save()
        
        # Vaciar el carrito después del pago exitoso
        ItemCarrito.objects.filter(usuario=request.user).delete()
        request.session["cart_count"] = 0  # Reiniciar contador del carrito

        
        return render(request, "webpay/exito.html", {"response": response})
    
    else:
        return render(request, "webpay/error.html", {"response": response})
    
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige al login después del registro
    else:
        form = RegistroUsuarioForm()

    return render(request, 'register.html', {'form': form})