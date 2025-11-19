from django.contrib import admin
# Agregamos los nuevos modelos a la importación
from .models import Empleado, Huesped, Habitacion, Reserva, ServicioAdicional, Renta

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cargo', 'salario', 'turno', 'telefono')
    list_filter = ('cargo', 'turno')
    search_fields = ('nombre', 'apellido')

@admin.register(Huesped)
class HuespedAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono', 'email', 'fecha_registro', 'registrado_por')
    list_filter = ('fecha_registro',)
    search_fields = ('nombre', 'apellido', 'email')
    filter_horizontal = ('habitaciones',)

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo', 'capacidad', 'precio_por_noche', 'disponibles', 'piso', 'estado_limpieza')
    list_filter = ('tipo', 'disponibles', 'piso', 'estado_limpieza')
    search_fields = ('numero',)

# --- NUEVAS TABLAS AGREGADAS ---

@admin.register(ServicioAdicional)
class ServicioAdicionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo', 'descripcion', 'creado_en')
    search_fields = ('nombre',)
    list_filter = ('creado_en',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    # Muestra ID, cliente, habitación y fechas clave
    list_display = ('id', 'cliente', 'habitacion', 'fecha_entrada', 'fecha_salida', 'estado')
    list_filter = ('estado', 'fecha_entrada')
    # Permite buscar por nombre del cliente o número de habitación
    search_fields = ('cliente__nombre', 'cliente__apellido', 'habitacion__numero')
    date_hierarchy = 'fecha_entrada'

@admin.register(Renta)
class RentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'fecha_checkin_real', 'monto_total', 'pagado')
    list_filter = ('pagado', 'fecha_checkin_real')
    search_fields = ('reserva__cliente__nombre',)
    # filter_horizontal crea un selector visual cómodo para los servicios (Many-to-Many)
    filter_horizontal = ('servicios_consumidos',)