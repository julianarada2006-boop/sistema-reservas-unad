"""
Módulo con excepciones personalizadas
Curso: Programación - Código: 213023
UNAD - Universidad Nacional Abierta y a Distancia
"""

class ErrorSistema(Exception):
    """Excepción base del sistema"""
    pass

class DatoInvalidoError(ErrorSistema):
    """Dato con formato o valor incorrecto"""
    pass

class ClienteDuplicadoError(ErrorSistema):
    """El cliente ya existe en el sistema"""
    pass

class ServicioNoDisponibleError(ErrorSistema):
    """Servicio no disponible para reserva"""
    pass

class ReservaInvalidaError(ErrorSistema):
    """Datos de reserva inconsistentes"""
    pass

class OperacionNoPermitidaError(ErrorSistema):
    """Acción no permitida"""
    pass