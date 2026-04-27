from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Este es el "formulario" que el cliente llenará en su App (Flutter)
class ClienteNuevo(BaseModel):
    nombre_completo: str
    telefono: str
    email: str
    contrasena: str

# --- FORMULARIO PARA VEHÍCULOS (CU-02) ---
class VehiculoNuevo(BaseModel):
    placa: str
    marca: str
    modelo: str
    color: str
    cliente_id: int  # ¡Súper importante! Esto nos dice de quién es el auto

# --- FORMULARIO PARA TALLERES (CU-03) ---
class TallerNuevo(BaseModel):
    nombre_taller: str
    direccion: str
    telefono: str
    email: str
    contrasena: str

# --- FORMULARIO PARA TÉCNICOS (CU-04) ---
class TecnicoNuevo(BaseModel):
    nombre_completo: str
    especialidad: str
    taller_id: int # Para saber en qué taller trabaja este mecánico
    usuario: Optional[str] = None      # Ej: "juanito_mec"
    contrasena: Optional[str] = None   # El taller la define

class LoginTecnico(BaseModel):
    usuario: str
    contrasena: str

# --- FORMULARIO PARA EMERGENCIAS (CU-05) ---
class EmergenciaNueva(BaseModel):
    cliente_id: int
    vehiculo_id: int
    direccion: str
    descripcion: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    tipo_ia: Optional[str] = None
    severidad_ia: Optional[str] = None
    audio_url: Optional[str] = None

class EmergenciaResponse(BaseModel):
    id: int
    cliente_id: int
    vehiculo_id: int
    direccion: str
    descripcion: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    tipo_ia: Optional[str] = None
    severidad_ia: Optional[str] = None
    estado: str
    audio_url: Optional[str] = None
    transcripcion: Optional[str] = None
    taller_id: Optional[int] = None
    tecnico_id: Optional[int] = None
    observaciones: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- SCHEMA PARA ACTUALIZAR ESTADO (CU-08, CU-09) ---
class ActualizarEstadoRequest(BaseModel):
    estado: str  # Aceptada, Rechazada, En Camino, En Proceso, Finalizado
    observaciones: Optional[str] = None
    tecnico_id: Optional[int] = None

# --- SCHEMA PARA HISTORIAL DE ESTADOS (CU-06) ---
class HistorialEstadoResponse(BaseModel):
    id: int
    emergencia_id: int
    estado_anterior: str
    estado_nuevo: str
    descripcion: Optional[str] = None
    fecha_cambio: datetime

    class Config:
        from_attributes = True

# --- SCHEMA PARA TRANSCRIPCIÓN DE AUDIO (CU-10) ---
class TranscripcionRequest(BaseModel):
    emergencia_id: int
    audio_url: str

class TranscripcionResponse(BaseModel):
    emergencia_id: int
    transcripcion: str
    exito: bool

# --- FORMULARIO PARA INICIAR SESIÓN ---
class LoginTaller(BaseModel):
    email: str
    contrasena: str

# --- FORMULARIO PARA CREAR CLIENTE ---
class ClienteCreate(BaseModel):
    nombre_completo: str
    email: str
    contrasena: str
    telefono: str

class LoginCliente(BaseModel):
    email: str
    contrasena: str

class VehiculoCreate(BaseModel):
    placa: str
    marca: str
    modelo: str
    color: str
    cliente_id: int

# --- SCHEMA PARA RESPUESTA DE EMERGENCIA CON HISTORIAL (CU-06) ---
class EmergenciaConHistorialResponse(EmergenciaResponse):
    historial_estados: Optional[list[HistorialEstadoResponse]] = None
    nombre_taller: Optional[str] = None
    nombre_tecnico: Optional[str] = None 

# Schema para que el taller acepte con tiempo estimado
class AceptarConTiempoRequest(BaseModel):
    taller_id: int
    tiempo_estimado_minutos: int = 15
    mensaje: Optional[str] = None
    tecnico_id: Optional[int] = None
 
# Schema de respuesta de un taller que aceptó
class TallerQueAceptoResponse(BaseModel):
    aceptacion_id: int
    taller_id: int
    nombre_taller: str
    direccion_taller: Optional[str]
    telefono: Optional[str]
    tiempo_estimado_minutos: Optional[int]
    mensaje: Optional[str]

class PagoNuevo(BaseModel):
     emergencia_id: int
     cliente_id: int
     taller_id: int
     monto: float
     metodo_pago: str = "tarjeta"

class TallerNuevo(BaseModel):
    nombre_taller: str
    direccion: str
    telefono: str
    email: str
    contrasena: str
    latitud: float # <-- Agregado
    longitud: float # <-- Agregado