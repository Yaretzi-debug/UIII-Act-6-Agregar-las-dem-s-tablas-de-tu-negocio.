from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import Empleado, Huesped, Habitacion, Reserva, ServicioAdicional, Renta

def inicio_hotel(request):
    return render(request, 'inicio.html')

# --- VISTAS EMPLEADOS ---
def agregar_empleados(request):
    if request.method == 'POST':
        empleado = Empleado(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            cargo=request.POST['cargo'],
            fecha_contratacion=request.POST['fecha_contratacion'],
            salario=request.POST['salario'],
            turno=request.POST['turno'],
            telefono=request.POST['telefono']
        )
        empleado.save()
        return redirect('ver_empleados')
    return render(request, 'empleados/agregar_empleados.html')

def ver_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/ver_empleados.html', {'empleados': empleados})

def actualizar_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/actualizar_empleados.html', {'empleados': empleados})

def realizar_actualizacion_empleados(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.nombre = request.POST['nombre']
        empleado.apellido = request.POST['apellido']
        empleado.cargo = request.POST['cargo']
        empleado.fecha_contratacion = request.POST['fecha_contratacion']
        empleado.salario = request.POST['salario']
        empleado.turno = request.POST['turno']
        empleado.telefono = request.POST['telefono']
        empleado.save()
        return redirect('ver_empleados')
    return render(request, 'empleados/actualizar_empleados_form.html', {'empleado': empleado})

def borrar_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/borrar_empleados.html', {'empleados': empleados})

def realizar_borrado_empleados(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('ver_empleados')
    return render(request, 'empleados/confirmar_borrado.html', {'empleado': empleado})

# --- VISTAS HUESPEDES ---
def agregar_huesped(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Huesped.objects.filter(email=email).exists():
            mensaje_error = "El email ya está registrado."
            empleados = Empleado.objects.all()
            habitaciones = Habitacion.objects.filter(disponibles=True)
            return render(request, 'huespedes/agregar_huesped.html', {
                'empleados': empleados, 'habitaciones': habitaciones, 'error_message': mensaje_error, 'form_data': request.POST
            })
        try:
            empleado_id = request.POST.get('registrado_por')
            empleado = Empleado.objects.get(id=empleado_id) if (empleado_id and empleado_id != '') else None
            huesped = Huesped(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                telefono=request.POST['telefono'],
                email=email,
                direccion=request.POST['direccion'],
                registrado_por=empleado
            )
            huesped.save()
            habitaciones_ids = request.POST.getlist('habitaciones')
            if habitaciones_ids:
                habitaciones = Habitacion.objects.filter(id__in=habitaciones_ids)
                huesped.habitaciones.set(habitaciones)
            return redirect('ver_huespedes')
        except Exception as e:
            empleados = Empleado.objects.all()
            habitaciones = Habitacion.objects.filter(disponibles=True)
            return render(request, 'huespedes/agregar_huesped.html', {
                'empleados': empleados, 'habitaciones': habitaciones, 'error_message': str(e)
            })
    
    empleados = Empleado.objects.all()
    habitaciones = Habitacion.objects.filter(disponibles=True)
    return render(request, 'huespedes/agregar_huesped.html', {'empleados': empleados, 'habitaciones': habitaciones})

def ver_huespedes(request):
    huespedes = Huesped.objects.all()
    return render(request, 'huespedes/ver_huespedes.html', {'huespedes': huespedes})

def actualizar_huesped(request):
    huespedes = Huesped.objects.all()
    return render(request, 'huespedes/actualizar_huesped.html', {'huespedes': huespedes})

def realizar_actualizacion_huesped(request, huesped_id):
    huesped = get_object_or_404(Huesped, id=huesped_id)
    if request.method == 'POST':
        huesped.nombre = request.POST['nombre']
        huesped.apellido = request.POST['apellido']
        huesped.telefono = request.POST['telefono']
        huesped.email = request.POST['email']
        huesped.direccion = request.POST['direccion']
        empleado_id = request.POST.get('registrado_por')
        huesped.registrado_por = Empleado.objects.get(id=empleado_id) if (empleado_id and empleado_id != '') else None
        huesped.save()
        habitaciones_ids = request.POST.getlist('habitaciones')
        habitaciones = Habitacion.objects.filter(id__in=habitaciones_ids)
        huesped.habitaciones.set(habitaciones)
        return redirect('ver_huespedes')
    
    empleados = Empleado.objects.all()
    habitaciones = Habitacion.objects.filter(disponibles=True)
    return render(request, 'huespedes/actualizar_huesped_form.html', {
        'huesped': huesped, 'empleados': empleados, 'habitaciones': habitaciones
    })

def borrar_huesped(request):
    huespedes = Huesped.objects.all()
    return render(request, 'huespedes/borrar_huesped.html', {'huespedes': huespedes})

def realizar_borrado_huesped(request, huesped_id):
    huesped = get_object_or_404(Huesped, id=huesped_id)
    if request.method == 'POST':
        huesped.delete()
        return redirect('ver_huespedes')
    return render(request, 'huespedes/confirmar_borrado_huesped.html', {'huesped': huesped})

# --- VISTAS HABITACIONES ---
def agregar_habitacion(request):
    if request.method == 'POST':
        habitacion = Habitacion(
            numero=request.POST['numero'],
            tipo=request.POST['tipo'],
            capacidad=request.POST['capacidad'],
            precio_por_noche=request.POST['precio_por_noche'],
            disponibles='disponibles' in request.POST,
            piso=request.POST['piso'],
            estado_limpieza=request.POST['estado_limpieza']
        )
        habitacion.save()
        return redirect('ver_habitaciones')
    return render(request, 'habitacion/agregar_habitacion.html')

def ver_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'habitacion/ver_habitaciones.html', {'habitaciones': habitaciones})

def actualizar_habitacion(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'habitacion/actualizar_habitacion.html', {'habitaciones': habitaciones})

def realizar_actualizacion_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    if request.method == 'POST':
        habitacion.numero = request.POST['numero']
        habitacion.tipo = request.POST['tipo']
        habitacion.capacidad = request.POST['capacidad']
        habitacion.precio_por_noche = request.POST['precio_por_noche']
        habitacion.disponibles = 'disponibles' in request.POST
        habitacion.piso = request.POST['piso']
        habitacion.estado_limpieza = request.POST['estado_limpieza']
        habitacion.save()
        return redirect('ver_habitaciones')
    return render(request, 'habitacion/actualizar_habitacion_form.html', {'habitacion': habitacion})

def borrar_habitacion(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'habitacion/borrar_habitacion.html', {'habitaciones': habitaciones})

def realizar_borrado_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    if request.method == 'POST':
        habitacion.delete()
        return redirect('ver_habitaciones')
    return render(request, 'habitacion/confirmar_borrado_habitacion.html', {'habitacion': habitacion})

# --- VISTAS RESERVAS ---
def ver_reservas(request):
    reservas = Reserva.objects.all().order_by('-fecha_reserva')
    return render(request, 'reservas/ver_reservas.html', {'reservas': reservas})

def agregar_reserva(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        habitacion_id = request.POST.get('habitacion')
        cliente = Huesped.objects.get(id=cliente_id)
        habitacion = Habitacion.objects.get(id=habitacion_id)
        reserva = Reserva(
            cliente=cliente,
            habitacion=habitacion,
            fecha_entrada=request.POST['fecha_entrada'],
            fecha_salida=request.POST['fecha_salida'],
            observaciones=request.POST['observaciones'],
            estado='PEN'
        )
        reserva.save()
        return redirect('ver_reservas')

    huespedes = Huesped.objects.all()
    habitaciones = Habitacion.objects.all()
    return render(request, 'reservas/agregar_reserva.html', {
        'huespedes': huespedes,
        'habitaciones': habitaciones
    })

def realizar_actualizacion_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        reserva.cliente = Huesped.objects.get(id=request.POST.get('cliente'))
        reserva.habitacion = Habitacion.objects.get(id=request.POST.get('habitacion'))
        reserva.fecha_entrada = request.POST['fecha_entrada']
        reserva.fecha_salida = request.POST['fecha_salida']
        reserva.estado = request.POST['estado']
        reserva.observaciones = request.POST['observaciones']
        reserva.save()
        return redirect('ver_reservas')

    huespedes = Huesped.objects.all()
    habitaciones = Habitacion.objects.all()
    return render(request, 'reservas/actualizar_reserva.html', {
        'reserva': reserva, 'huespedes': huespedes, 'habitaciones': habitaciones
    })

def realizar_borrado_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        reserva.delete()
        return redirect('ver_reservas')
    return render(request, 'reservas/borrar_reserva.html', {'reserva': reserva})

# --- VISTAS SERVICIOS ---
def ver_servicios(request):
    servicios = ServicioAdicional.objects.all()
    return render(request, 'servicios/ver_servicios.html', {'servicios': servicios})

def agregar_servicio(request):
    if request.method == 'POST':
        servicio = ServicioAdicional(
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion'],
            costo=request.POST['costo']
        )
        servicio.save()
        return redirect('ver_servicios')
    return render(request, 'servicios/agregar_servicio.html')

def realizar_actualizacion_servicio(request, servicio_id):
    servicio = get_object_or_404(ServicioAdicional, id=servicio_id)
    if request.method == 'POST':
        servicio.nombre = request.POST['nombre']
        servicio.descripcion = request.POST['descripcion']
        servicio.costo = request.POST['costo']
        servicio.save()
        return redirect('ver_servicios')
    return render(request, 'servicios/actualizar_servicio.html', {'servicio': servicio})

def realizar_borrado_servicio(request, servicio_id):
    servicio = get_object_or_404(ServicioAdicional, id=servicio_id)
    if request.method == 'POST':
        servicio.delete()
        return redirect('ver_servicios')
    return render(request, 'servicios/borrar_servicio.html', {'servicio': servicio})

# --- VISTAS RENTAS (ACTUALIZADO) ---
def ver_rentas(request):
    rentas = Renta.objects.all() # O tu consulta específica
    return render(request, 'rentas/ver_rentas.html', {'rentas': rentas})

def agregar_renta(request):
    if request.method == 'POST':
        # 1. Capturar datos del formulario
        reserva_id = request.POST.get('reserva')
        empleado_id = request.POST.get('empleado_seleccionado')
        monto_base = request.POST.get('monto_renta')
        deposito = request.POST.get('deposito')
        observaciones = request.POST.get('observaciones_servicio')
        pagado = 'pagado' in request.POST
        
        reserva = get_object_or_404(Reserva, id=reserva_id)
        
        # Obtener empleado
        empleado = None
        if empleado_id:
            empleado = Empleado.objects.get(id=empleado_id)
            
        # Validar montos vacíos
        monto_base_float = float(monto_base) if monto_base else 0.0
        deposito_float = float(deposito) if deposito else 0.0
        
        # 2. Crear Renta
        renta = Renta(
            reserva=reserva,
            pagado=pagado,
            empleado=empleado,
            deposito=deposito_float,
            observaciones=observaciones,
            monto_total=monto_base_float
        )
        renta.save()
        
        # 3. Guardar servicios seleccionados
        servicios_ids = request.POST.getlist('servicios')
        if servicios_ids:
            servicios = ServicioAdicional.objects.filter(id__in=servicios_ids)
            renta.servicios_consumidos.set(servicios)
            
            # Sumar costos de servicios al total
            total_final = monto_base_float
            for s in servicios:
                total_final += float(s.costo)
            
            renta.monto_total = total_final
            renta.save()
            
        return redirect('ver_rentas')

    # GET REQUEST
    reservas_disponibles = Reserva.objects.filter(renta__isnull=True)
    servicios = ServicioAdicional.objects.all()
    lista_empleados = Empleado.objects.all() # Lista para el selector

    return render(request, 'rentas/agregar_renta.html', {
        'reservas_disponibles': reservas_disponibles,
        'servicios': servicios,
        'lista_empleados': lista_empleados
    })

def realizar_actualizacion_renta(request, renta_id):
    renta = get_object_or_404(Renta, id=renta_id)
    if request.method == 'POST':
        renta.monto_total = request.POST['monto_total']
        renta.pagado = 'pagado' in request.POST
        renta.save()
        servicios_ids = request.POST.getlist('servicios')
        servicios = ServicioAdicional.objects.filter(id__in=servicios_ids)
        renta.servicios_consumidos.set(servicios)
        return redirect('ver_rentas')

    servicios = ServicioAdicional.objects.all()
    return render(request, 'rentas/actualizar_renta.html', {'renta': renta, 'servicios': servicios})

def realizar_borrado_renta(request, renta_id):
    renta = get_object_or_404(Renta, id=renta_id)
    if request.method == 'POST':
        renta.delete()
        return redirect('ver_rentas')
    return render(request, 'rentas/borrar_renta.html', {'renta': renta})

def detalle_renta(request, pk):
    renta = get_object_or_404(Renta, pk=pk)
    return render(request, 'rentas/detalle_renta.html', {'renta': renta})