"""
Ejemplos de uso del sistema MVC de Aviones.
Este archivo demuestra cómo usar los componentes del proyecto.
"""

# ============== EJEMPLO 1: Uso Básico ==============
def ejemplo_basico():
    """Ejemplo básico de ejecución del programa."""
    from controlador import ControladorAviones
    
    controlador = ControladorAviones()
    controlador.ejecutar()


# ============== EJEMPLO 2: Uso del Modelo ==============
def ejemplo_modelo():
    """Ejemplo de uso directo del modelo."""
    from modelo import GestorAviones
    
    # Crear gestor
    gestor = GestorAviones(rango_plano=100)
    
    # Generar aviones
    aviones = gestor.generar_aviones_aleatorios(cantidad=3, distancia_minima=40)
    
    print("Aviones generados:")
    for avion in aviones:
        print(f"  {avion}")
    
    # Actualizar posiciones
    for i in range(10):
        gestor.actualizar_aviones()
        print(f"\nFrame {i + 1}:")
        for avion in gestor.obtener_todos_aviones():
            print(f"  {avion}")
    
    # Calcular distancias
    print("\nDistancias entre aviones:")
    ids = list(gestor.aviones.keys())
    if len(ids) >= 2:
        dist = gestor.calcular_distancia_entre_aviones(ids[0], ids[1])
        print(f"  Avión {ids[0]} - Avión {ids[1]}: {dist:.2f} unidades")


# ============== EJEMPLO 3: Crear Aviones Personalizados ==============
def ejemplo_aviones_personalizados():
    """Ejemplo de creación de aviones con parámetros específicos."""
    from modelo import Avion
    
    # Crear aviones en posiciones específicas
    avion1 = Avion(id_avion=1, x=0, y=0, velocidad=1.0, angulo=45)
    avion2 = Avion(id_avion=2, x=50, y=50, velocidad=2.0, angulo=225)
    
    print("Avión 1:", avion1)
    print("Avión 2:", avion2)
    
    # Simular movimiento
    print("\nSimulación de movimiento:")
    for i in range(5):
        avion1.mover()
        avion2.mover()
        print(f"Frame {i + 1}:")
        print(f"  {avion1}")
        print(f"  {avion2}")


# ============== EJEMPLO 4: Detección de Colisiones ==============
def ejemplo_deteccion_colisiones():
    """Ejemplo de detección de colisiones."""
    from modelo import GestorAviones
    
    gestor = GestorAviones(rango_plano=50)
    
    # Generar aviones muy cerca uno del otro
    avion1 = gestor.generar_aviones_aleatorios(cantidad=1)[0]
    
    # Crear segundo avión muy cerca del primero
    from modelo import Avion
    x1, y1 = avion1.obtener_posicion()
    avion2 = Avion(id_avion=1, x=x1 + 5, y=y1 + 5, velocidad=0, angulo=0)
    gestor.aviones[1] = avion2
    
    print("Aviones generados:")
    print(f"  {avion1}")
    print(f"  {avion2}")
    
    # Verificar colisión
    colision, id1, id2 = gestor.detectar_colision(distancia_minima=10)
    print(f"\n¿Colisión detectada? {colision}")
    
    if colision:
        print(f"  Avión {id1} colisión con Avión {id2}")


# ============== EJEMPLO 5: Estadísticas ==============
def ejemplo_estadisticas():
    """Ejemplo de obtención de estadísticas."""
    from modelo import GestorAviones
    
    gestor = GestorAviones(rango_plano=100)
    gestor.generar_aviones_aleatorios(cantidad=4)
    
    # Obtener estadísticas
    stats = gestor.obtener_estadisticas()
    
    print("Estadísticas del Sistema:")
    print(f"  Cantidad de aviones: {stats['cantidad_aviones']}")
    print(f"  Rango del plano: ±{stats['rango_plano']}")
    print("\nDetalle de aviones:")
    for avion_info in stats['aviones']:
        print(f"  {avion_info}")


# ============== EJEMPLO 6: Configuración Personalizada ==============
def ejemplo_configuracion_personalizada():
    """Ejemplo con configuración personalizada."""
    from controlador import ControladorAviones
    from config import (
        ANCHO_VENTANA, ALTO_VENTANA, RANGO_PLANO, FPS
    )
    
    # Usar configuración desde config.py
    controlador = ControladorAviones(
        ancho_ventana=ANCHO_VENTANA,
        alto_ventana=ALTO_VENTANA,
        rango_plano=RANGO_PLANO
    )
    
    # Modificar parámetros
    controlador.fps = FPS
    controlador.distancia_colision = 12
    
    print("Configuración personalizada:")
    print(f"  Ventana: {ANCHO_VENTANA}x{ALTO_VENTANA}")
    print(f"  Rango: ±{RANGO_PLANO}")
    print(f"  FPS: {FPS}")
    
    # Descomenta para ejecutar:
    # controlador.ejecutar()


# ============== EJEMPLO 7: Uso de Utilidades ==============
def ejemplo_utilidades():
    """Ejemplo de funciones utilitarias."""
    from utilidades import (
        calcular_distancia, calcular_angulo, normalizar_angulo,
        punto_en_rango, mover_hacia_punto
    )
    
    # Calcular distancia
    dist = calcular_distancia(0, 0, 3, 4)
    print(f"Distancia de (0,0) a (3,4): {dist}")
    
    # Calcular ángulo
    ang = calcular_angulo(0, 0, 1, 1)
    print(f"Ángulo de (0,0) a (1,1): {ang}°")
    
    # Normalizar ángulo
    ang_norm = normalizar_angulo(450)
    print(f"450° normalizado: {ang_norm}°")
    
    # Verificar punto en rango
    en_rango = punto_en_rango(50, 50, 100)
    print(f"¿Punto (50,50) en rango ±100? {en_rango}")
    
    # Mover hacia punto
    x, y = mover_hacia_punto(0, 0, 10, 10, velocidad=1.0)
    print(f"Movimiento de (0,0) hacia (10,10) con velocidad 1: ({x:.2f}, {y:.2f})")


# ============== MENÚ PRINCIPAL ==============
def menu_principal():
    """Menú interactivo para ejecutar ejemplos."""
    ejemplos = {
        '1': ('Ejemplo Básico (Ejecutar Programa)', ejemplo_basico),
        '2': ('Uso del Modelo', ejemplo_modelo),
        '3': ('Aviones Personalizados', ejemplo_aviones_personalizados),
        '4': ('Detección de Colisiones', ejemplo_deteccion_colisiones),
        '5': ('Estadísticas', ejemplo_estadisticas),
        '6': ('Configuración Personalizada', ejemplo_configuracion_personalizada),
        '7': ('Utilidades', ejemplo_utilidades),
    }
    
    print("\n" + "=" * 60)
    print("EJEMPLOS DE USO - SISTEMA DE AVIONES MVC")
    print("=" * 60)
    
    for key, (descripcion, _) in ejemplos.items():
        print(f"{key}. {descripcion}")
    
    print("0. Salir")
    print("-" * 60)
    
    opcion = input("\nSelecciona un ejemplo (0-7): ").strip()
    
    if opcion in ejemplos:
        print(f"\n▶ Ejecutando: {ejemplos[opcion][0]}\n")
        print("-" * 60)
        ejemplos[opcion][1]()
        print("-" * 60)
    elif opcion == '0':
        print("¡Hasta luego!")
    else:
        print("Opción no válida")


if __name__ == "__main__":
    menu_principal()
