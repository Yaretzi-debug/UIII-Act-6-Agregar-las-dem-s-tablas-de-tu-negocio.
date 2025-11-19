from django.db import models

# --- Modelo Empleado ---
class Empleado(models.Model):
    CARGOS = (
        ('GER', 'Gerente'),
        ('REC', 'Recepcionista'),
        ('LIM', 'Personal de Limpieza'),
        ('OTR', 'Otro'),
    )
    TURNOS = (
        ('MAN', 'Mañana'),
        ('TAR', 'Tarde'),
        ('NOCH', 'Noche'),
    )

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=3, choices=CARGOS, default='OTR')
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    turno = models.CharField(max_length=4, choices=TURNOS)
    telefono = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.get_cargo_display()}'

    class Meta:
        verbose_name_plural = "Empleados"
        ordering = ['apellido']

# --- Modelo Habitación ---
class Habitacion(models.Model):
    TIPOS_HABITACION = (
        ('IND', 'Individual'),
        ('DOB', 'Doble'),
        ('SUI', 'Suite'),
        ('FAM', 'Familiar'),
    )
    ESTADOS_LIMPIEZA = (
        ('LIM', 'Limpia'),
        ('SUC', 'Sucia'),
        ('MNT', 'En Mantenimiento'),
    )

    numero = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=3, choices=TIPOS_HABITACION)
    capacidad = models.IntegerField(help_text='Máximo número de personas.')
    precio_por_noche = models.DecimalField(max_digits=8, decimal_places=2)
    disponibles = models.BooleanField(default=True, help_text='Indica si la habitación está lista para ser reservada.')
    piso = models.IntegerField()
    estado_limpieza = models.CharField(max_length=3, choices=ESTADOS_LIMPIEZA, default='LIM')

    def __str__(self):
        return f'Hab. N° {self.numero} ({self.get_tipo_display()})'

    class Meta:
        verbose_name_plural = "Habitaciones"
        ordering = ['numero']

# --- Modelo Huesped ---
class Huesped(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    direccion = models.TextField()

    registrado_por = models.ForeignKey(
        Empleado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='huespedes_registrados',
        help_text='Empleado que realizó el registro del huésped.'
    )

    habitaciones = models.ManyToManyField(
        Habitacion,
        related_name='huespedes_actuales',
        blank=True,
        help_text='Habitaciones actualmente ocupadas por este huésped.'
    )

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    class Meta:
        verbose_name_plural = "Huéspedes"
        ordering = ['apellido']

# --- Modelo Servicios Adicionales ---
class ServicioAdicional(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=8, decimal_places=2)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Servicio Adicional"
        verbose_name_plural = "Servicios Adicionales"

    def __str__(self):
        return f"{self.nombre} - ${self.costo}"

# --- Modelo Reservas ---
class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('PEN', 'Pendiente'),
        ('CON', 'Confirmada'),
        ('CAN', 'Cancelada'),
        ('FIN', 'Finalizada'),
    ]

    cliente = models.ForeignKey(Huesped, on_delete=models.CASCADE, related_name='reservas')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.SET_NULL, null=True, related_name='reservas')
    
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default='PEN')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reserva #{self.id} - {self.cliente} (Hab: {self.habitacion.numero})"

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

# --- Modelo Rentas (ACTUALIZADO) ---
class Renta(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='renta')
    
    # NUEVOS CAMPOS AGREGADOS
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    deposito = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observaciones = models.TextField(blank=True, null=True)

    fecha_checkin_real = models.DateTimeField(auto_now_add=True)
    fecha_checkout_real = models.DateTimeField(null=True, blank=True)
    
    servicios_consumidos = models.ManyToManyField(ServicioAdicional, blank=True, related_name='rentas')
    
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Renta #{self.id} - {self.reserva.cliente}"

    class Meta:
        verbose_name = "Renta"
        verbose_name_plural = "Rentas"