"""
Configuración: Centraliza los parámetros de la aplicación.
"""

# ============== CONFIGURACIÓN DE VENTANA ==============
ANCHO_VENTANA = 1100
ALTO_VENTANA = 700

# ============== CONFIGURACIÓN DEL PLANO ==============
RANGO_PLANO = 120  # De -120 a +120
ESCALA_BASE = 1.0  # Factor de escala multiplicador

# ============== CONFIGURACIÓN DE AVIONES ==============
CANTIDAD_AVIONES_INICIAL = 2
DISTANCIA_MINIMA_AVIONES = 50  # Distancia mínima entre aviones al generarlos
DISTANCIA_COLISION = 15  # Distancia para detectar colisión

# ============== CONFIGURACIÓN DE VELOCIDAD ==============
VELOCIDAD_MINIMA = 0.5
VELOCIDAD_MAXIMA = 2.0
FPS = 60  # Frames por segundo

# ============== INTERFAZ / FUENTES ==============
LEFT_PANEL_WIDTH = 400
FONT_SIZE_GRANDE = 28
FONT_SIZE_NORMAL = 20
FONT_SIZE_PEQUENA = 16
FONT_SIZE_MINI = 10

# ============== CONFIGURACIÓN DE COLORES ==============
COLORES_AVIONES = [
    (255, 0, 0),      # Rojo
    (0, 100, 255),    # Azul
    (0, 200, 0),      # Verde
    (255, 165, 0),    # Naranja
    (255, 255, 0),    # Amarillo
    (255, 0, 255),    # Magenta
]

COLORES = {
    'BLANCO': (255, 255, 255),
    'NEGRO': (0, 0, 0),
    'GRIS_CLARO': (220, 220, 220),
    'GRIS': (100, 100, 100),
    'ROJO': (255, 0, 0),
    'AZUL': (0, 100, 255),
    'VERDE': (0, 200, 0),
    'NARANJA': (255, 165, 0),
}

# ============== CONFIGURACIÓN DE PANTALLA ==============
TITULO_VENTANA = "Sistema de Aviones - Plano Cartesiano (MVC)"
MOSTRAR_GRID = False
MOSTRAR_ETIQUETAS = True

# ============== CONFIGURACIÓN DE MOVIMIENTO ==============
MOVIMIENTO_ACTIVO_INICIAL = True
MOSTRAR_HISTORIAL_INICIAL = False

# ============== MENSAJES ==============
MENSAJE_INICIO = """
╔════════════════════════════════════════════════════════════╗
║    SISTEMA DE AVIONES - PLANO CARTESIANO (MVC)           ║
║              Simulación de Movimiento Aéreo               ║
╚════════════════════════════════════════════════════════════╝

CONTROLES:
  ESPACIO  - Generar nuevos aviones
  M        - Activar/Desactivar movimiento
  H        - Mostrar/Ocultar historial
  A        - Añadir un avión más
  ESC      - Salir

═══════════════════════════════════════════════════════════════
"""

# ============== CONFIGURACIÓN AVANZADA ==============
DEBUG_MODE = False  # Modo depuración (imprime más información)
LIMITE_FRAMES_HISTORIAL = 500  # Máximo de frames en el historial antes de limpiar
# Factor multiplicador para interpretar el umbral ingresado.
# Por defecto 1.0: el umbral se usa tal cual en las unidades del modelo.
# Si quieres que el umbral sea más permisivo, aumenta este valor (ej. 2.0).
UMBRAL_SCALE = 1.0
