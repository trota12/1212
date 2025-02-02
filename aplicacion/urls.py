from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet
from django.urls import path, include




from .views import iniciar_pago, respuesta
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('vision/', views.vision, name='vision'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('producto_detalle/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),  # Corregido
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar-del-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('buscar/', views.buscar_producto, name='buscar_producto'),
    path('webpay/iniciar_pago/', iniciar_pago, name='iniciar_pago'),
    path('webpay/respuesta/', respuesta, name='respuesta'),
    path('api/', include(router.urls)),  # Ruta para la API
]
