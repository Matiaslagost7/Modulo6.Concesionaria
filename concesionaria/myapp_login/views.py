from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import CustomUser
from concesionaria.myapp_conces.models import Automovil
from concesionaria.myapp_conces.forms import AutomovilForm
from .mixins import verificar_login_y_permisos, solo_login_requerido

# ========================================================================
# VISTAS DE AUTENTICACIÓN - Registro, Login y Logout
# ========================================================================

def RegisterView(request):
    class CustomUserCreationForm(UserCreationForm):
        class Meta:
            model = CustomUser
            fields = ('username', 'email', 'password1', 'password2')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group_name = request.POST.get('group')
            if group_name:
                group = Group.objects.get(name=group_name)
                user.groups.add(group) # Assign user to the selected group
            login(request, user)  # Log the user in after registration
            return redirect('public:index')  # Redirect to a success page.  
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('public:index')
    return render(request, 'login.html')

def LogoutView(request):
    logout(request)
    return render(request, 'logout.html')

# ========================================================================
# VISTAS ADMINISTRATIVAS - Requieren autenticación y permisos específicos
# ========================================================================

def InventarioView(request):
    """
    Vista administrativa para mostrar el inventario completo de automóviles.
    Permite ver todos los vehículos (disponibles y no disponibles).
    Requiere: autenticación + permiso InventarioView (usando mixin súper simple)
    """
    # PASO 1: Verificar login y permisos (súper fácil!)
    resultado = verificar_login_y_permisos(request, 'myapp_login.InventarioView')
    if resultado:  # Si hay problema, redirigir
        return resultado
    
    # PASO 2: Si llegamos aquí, todo está bien, hacer el trabajo normal
    automoviles = Automovil.objects.all().order_by('-id')
    context = {
        'automoviles': automoviles,
        'total_autos': automoviles.count(),
        'autos_disponibles': automoviles.filter(disponible=True).count(),
        'autos_no_disponibles': automoviles.filter(disponible=False).count(),
    }
    return render(request, 'inventario.html', context)

def Crear_AutomovilView(request):
    """
    Vista administrativa para crear un nuevo automóvil.
    Requiere: autenticación + permiso add_auto (usando mixin súper simple)
    """
    # PASO 1: Verificar login y permisos (súper fácil!)
    resultado = verificar_login_y_permisos(request, 'myapp_conces.add_auto')
    if resultado:  # Si hay problema, redirigir
        return resultado
    
    # PASO 2: Si llegamos aquí, todo está bien, hacer el trabajo normal
    if request.method == 'POST':
        form = AutomovilForm(request.POST, request.FILES)
        if form.is_valid():
            automovil = form.save()
            messages.success(request, f'Automóvil {automovil.marca} {automovil.modelo} creado exitosamente.')
            return redirect('inventario')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = AutomovilForm()
    
    return render(request, 'crear_automovil.html', {'form': form})

@solo_login_requerido
def Detalle_AutomovilView(request, automovil_id):
    """
    Vista administrativa para mostrar detalles completos de un automóvil.
    Incluye información administrativa no visible en la vista pública.
    Requiere: solo login (usando decorador súper simple)
    """
    automovil = get_object_or_404(Automovil, id=automovil_id)
    return render(request, 'detalle_automovil.html', {'automovil': automovil})


def Editar_AutomovilView(request, automovil_id):
    """
    Vista administrativa para editar un automóvil existente.
    Requiere: autenticación + permiso change_auto
    """
    # PASO 1: Verificar login y permisos (súper fácil!)
    resultado = verificar_login_y_permisos(request, 'myapp_conces.change_auto')
    if resultado:  # Si hay problema, redirigir
        return resultado
    
    # PASO 2: Si llegamos aqui, todo está bien, hacer el trabajo normal
    automovil = get_object_or_404(Automovil, id=automovil_id)
    
    if request.method == 'POST':
        form = AutomovilForm(request.POST, request.FILES, instance=automovil)
        if form.is_valid():
            form.save()
            messages.success(request, f'Automóvil {automovil.marca} {automovil.modelo} actualizado exitosamente.')
            return redirect('inventario')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = AutomovilForm(instance=automovil)
    
    return render(request, 'editar_automovil.html', {'form': form, 'automovil': automovil})

@login_required(login_url='login')
@permission_required('myapp_conces.delete_auto', raise_exception=True)
def Eliminar_AutomovilView(request, automovil_id):
    """
    Vista administrativa para eliminar un automóvil existente.
    Requiere: autenticación + permiso delete_auto
    """
    automovil = get_object_or_404(Automovil, id=automovil_id)
    
    if request.method == 'POST':
        marca_modelo = f"{automovil.marca} {automovil.modelo}"
        automovil.delete()
        messages.success(request, f'Automóvil {marca_modelo} eliminado exitosamente.')
        return redirect('inventario')
    
    return render(request, 'eliminar_automovil.html', {'automovil': automovil})
