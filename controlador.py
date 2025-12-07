"""
Controlador: Gestiona la interacción entre el modelo y la vista.
"""
import pygame
from modelo import GestorAviones
from vista import VistaPlanoCartesiano
try:
    from config import UMBRAL_SCALE, DEBUG_MODE
except Exception:
    UMBRAL_SCALE = 1.0
    DEBUG_MODE = False


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
        self.param_fields = [['NUMERO DE AVIONES', ''], ['UMBRAL DE NM', '']]
        self.input_index = 0
        self.input_buffer = ''
        # Mensaje de error para mostrar en pantalla cuando la entrada es inválida
        self.input_error_msg = None
    
    def manejar_eventos(self):
        """Maneja los eventos del usuario."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Si panel de parejas está abierto, permitir cerrar con click fuera
                if self.vista.mostrar_panel_parejas and evento.button == 1:
                    mx, my = evento.pos
                    # El panel está centrado, si hace click afuera lo cerramos
                    # (simplemente toggle el estado)
                    # Para click en el botón "Ver todo", ya lo manejamos abajo
                    return True
                
                # Si está el formulario abierto, permitir hacer click en las cajas para enfocar
                if self.input_mode and evento.button == 1:
                    mx, my = evento.pos
                    # Click en botón "Ver todo parejas" si existe
                    if hasattr(self.vista, 'boton_parejas_rect'):
                        if self.vista.boton_parejas_rect.collidepoint(mx, my):
                            self.vista.mostrar_panel_parejas = True
                            return True
                    
                    # Coordenadas de las cajas en el panel izquierdo (deben coincidir con dibujar_interfaz)
                    x_pad = 10
                    box_x = x_pad
                    # Debe coincidir con la lógica de vista: resto 30px para margen
                    box_w = max(60, self.vista.left_panel_width - 2 * x_pad - 30)
                    box_h = 44
                    label_height = 22
                    spacing = 80
                    y0 = 10 + 40  # y_pos inicial en dibujar_interfaz
                    
                    # Calcular rects para cada campo
                    for i in range(len(self.param_fields)):
                        rect_y = y0 + i * spacing + label_height + 4
                        rect = pygame.Rect(box_x, rect_y, box_w, box_h)
                        if rect.collidepoint(mx, my):
                            self.input_index = i
                            return True
                    return True

                # Manejo legacy de rueda usando botones 4/5 (scroll)
                # Si el usuario hizo click con botón 4 (arriba) o 5 (abajo) dentro
                # del área del panel izquierdo, desplazar la lista.
                if evento.button in (4, 5):
                    mx, my = evento.pos
                    if mx <= self.vista.left_panel_width:
                        delta = 20 if evento.button == 5 else -20
                        self.vista.left_panel_scroll = max(0, self.vista.left_panel_scroll + delta)
                        return True

            # Manejar redimensionamiento de ventana (maximizar / cambiar tamaño)
            elif evento.type == pygame.VIDEORESIZE:
                try:
                    nuevo_ancho = evento.w
                    nuevo_alto = evento.h
                    # Delegar a la vista para recalcular escala y rects
                    self.vista.ajustar_tamano(nuevo_ancho, nuevo_alto)
                except Exception:
                    pass
                return True

            elif evento.type == pygame.KEYDOWN:
                # Si panel de parejas está abierto, manejar navegación
                if self.vista.mostrar_panel_parejas:
                    if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_p:
                        self.vista.mostrar_panel_parejas = False
                        self.vista.panel_parejas_scroll = 0
                        return True
                    if evento.key == pygame.K_UP:
                        self.vista.panel_parejas_scroll = max(0, self.vista.panel_parejas_scroll - 20)
                        return True
                    if evento.key == pygame.K_DOWN:
                        self.vista.panel_parejas_scroll += 20
                        return True

                # Si el panel lateral NO está abierto y no estamos en input_mode,
                # permitir usar ↑/↓ para desplazar el panel izquierdo (lista)
                if not self.vista.mostrar_panel_parejas and not self.input_mode:
                    if evento.key == pygame.K_UP:
                        self.vista.left_panel_scroll = max(0, self.vista.left_panel_scroll - 20)
                        return True
                    if evento.key == pygame.K_DOWN:
                        self.vista.left_panel_scroll += 20
                        return True

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
                            # Validaciones básicas
                            if n <= 0:
                                raise ValueError("n debe ser mayor que 0")
                            if n > 500:
                                # No permitir más de 500 aviones
                                self.input_error_msg = "Máximo permitido: 500 aviones"
                                return True
                            if umbral <= 0:
                                raise ValueError("Umbral de NM debe ser mayor que 0")

                            self.input_error_msg = None
                            self.umbral = umbral  # Guardar umbral

                            # Ignorar los rangos ingresados; siempre usar 120x120 para evitar distorsión
                            # Pero regenerar aviones con la cantidad especificada
                            self.modelo.limpiar_aviones()
                            # Generar aviones permitiendo distancias más pequeñas entre ellos
                            # para que umbrales bajos (ej. 10) puedan detectar parejas.
                            self.modelo.generar_aviones_aleatorios(cantidad=n, distancia_minima=5)
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
                    self.param_fields = [['NUMERO DE AVIONES', ''], ['UMBRAL DE NM', '']]
                    self.input_index = 0
                    self.modelo.limpiar_aviones()
                    # Resetear estado del panel de parejas
                    self.vista.mostrar_panel_parejas = False
                    self.vista.panel_parejas_scroll = 0
                    print("Regresando a entrada de parámetros...")
                    return True
                # Controles de zoom: '+' (o '=') para acercar, '-' para alejar
                if not self.input_mode:
                    if evento.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                        try:
                            self.vista.ajustar_zoom(1.15)
                        except Exception:
                            pass
                        return True
                    if evento.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        try:
                            self.vista.ajustar_zoom(0.85)
                        except Exception:
                            pass
                        return True
                    # Tecla P para mostrar/ocultar panel de parejas
                    if evento.key == pygame.K_p:
                        self.vista.mostrar_panel_parejas = not self.vista.mostrar_panel_parejas
                        self.vista.panel_parejas_scroll = 0
                        return True

            # Manejar eventos de rueda modernos (pygame.MOUSEWHEEL)
            elif evento.type == pygame.MOUSEWHEEL:
                # Obtener posición actual del mouse y desplazar si está sobre el panel izquierdo
                try:
                    mx, my = pygame.mouse.get_pos()
                    if mx <= self.vista.left_panel_width:
                        # evento.y: positivo hacia arriba; invertimos para que rueda hacia arriba reduzca scroll
                        self.vista.left_panel_scroll = max(0, self.vista.left_panel_scroll - int(evento.y * 24))
                        return True
                except Exception:
                    pass
                # (Input-mode handling is done on KEYDOWN; nothing more here.)
        
        return True
    
    def actualizar(self):
        """Actualiza el estado del juego."""
        # Los aviones solo se generan aleatoriamente en el plano, no se mueven

        # Ejecutar algoritmo Dividir y Vencer para encontrar pareja más cercana
        self.modelo.ejecutar_algoritmo_pareja_cercana()
        # Calcular todas las parejas dentro del umbral actual (riesgo)
        effective_umbral = (self.umbral or 0) * UMBRAL_SCALE
        try:
            self.parejas_riesgo = self.modelo.encontrar_parejas_en_riesgo(effective_umbral)
        except Exception:
            # Si algo falla, aseguramos que la variable exista
            self.parejas_riesgo = []

        # Debug: imprimir resumen de parejas y algunas distancias si está activado
        if DEBUG_MODE:
            try:
                dists = [round(p.distancia, 2) for p in self.parejas_riesgo]
                dists_sorted = sorted(dists)
                print(f"[DEBUG] umbral={self.umbral} scale={UMBRAL_SCALE} effective={effective_umbral} -> parejas={len(dists_sorted)} dists={dists_sorted[:10]}")
            except Exception:
                print(f"[DEBUG] umbral={self.umbral} scale={UMBRAL_SCALE} effective={effective_umbral} -> parejas={len(self.parejas_riesgo)}")
    
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
            # parejas en riesgo calculadas durante `actualizar`
            parejas_riesgo = getattr(self, 'parejas_riesgo', [])
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
            # Pasar mensaje de error (si existe) dentro de 'estadisticas' para que la vista lo pinte
            estadisticas = self.obtener_estadisticas()
            if self.input_error_msg:
                # Insertar clave especial para mensaje de input
                estadisticas['__input_error__'] = self.input_error_msg

            kwargs = dict(input_mode=self.input_mode, campos=campos,
                          input_index=self.input_index, umbral=self.umbral,
                          parejas_riesgo=parejas_riesgo)
            self.vista.dibujar(
                aviones,
                estadisticas,
                pareja_cercana,
                stats_algoritmo,
                self.mostrar_historial,
                False,
                **kwargs,
            )
            
            # Controlar FPS
            self.vista.tick(self.fps)
        
        self.vista.cerrar()
        pygame.quit()
        print("\nAplicación cerrada.")
