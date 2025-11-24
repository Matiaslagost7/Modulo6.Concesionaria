from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Automovil, Carrito, ItemCarrito, Compra
from .forms import ContactoForm

# Vista para la página de inicio
def index(request):
    """
    Vista para la página de inicio.
    """
    return render(request, 'index.html')

# Vista para el formulario de contacto
def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Procesar el formulario
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            mensaje = form.cleaned_data['mensaje']
            # Aquí podrías enviar un correo o guardar el mensaje en la base de datos
            return render(request, 'contacto_exito.html', {'nombre': nombre})
    else:
        form = ContactoForm()
    return render(request, 'contacto.html', {'form': form})

# Vista para mostrar el catálogo de automóviles
def catalogo(request):
    automoviles = Automovil.objects.all()
    if not automoviles:
        mensaje = "No hay automóviles disponibles en el catálogo."
        return render(request, 'catalogo.html', {'mensaje': mensaje})
    
    return render(request, 'catalogo.html', {'automoviles': automoviles})

# ========================================================================
# NOTA: Las vistas de administración (inventario, crear, editar, eliminar)
# han sido movidas a myapp_login/views.py para mantener separación clara
# entre funcionalidades públicas y administrativas
# ========================================================================

# Vista pública para mostrar el detalle de un automóvil
def detalle_automovil(request, automovil_id):
    """
    Vista pública para mostrar los detalles de un automóvil específico.
    Esta es la vista pública del catálogo, sin requerir autenticación.
    """
    try:
        automovil = Automovil.objects.get(id=automovil_id, disponible=True)
        return render(request, 'detalle_auto.html', {'auto': automovil})
    except Automovil.DoesNotExist:
        return render(request, 'catalogo.html', {
            'mensaje': 'El automóvil solicitado no está disponible.'
        })

# Vista para buscar automóviles en el catálogo público
def buscar_automovil(request):
    """
    Vista pública para buscar automóviles en el catálogo.
    """
    query = request.GET.get('q', '')
    resultados = []
    
    if query:
        resultados = Automovil.objects.filter(
            (models.Q(marca__icontains=query) | models.Q(modelo__icontains=query)),
            disponible=True
        )
    
    return render(request, 'buscar_automovil.html', {
        'resultados': resultados, 
        'query': query
    })


# ===================== PROCESO DE COMPRA =====================

@login_required
def agregar_al_carrito(request, automovil_id):
    auto = get_object_or_404(Automovil, id=automovil_id, disponible=True)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user, activo=True)
    item, creado_item = ItemCarrito.objects.get_or_create(carrito=carrito, automovil=auto)
    if not creado_item:
        item.cantidad += 1
        item.save()
    messages.success(request, f"{auto} agregado al carrito.")
    return redirect('public:catalogo')



from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse

def ver_carrito(request):
    if not request.user.is_authenticated:
        # Carrito solo en sesión para usuarios no autenticados
        items = []
        total = 0
        # Si se quiere implementar carrito para no autenticados, aquí se puede usar session
        return render(request, 'carrito.html', {'carrito': None, 'items': items, 'total': total})
    else:
        carrito = Carrito.objects.filter(usuario=request.user, activo=True).first()
        items = carrito.items.all() if carrito else []
        total = sum(item.automovil.precio * item.cantidad for item in items)
        return render(request, 'carrito.html', {'carrito': carrito, 'items': items, 'total': total})


@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user, carrito__activo=True)
    item.delete()
    messages.info(request, "Auto eliminado del carrito.")
    return redirect('public:ver_carrito')


@login_required
def finalizar_compra(request):
    carrito = Carrito.objects.filter(usuario=request.user, activo=True).first()
    if not carrito or not carrito.items.exists():
        messages.error(request, "El carrito está vacío.")
        return redirect('public:ver_carrito')
    total = sum(item.automovil.precio * item.cantidad for item in carrito.items.all())
    # Descontar cantidad y marcar como no disponible si llega a 0
    for item in carrito.items.all():
        auto = item.automovil
        if auto.cantidad >= item.cantidad:
            auto.cantidad -= item.cantidad
        else:
            auto.cantidad = 0
        # Actualizar disponibilidad según cantidad
        if auto.cantidad > 0:
            auto.disponible = True
        else:
            auto.disponible = False
        auto.save()
    compra = Compra.objects.create(usuario=request.user, carrito=carrito, total=total)
    carrito.activo = False
    carrito.save()
    messages.success(request, "¡Compra realizada con éxito!")
    return render(request, 'compra_exitosa.html', {'compra': compra})

