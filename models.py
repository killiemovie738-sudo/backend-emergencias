from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# --- ESTANTE 1: CLIENTES (CU-01) ---
class Cliente(Base):
    __tablename__ = "clientes" # Así se llamará la tabla en PostgreSQL

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String, index=True)
    telefono = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    contrasena = Column(String)

    # Relación: Un cliente puede tener varios vehículos
    vehiculos = relationship("Vehiculo", back_populates="dueño")


# --- ESTANTE 2: VEHÍCULOS (CU-02) ---
class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String, unique=True, index=True)
    marca = Column(String)
    modelo = Column(String)
    color = Column(String)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    dueño = relationship("Cliente", back_populates="vehiculos")


# --- ESTANTE 3: TALLERES (CU-03) ---
class Taller(Base):
    __tablename__ = "talleres"

    id = Column(Integer, primary_key=True, index=True)
    nombre_taller = Column(String, index=True)
    direccion = Column(String)
    telefono = Column(String)
    email = Column(String, unique=True, index=True)
    contrasena = Column(String)
    # En models.py, dentro de class Taller:
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)

    # Relación: Un taller tiene varios técnicos
    tecnicos = relationship("Tecnico", back_populates="taller_trabajo")


# --- ESTANTE 4: TÉCNICOS (CU-04) ---
class Tecnico(Base):
    __tablename__ = "tecnicos"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String)
    especialidad = Column(String) # Ej: Mecánico general, Eléctrico, Llantas
    
    usuario          = Column(String, unique=True, nullable=True)
    contrasena       = Column(String, nullable=True)

     # NUEVO: disponibilidad (CU-14)
    # True = disponible para atender, False = ocupado/fuera de turno
    disponible       = Column(Boolean, default=True)
    motivo_no_disponible = Column(String, nullable=True)  # "fuera de horario", "en servicio", etc.

    # Esta es la "cuerdita" que une al técnico con su taller
    taller_id = Column(Integer, ForeignKey("talleres.id"))
    taller_trabajo = relationship("Taller", back_populates="tecnicos")
# --- ESTANTE 5: EMERGENCIAS (CU-05) ---
class Emergencia(Base):
    __tablename__ = "emergencias"
    id = Column(Integer, primary_key=True, index=True)
    # Datos de ubicación y problema
    direccion = Column(String) # Dirección manual escrita por el cliente
    descripcion = Column(String)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    tipo_ia = Column(String(100), nullable=True)
    severidad_ia = Column(String(50), nullable=True)
    estado = Column(String, default="Pendiente") # Pendiente, Asignada, Aceptada, Rechazada, En Camino, En Proceso, Finalizado

    # Campos para audio y transcripción (CU-10)
    audio_url = Column(String, nullable=True)
    transcripcion = Column(Text, nullable=True)

    foto_url = Column(String, nullable=True)    

    # Campos para técnico y observaciones (CU-09)
    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"), nullable=True)
    observaciones = Column(Text, nullable=True)

    # Timestamps
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relaciones (Foreign Keys)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"))
    taller_id = Column(Integer, ForeignKey("talleres.id"), nullable=True) # Se llena cuando el taller acepta

    # Relaciones con back_populates
    cliente = relationship("Cliente", backref="emergencias")
    vehiculo = relationship("Vehiculo", backref="emergencias")
    taller = relationship("Taller", backref="emergencias")
    tecnico = relationship("Tecnico", backref="emergencias")

# --- ESTANTE 6: HISTORIAL DE ESTADOS (CU-06, CU-08, CU-09) ---
class HistorialEstado(Base):
    __tablename__ = "historial_estados"
    id = Column(Integer, primary_key=True, index=True)
    emergencia_id = Column(Integer, ForeignKey("emergencias.id"))
    estado_anterior = Column(String)
    estado_nuevo = Column(String)
    descripcion = Column(String, nullable=True)
    fecha_cambio = Column(DateTime, default=datetime.now)

    emergencia = relationship("Emergencia", backref="historial_estados")

# --- TABLA NUEVA: ACEPTACIONES DE TALLERES ---
# Guarda cada vez que un taller acepta UNA emergencia.
# Así el cliente puede ver la lista y elegir uno.
class AceptacionTaller(Base):
    __tablename__ = "aceptaciones_taller"
 
    id             = Column(Integer, primary_key=True, index=True)
    emergencia_id  = Column(Integer, ForeignKey("emergencias.id"))
    taller_id      = Column(Integer, ForeignKey("talleres.id"))
    # Tiempo estimado de llegada en minutos (lo ingresa el taller)
    tiempo_estimado_minutos = Column(Integer, nullable=True)
    # Mensaje adicional del taller (ej: "Tengo grúa disponible")
    mensaje        = Column(String, nullable=True)
    # Estado de esta aceptación específica
    # "pendiente" = esperando que el cliente elija
    # "confirmada" = el cliente eligió este taller
    # "rechazada" = el cliente eligió otro taller
    estado         = Column(String, default="pendiente")
    fecha          = Column(DateTime, default=datetime.now)
 
    emergencia     = relationship("Emergencia", backref="aceptaciones")
    taller         = relationship("Taller", backref="aceptaciones")

# CU16 PAGOS

class Pago(Base):
    __tablename__ = "pagos"
    
    id              = Column(Integer, primary_key=True)
    emergencia_id   = Column(Integer, ForeignKey("emergencias.id"))
    cliente_id      = Column(Integer, ForeignKey("clientes.id"))
    taller_id       = Column(Integer, ForeignKey("talleres.id"))
    monto           = Column(Float)          # En bolivianos (BOB) o USD
    metodo_pago     = Column(String)         # "tarjeta", "qr", "efectivo"
    estado_pago     = Column(String, default="pendiente")  # pendiente, completado, fallido
    referencia      = Column(String, nullable=True)        # ID de transacción Stripe/MP
    fecha_pago      = Column(DateTime, nullable=True)
    fecha_creacion  = Column(DateTime, default=datetime.now)
    
    emergencia      = relationship("Emergencia", backref="pago")

# ==========================================
# CU-18: TABLA DE TOKENS PARA NOTIFICACIONES
# ==========================================
class TokenNotificacion(Base):
    __tablename__ = "tokens_notificacion"
    
    id          = Column(Integer, primary_key=True)
    cliente_id  = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    taller_id   = Column(Integer, ForeignKey("talleres.id"), nullable=True)
    token_fcm   = Column(String)        # Token del dispositivo (Firebase)
    plataforma  = Column(String)        # "android", "ios", "web"
    activo      = Column(Boolean, default=True)
    fecha       = Column(DateTime, default=datetime.now)