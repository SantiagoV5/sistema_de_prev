"""
Utilidades: Funciones auxiliares para la aplicación.
"""
import math


def calcular_distancia(x1, y1, x2, y2):
    """
    Calcula la distancia euclidiana entre dos puntos.
    
    Args:
        x1, y1: Coordenadas del primer punto
        x2, y2: Coordenadas del segundo punto
    
    Returns:
        Distancia entre los puntos
    """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def calcular_angulo(x1, y1, x2, y2):
    """
    Calcula el ángulo entre dos puntos en grados.
    
    Args:
        x1, y1: Coordenadas del primer punto
        x2, y2: Coordenadas del segundo punto
    
    Returns:
        Ángulo en grados (0-360)
    """
    radianes = math.atan2(y2 - y1, x2 - x1)
    grados = math.degrees(radianes)
    return grados % 360


def normalizar_angulo(angulo):
    """
    Normaliza un ángulo al rango 0-360.
    
    Args:
        angulo: Ángulo en grados
    
    Returns:
        Ángulo normalizado
    """
    return angulo % 360


def punto_en_rango(x, y, rango):
    """
    Verifica si un punto está dentro del rango especificado.
    
    Args:
        x, y: Coordenadas del punto
        rango: Rango (de -rango a +rango)
    
    Returns:
        True si el punto está dentro del rango
    """
    return -rango <= x <= rango and -rango <= y <= rango


def rebote_en_limites(x, y, rango):
    """
    Ajusta las coordenadas para que reboten dentro de los límites.
    
    Args:
        x, y: Coordenadas
        rango: Rango del plano
    
    Returns:
        Tupla (x_ajustado, y_ajustado)
    """
    x_nuevo = x
    y_nuevo = y
    
    if x < -rango:
        x_nuevo = rango
    elif x > rango:
        x_nuevo = -rango
    
    if y < -rango:
        y_nuevo = rango
    elif y > rango:
        y_nuevo = -rango
    
    return x_nuevo, y_nuevo



