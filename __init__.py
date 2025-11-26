"""
Sistema de Aviones - Plano Cartesiano (MVC)

Aplicación que simula aviones moviéndose en un plano cartesiano
usando arquitectura Modelo-Vista-Controlador.

Módulos:
- modelo: Lógica de negocio
- vista: Visualización con pygame
- controlador: Coordinación entre modelo y vista
- config: Configuración de la aplicación
- utilidades: Funciones auxiliares
"""

__version__ = "1.0.0"
__author__ = "Proyecto Educativo"
__all__ = ['modelo', 'vista', 'controlador', 'config', 'utilidades']

from . import modelo
from . import vista
from . import controlador
from . import config
from . import utilidades
