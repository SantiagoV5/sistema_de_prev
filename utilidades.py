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


def mover_hacia_punto(x_actual, y_actual, x_objetivo, y_objetivo, velocidad):
    """
    Mueve un punto hacia otro objetivo.
    
    Args:
        x_actual, y_actual: Posición actual
        x_objetivo, y_objetivo: Posición objetivo
        velocidad: Velocidad de movimiento
    
    Returns:
        Tupla (x_nuevo, y_nuevo)
    """
    distancia = calcular_distancia(x_actual, y_actual, x_objetivo, y_objetivo)
    
    if distancia < velocidad:
        return x_objetivo, y_objetivo
    
    # Calcular dirección
    dx = x_objetivo - x_actual
    dy = y_objetivo - y_actual
    
    # Normalizar
    dx_norm = dx / distancia
    dy_norm = dy / distancia
    
    # Mover
    x_nuevo = x_actual + dx_norm * velocidad
    y_nuevo = y_actual + dy_norm * velocidad
    
    return x_nuevo, y_nuevo


def verificar_colision_círculo(x1, y1, r1, x2, y2, r2):
    """
    Verifica colisión entre dos círculos.
    
    Args:
        x1, y1: Centro del primer círculo
        r1: Radio del primer círculo
        x2, y2: Centro del segundo círculo
        r2: Radio del segundo círculo
    
    Returns:
        True si hay colisión
    """
    distancia = calcular_distancia(x1, y1, x2, y2)
    return distancia < (r1 + r2)


def limitar_rango(valor, minimo, maximo):
    """
    Limita un valor a un rango específico.
    
    Args:
        valor: Valor a limitar
        minimo: Valor mínimo
        maximo: Valor máximo
    
    Returns:
        Valor limitado
    """
    return max(minimo, min(maximo, valor))


def interpolar_color(color1, color2, factor):
    """
    Interpola entre dos colores RGB.
    
    Args:
        color1: Tupla RGB (r, g, b)
        color2: Tupla RGB (r, g, b)
        factor: Factor de interpolación (0.0 a 1.0)
    
    Returns:
        Tupla RGB interpolada
    """
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)
    return (r, g, b)


def formatear_vector(x, y, decimales=2):
    """
    Formatea un vector para impresión.
    
    Args:
        x, y: Componentes del vector
        decimales: Cantidad de decimales
    
    Returns:
        String formateado
    """
    return f"({x:.{decimales}f}, {y:.{decimales}f})"


def obtener_velocidad_desde_angulo(velocidad_magnitud, angulo):
    """
    Obtiene componentes de velocidad (vx, vy) desde magnitud y ángulo.
    
    Args:
        velocidad_magnitud: Magnitud de la velocidad
        angulo: Ángulo en grados
    
    Returns:
        Tupla (vx, vy)
    """
    radianes = math.radians(angulo)
    vx = velocidad_magnitud * math.cos(radianes)
    vy = velocidad_magnitud * math.sin(radianes)
    return vx, vy
