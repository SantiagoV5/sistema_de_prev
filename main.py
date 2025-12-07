from controlador import ControladorAviones

def main():
    """Función principal."""
    
    controlador = ControladorAviones(
        ancho_ventana=1200,
        alto_ventana=700,
        rango_x=120,
        rango_y=120
    )
    
    
    controlador.ejecutar()


if __name__ == "__main__":
    main()
