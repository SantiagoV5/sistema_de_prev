"""
Controlador: Gestiona la interacción entre el modelo y la vista.
"""
import pygame
import sys
from modelo import GestorAviones
from vista import VistaPlanoCartesiano


class ControladorAviones:
    """Controlador principal que gestiona la aplicación."""
    
    def __init__(self, ancho_ventana=900, alto_ventana=700, rango_x=120, rango_y=120):
        """
        Inicializa el controlador.
        
        Args:
            ancho_ventana: Ancho de la ventana
            alto_ventana: Alto de la ventana
            rango_x: Rango X del plano cartesiano
            rango_y: Rango Y del plano cartesiano
        """
        self.modelo = GestorAviones(rango_x=rango_x, rango_y=rango_y)
        self.vista = VistaPlanoCartesiano(ancho_ventana, alto_ventana, rango_x=rango_x, rango_y=rango_y)
        
        # Configuración
        self.fps = 60
        self.mostrar_historial = False
        self.movimiento_activo = True
        self.distancia_colision = 15
        self.umbral = 15  # Umbral de riesgo de colisión en NM
        
        # No generar aviones aun: pedir al usuario las entradas al iniciar
        self.input_mode = True
        # campos: lista de [clave, valor_str]
        # Todos los campos vacíos al inicio
        self.param_fields = [['Número de aviones', ''], ['Umbral de NM', '']]
        self.input_index = 0
        self.input_buffer = ''
    
    def manejar_eventos(self):
        """Maneja los eventos del usuario."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Si está el formulario abierto, permitir hacer click en las cajas para enfocar
                if self.input_mode and evento.button == 1:
                    mx, my = evento.pos
                    # Coordenadas de las cajas en el panel izquierdo (deben coincidir con dibujar_interfaz)
                    x_pad = 10
                    box_x = x_pad
                    box_w = self.vista.left_panel_width - 2 * x_pad
                    box_h = 30
                    label_height = 22
                    spacing = 60
                    y0 = 10 + 40  # y_pos inicial en dibujar_interfaz
                    
                    # Calcular rects para cada campo
                    for i in range(len(self.param_fields)):
                        rect_y = y0 + i * spacing + label_height + 4
                        rect = pygame.Rect(box_x, rect_y, box_w, box_h)
                        if rect.collidepoint(mx, my):
                            self.input_index = i
                            return True
                    return True

            elif evento.type == pygame.KEYDOWN:
                # Si estamos en modo de entrada de parámetros, procesar texto
                if self.input_mode:
                    # ESC cierra la aplicación
                    if evento.key == pygame.K_ESCAPE:
                        return False

                    # ENTER aplica parámetros
                    if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        try:
                            n = int(self.param_fields[0][1])
                            umbral = float(self.param_fields[1][1])

                            # Validaciones básicas
                            if n <= 0:
                                raise ValueError("n debe ser mayor que 0")
                            if umbral <= 0:
                                raise ValueError("Umbral de NM debe ser mayor que 0")

                            self.umbral = umbral  # Guardar umbral

                            # Ignorar los rangos ingresados; siempre usar 120x120 para evitar distorsión
                            # Pero regenerar aviones con la cantidad especificada
                            self.modelo.limpiar_aviones()
                            self.modelo.generar_aviones_aleatorios(cantidad=n, distancia_minima=max(5, 120 * 0.1))
                            # Registrar la cantidad inicial y resetear contadores
                            self.modelo.inicial_cantidad = n
                            self.modelo.colisiones_evitadas = 0
                            self.modelo.colisiones_reportadas = False
                            print(f"Parámetros aplicados: n={n}, plano fijo en 120x120, umbral={umbral}")

                            # Salir modo input y comenzar simulación
                            self.input_mode = False
                            return True

                        except Exception as e:
                            print("Error aplicando parámetros:", e)
                            return True

                    # BACKSPACE
                    if evento.key == pygame.K_BACKSPACE:
                        cur = self.param_fields[self.input_index][1]
                        self.param_fields[self.input_index][1] = cur[:-1]
                        return True

                    # TAB cambia campo
                    if evento.key == pygame.K_TAB:
                        self.input_index = (self.input_index + 1) % len(self.param_fields)
                        return True

                    # Texto (unicode)
                    char = evento.unicode
                    if char:
                        # permitir dígitos, signo y punto
                        if char.isprintable():
                            self.param_fields[self.input_index][1] += char
                    return True

                # Modo normal (no input panel)
                if evento.key == pygame.K_ESCAPE:
                    # Volver a modo de entrada de parámetros
                    self.input_mode = True
                    self.param_fields = [['Número de aviones', ''], ['Umbral de NM', '']]
                    self.input_index = 0
                    self.modelo.limpiar_aviones()
                    print("Regresando a entrada de parámetros...")
                    return True
        
        return True
    
    def actualizar(self):
        """Actualiza el estado del juego."""
        # Los aviones solo se generan aleatoriamente en el plano, no se mueven

        # Ejecutar algoritmo Dividir y Vencer para encontrar pareja más cercana
        self.modelo.ejecutar_algoritmo_pareja_cercana()
    
    def obtener_estadisticas(self):
        """Obtiene las estadísticas del sistema."""
        return self.modelo.obtener_estadisticas()
    
    def ejecutar(self):
        """Ejecuta el bucle principal de la aplicación."""
        ejecutando = True
        while ejecutando:
            # Manejar eventos
            ejecutando = self.manejar_eventos()
            
            # Actualizar modelo
            self.actualizar()
            
            # Obtener datos para la vista
            aviones = self.modelo.obtener_todos_aviones()
            estadisticas = self.obtener_estadisticas()
            pareja_cercana = self.modelo.obtener_pareja_mas_cercana()
            stats_algoritmo = self.modelo.obtener_estadisticas_algoritmo()

            # Si todos los aviones salieron del plano y aún no reportamos colisiones evitadas,
            # asignar colisiones_evitadas = inicial_cantidad // 2 (y reportarlo solo una vez).
            if estadisticas.get('todos_fuera', False) and not getattr(self.modelo, 'colisiones_reportadas', False):
                inicial = getattr(self.modelo, 'inicial_cantidad', 0) or 0
                self.modelo.colisiones_evitadas = inicial // 2
                self.modelo.colisiones_reportadas = True
            
            # Dibujar (vista ahora incluye panel izquierdo donde mostramos entradas)
            campos = [(f[0], f[1]) for f in self.param_fields]
            # Pasamos el estado de input_mode e índices para que la vista pinte los valores en el panel
            self.vista.dibujar(aviones, estadisticas, pareja_cercana, stats_algoritmo,
                              self.mostrar_historial, False,
                              input_mode=self.input_mode, campos=campos, input_index=self.input_index, umbral=self.umbral)
            
            # Controlar FPS
            self.vista.tick(self.fps)
        
        self.vista.cerrar()
        pygame.quit()
        print("\nAplicación cerrada.")
