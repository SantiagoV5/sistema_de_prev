import sys
import os

# Añadir el directorio actual al path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controlador import ControladorAviones


def main():
    """Función principal."""
    # Crear el controlador con configuración personalizada
    controlador = ControladorAviones(
        ancho_ventana=900,
        alto_ventana=700,
        rango_x=120,
        rango_y=120
    )
    
    # Ejecutar la aplicación
    controlador.ejecutar()


if __name__ == "__main__":
    main()
