"""
Clases del sistema: abstracción, herencia, polimorfismo, encapsulamiento
"""

from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import *


class Entidad(ABC):
    """Clase abstracta base para todas las entidades del sistema"""
    
    def _init_(self, identificador: int, nombre: str):
        self._id = identificador
        self._nombre = nombre.strip()