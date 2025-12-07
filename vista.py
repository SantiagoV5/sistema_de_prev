"""
Vista: Maneja toda la visualización usando pygame.
"""
import pygame

# Intentar cargar configuración centralizada; usar valores por defecto si falta
try:
    from config import (
        ANCHO_VENTANA,
        ALTO_VENTANA,
        RANGO_PLANO,
        COLORES,
        COLORES_AVIONES,
        FPS,
        LEFT_PANEL_WIDTH,
        FONT_SIZE_GRANDE,
        FONT_SIZE_NORMAL,
        FONT_SIZE_PEQUENA,
        FONT_SIZE_MINI,
        MOSTRAR_GRID,
    )
except Exception:
    # Valores por defecto mínimos si no existe config.py
    ANCHO_VENTANA = 900
    ALTO_VENTANA = 700
    RANGO_PLANO = 120
    COLORES = {
        'BLANCO': (255, 255, 255),
        'NEGRO': (0, 0, 0),
        'GRIS_CLARO': (50, 50, 50),
        'GRIS': (150, 150, 150),
        'ROJO': (255, 0, 0),
        'AZUL': (0, 150, 255),
        'VERDE': (0, 255, 100),
        'NARANJA': (255, 165, 0),
        'AMARILLO': (255, 255, 0),
    }
    COLORES_AVIONES = [
        COLORES['ROJO'],
        COLORES['AZUL'],
        COLORES['VERDE'],
        COLORES['NARANJA'],
        COLORES['AMARILLO'],
        (255, 0, 255),
    ]
    FPS = 60
    LEFT_PANEL_WIDTH = 400
    FONT_SIZE_GRANDE = 28
    FONT_SIZE_NORMAL = 20
    FONT_SIZE_PEQUENA = 16
    FONT_SIZE_MINI = 10
    MOSTRAR_GRID = False


class VistaPlanoCartesiano:
    """Gestiona la visualización del plano cartesiano con pygame."""
    
    def __init__(self, ancho=ANCHO_VENTANA, alto=ALTO_VENTANA, rango_x=RANGO_PLANO, rango_y=RANGO_PLANO, left_panel_width=LEFT_PANEL_WIDTH):
        """
        Inicializa la vista.
        
        Args:
            ancho: Ancho de la ventana
            alto: Alto de la ventana
            rango_x: Rango en X del plano cartesiano
            rango_y: Rango en Y del plano cartesiano
        """
        pygame.init()
        self.ancho = ancho
        self.alto = alto
        # Usar el rango establecido en la configuración central
        self.rango_x = rango_x
        self.rango_y = rango_y
        # Tamaño del panel izquierdo (entradas / información)
        self.left_panel_width = left_panel_width
        # Área del plano a la derecha
        self.plano_rect = pygame.Rect(self.left_panel_width, 0, self.ancho - self.left_panel_width, self.alto)
        
        # Control de panel expandido para parejas en riesgo
        self.mostrar_panel_parejas = False
        self.scroll_parejas = 0
        # Scroll interno para el panel izquierdo (lista de parejas)
        self.left_panel_scroll = 0
        # Scroll para la sección de control (agregar/eliminar aviones)
        self.extra_fields_scroll = 0
        # Panel lateral derecho para parejas
        self.panel_parejas_ancho = 280
        self.panel_parejas_scroll = 0

        # Escala basada en el rango configurado
        self.rango = min(self.rango_x, self.rango_y)
        # Hacer la ventana redimensionable para que el botón Maximizar funcione
        self.pantalla = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)
        pygame.display.set_caption("SISTEMA DE PREVENCION")
        self.reloj = pygame.time.Clock()
        
        # Centro del plano en pantalla (dentro del rectángulo derecho)
        self.centro_x = self.plano_rect.x + self.plano_rect.width // 2
        self.centro_y = self.plano_rect.y + self.plano_rect.height // 2
        # Escala basada en el tamaño del rectángulo del plano
        # Zoom multiplicador (1.0 = 100%) para permitir aumentar/disminuir zoom
        self.zoom = 1.0
        self._calcular_escala()
        
        # Colores (tema oscuro) desde config
        self.BLANCO = COLORES.get('BLANCO', (255, 255, 255))
        self.NEGRO = COLORES.get('NEGRO', (0, 0, 0))
        self.GRIS_CLARO = COLORES.get('GRIS_CLARO', (50, 50, 50))
        self.GRIS = COLORES.get('GRIS', (150, 150, 150))
        self.ROJO = COLORES.get('ROJO', (255, 0, 0))
        self.AZUL = COLORES.get('AZUL', (0, 150, 255))
        self.VERDE = COLORES.get('VERDE', (0, 255, 100))
        self.NARANJA = COLORES.get('NARANJA', (255, 165, 0))
        self.AMARILLO = COLORES.get('AMARILLO', (255, 255, 0))

        # Colores para aviones
        self.colores_aviones = COLORES_AVIONES
        
        # Fuentes (tamaños desde config)
        self.fuente_grande = pygame.font.Font(None, FONT_SIZE_GRANDE)
        self.fuente_normal = pygame.font.Font(None, FONT_SIZE_NORMAL)
        self.fuente_pequeña = pygame.font.Font(None, FONT_SIZE_PEQUENA)
        self.fuente_mini = pygame.font.Font(None, FONT_SIZE_MINI)
        self.mostrar_grid = MOSTRAR_GRID
    
    def coordenada_pantalla(self, x_cart, y_cart):
        """Convierte coordenadas cartesianas a coordenadas de pantalla."""
        x_pantalla = self.centro_x + x_cart * self.escala
        y_pantalla = self.centro_y - y_cart * self.escala
        return (int(x_pantalla), int(y_pantalla))
    
    def dibujar_ejes(self):
        """Dibuja los ejes cartesianos."""
        # Eje X dentro del rect del plano (blanco)
        x1 = self.plano_rect.x
        x2 = self.plano_rect.x + self.plano_rect.width
        y_center = self.centro_y
        pygame.draw.line(self.pantalla, self.BLANCO, (x1, y_center), (x2, y_center), 2)

        # Eje Y dentro del rect del plano (blanco)
        y1 = self.plano_rect.y
        y2 = self.plano_rect.y + self.plano_rect.height
        pygame.draw.line(self.pantalla, self.BLANCO, (self.centro_x, y1), (self.centro_x, y2), 2)
        
        # Marcas cada 10 unidades hasta 100 (blanco)
        for i in range(-100, 101, 10):
            if i != 0:
                # Marcas en X
                x, y = self.coordenada_pantalla(i, 0)
                pygame.draw.line(self.pantalla, self.BLANCO, (x, y - 4), (x, y + 4), 1)
                texto = self.fuente_normal.render(str(i), True, self.BLANCO)
                self.pantalla.blit(texto, (x - 10, y + 8))

                # Marcas en Y
                x, y = self.coordenada_pantalla(0, i)
                pygame.draw.line(self.pantalla, self.BLANCO, (x - 4, y), (x + 4, y), 1)
                texto = self.fuente_normal.render(str(i), True, self.BLANCO)
                self.pantalla.blit(texto, (x - 20, y - 8))
        
        # Etiquetas de ejes
        # Etiquetas de ejes (colocadas en el borde del rect) - blanco
        texto_x = self.fuente_normal.render("X", True, self.BLANCO)
        texto_y = self.fuente_normal.render("Y", True, self.BLANCO)
        self.pantalla.blit(texto_x, (self.plano_rect.x + self.plano_rect.width - 25, self.centro_y + 8))
        self.pantalla.blit(texto_y, (self.centro_x + 8, self.plano_rect.y + 8))
        
        # Origen
        texto_origen = self.fuente_pequeña.render("O", True, self.BLANCO)
        self.pantalla.blit(texto_origen, (self.centro_x - 8, self.centro_y + 8))
    
    def dibujar_avion(self, x, y, color, id_avion, angulo=0, resaltado=False):
        """
        Dibuja un avión en el plano.

        Args:
            x: Coordenada X
            y: Coordenada Y
            color: Color del avión
            id_avion: ID del avión
            angulo: Ángulo de dirección en grados
            resaltado: Si es True, dibuja con mayor tamaño
        """
        x_pantalla, y_pantalla = self.coordenada_pantalla(x, y)
        
        # Dibuja punto (círculo) con tamaño ligeramente mayor para mayor visibilidad
        radio = 6 if resaltado else 5
        pygame.draw.circle(self.pantalla, color, (x_pantalla, y_pantalla), radio)
        pygame.draw.circle(self.pantalla, self.NEGRO, (x_pantalla, y_pantalla), radio, 1)
        
        # Etiqueta con sólo ID del avión (sin coordenadas)
        texto = self.fuente_pequeña.render(f"A{id_avion}", True, color)
        self.pantalla.blit(texto, (x_pantalla + 15, y_pantalla - 15))
    
    def dibujar_historial(self, historial, color):
        """Dibuja el historial de posiciones (rastro)."""
        if len(historial) > 1:
            puntos_pantalla = [self.coordenada_pantalla(x, y) for x, y in historial]
            # Dibuja líneas con opacidad decreciente
            for i in range(len(puntos_pantalla) - 1):
                # Usa un color con menor brillo para el historial
                p1 = puntos_pantalla[i]
                p2 = puntos_pantalla[i + 1]
                pygame.draw.line(self.pantalla, color, p1, p2, 1)
    
    def dibujar_pareja_mas_cercana(self, pareja):
        """
        Dibuja la pareja más cercana con línea y resalta los aviones.
        
        Args:
            pareja: Objeto Pareja con los dos aviones más cercanos
        """
        if not pareja or not pareja.punto1 or not pareja.punto2:
            return
        
        # Obtener coordenadas en pantalla
        x1, y1 = self.coordenada_pantalla(pareja.punto1.x, pareja.punto1.y)
        x2, y2 = self.coordenada_pantalla(pareja.punto2.x, pareja.punto2.y)
        
        # No dibujamos la línea entre aviones para evitar distracciones;
        # los aviones ya se resaltan individualmente cuando forman la pareja.
    
    def dibujar_interfaz(self, estadisticas, pareja_cercana=None, stats_algoritmo=None, colision=False, input_mode=False, campos=None, input_index=0, parejas_riesgo=None, extra_fields=None, extra_index=-1):
        """Dibuja la interfaz de usuario en el panel izquierdo.

        Si `input_mode` es True, muestra cajas de texto para los campos proporcionados
        en `campos` (lista de tuples (clave, valor)). Si es False, muestra la información
        normal de estadísticas.
        """
        # Panel izquierdo padding
        x_pad = 10
        y_pos = 10

        # Título (blanco)
        titulo = self.fuente_grande.render("Sistema de monitoreo", True, self.BLANCO)
        self.pantalla.blit(titulo, (x_pad, y_pos))
        y_pos += 40

        if input_mode and campos is not None:
            # Asegurar que todo lo que dibujemos para el panel izquierdo quede
            # dentro del área del mismo (evitar superposición con el plano derecho)
            left_clip = pygame.Rect(0, 0, self.left_panel_width, self.alto)
            self.pantalla.set_clip(left_clip)
            # Dibujar SOLO campos de entrada (sin duplicar información)
            box_x = x_pad
            # Hacer las cajas ligeramente más angostas para dar más margen
            box_w = max(60, self.left_panel_width - 2 * x_pad - 30)
            # Aumentar la altura de la caja para permitir una segunda línea
            box_h = 44
            label_height = 22  # Altura para la etiqueta
            # Incrementar spacing para evitar colisión con la siguiente etiqueta
            spacing = 80  # Espacio total entre campos

            for i, (clave, valor) in enumerate(campos):
                # Etiqueta (blanca)
                etiqueta = self.fuente_normal.render(f"{clave}", True, self.BLANCO)
                self.pantalla.blit(etiqueta, (box_x, y_pos))

                # Caja (debajo de la etiqueta) - fondo gris oscuro
                rect = pygame.Rect(box_x, y_pos + label_height + 4, box_w, box_h)
                pygame.draw.rect(self.pantalla, (60, 60, 60), rect)
                borde_color = (0, 120, 215) if i == input_index else self.GRIS
                pygame.draw.rect(self.pantalla, borde_color, rect, 2)

                # Valor dentro de la caja (blanco)
                texto_val = valor if valor is not None else ''
                # Ajustar el texto para mostrar la mayor cantidad de palabras
                # completas en la línea principal y, si hay resto (palabra cortada
                # o texto sobrante), mostrarlo en una segunda línea justo debajo
                display_text, overflow = self._split_text_for_box(texto_val, self.fuente_normal, box_w - 12)
                linea = self.fuente_normal.render(display_text, True, self.BLANCO)
                self.pantalla.blit(linea, (rect.x + 8, rect.y + 6))
                if overflow:
                    # Dibujar overflow dentro de la zona gris (segunda línea)
                    y_over = rect.y + 6 + self.fuente_normal.get_height()
                    overflow_line = self.fuente_pequeña.render(overflow, True, (200, 200, 200))
                    self.pantalla.blit(overflow_line, (rect.x + 8, y_over))

                y_pos += spacing

            # Hint (gris claro)
            hint = self.fuente_pequeña.render("INGRESE LOS VALORES Y PRESIONE ENTER PARA INICIAR", True, (200, 200, 200))
            self.pantalla.blit(hint, (x_pad, y_pos + 8))

            # Si el controlador pasó un mensaje de error, dibujarlo debajo
            try:
                error_msg = estadisticas.get('__input_error__')
            except Exception:
                error_msg = None
            if error_msg:
                err = self.fuente_normal.render(error_msg, True, (220, 100, 100))
                self.pantalla.blit(err, (x_pad, y_pos + 36))

            # Restaurar clip para que la vista del plano pueda dibujarse encima
            self.pantalla.set_clip(None)

        else:
            # Información general (SOLO lo esencial, sin duplicación) - blanco
            info = [
                f"Aviones: {estadisticas.get('cantidad_aviones', estadisticas.get('CANTIDAD_AVIONES', 0))}",
            ]

            # Lista de parejas en riesgo (mostrar pares formateados)
            pr = parejas_riesgo or []
            # Preparar pares como lista de tokens "A# - A#"
            try:
                lista_pares = [f"A{p.punto1.id} - A{p.punto2.id}" for p in pr if p and p.punto1 and p.punto2]
            except Exception:
                lista_pares = []

            info.append(f"PAREJAS EN RIESGO: {len(pr)}")

            # Dibujar la primera línea de info (Aviones)
            if info:
                linea = self.fuente_normal.render(info[0], True, self.BLANCO)
                self.pantalla.blit(linea, (x_pad, y_pos))
                y_pos += 26

            # ═══════════════════════════════════════════════════════
            # SECCIÓN 1: LISTA DE PAREJAS EN RIESGO (Scrolleable)
            # ═══════════════════════════════════════════════════════
            
            # Línea separadora superior
            pygame.draw.line(self.pantalla, (80, 80, 80), 
                           (x_pad, y_pos), 
                           (self.left_panel_width - x_pad, y_pos), 1)
            y_pos += 8
            
            # Título de parejas
            titulo_parejas = self.fuente_normal.render("PAREJAS EN RIESGO", True, (100, 200, 100))
            self.pantalla.blit(titulo_parejas, (x_pad, y_pos))
            y_pos += 26

            # Área visible para la lista de parejas en el panel izquierdo
            # IMPORTANTE: Dejar espacio para los campos extras abajo
            altura_campos_extras = 200  # Espacio reservado para agregar/eliminar
            inicio_lista_y = y_pos
            fin_lista_y = self.alto - altura_campos_extras - 10
            alto_linea = 18

            # Contenido total y ajuste del scroll
            total_parejas = len(lista_pares)
            contenido_alto = total_parejas * alto_linea
            vista_alto = max(0, fin_lista_y - inicio_lista_y)
            # Limitar el scroll dentro de los rangos válidos
            max_scroll = max(0, contenido_alto - vista_alto)
            self.left_panel_scroll = min(max(self.left_panel_scroll, 0), max_scroll)

            # Fondo para área de parejas
            area_parejas = pygame.Rect(x_pad, inicio_lista_y, self.left_panel_width - 2*x_pad, vista_alto)
            pygame.draw.rect(self.pantalla, (40, 40, 40), area_parejas)
            pygame.draw.rect(self.pantalla, (80, 80, 80), area_parejas, 1)

            # Activar clip para el área de la lista y dibujar cada pareja con offset de scroll
            lista_rect = pygame.Rect(0, inicio_lista_y, self.left_panel_width, vista_alto)
            self.pantalla.set_clip(lista_rect)
            for i, texto_par in enumerate(lista_pares):
                y_line = inicio_lista_y + i * alto_linea - self.left_panel_scroll
                linea = self.fuente_normal.render(texto_par, True, self.BLANCO)
                self.pantalla.blit(linea, (x_pad + 6, y_line))
            # Restaurar clip
            self.pantalla.set_clip(None)

            # Dibujar barra de scroll si es necesario
            if max_scroll > 0 and vista_alto > 0:
                barra_x = self.left_panel_width - 10
                barra_rect = pygame.Rect(barra_x, inicio_lista_y, 8, vista_alto)
                pygame.draw.rect(self.pantalla, (50, 50, 50), barra_rect)
                thumb_h = max(15, int(vista_alto * (vista_alto / max(contenido_alto, 1))))
                thumb_y = inicio_lista_y + int((self.left_panel_scroll / max_scroll) * (vista_alto - thumb_h)) if max_scroll > 0 else inicio_lista_y
                thumb_rect = pygame.Rect(barra_x, thumb_y, 8, thumb_h)
                pygame.draw.rect(self.pantalla, (120, 180, 255), thumb_rect)
                pygame.draw.rect(self.pantalla, (150, 200, 255), thumb_rect, 1)

            # Hint para área de parejas
            if total_parejas > 0 and vista_alto > 0:
                hint_y = fin_lista_y + 4
                hint = self.fuente_pequeña.render("Rueda/Arrastra para navegar", True, (150, 150, 150))
                self.pantalla.blit(hint, (x_pad, hint_y))
            
            # ═══════════════════════════════════════════════════════
            # SECCIÓN 2: AGREGAR/ELIMINAR AVIONES (CON SCROLL)
            # ═══════════════════════════════════════════════════════
            
            # Línea separadora superior
            y_control_inicio = self.alto - 240
            pygame.draw.line(self.pantalla, (80, 80, 80), 
                           (x_pad, y_control_inicio - 5), 
                           (self.left_panel_width - x_pad, y_control_inicio - 5), 1)
            
            # Área scrollable para controles
            control_area_height = 180
            control_rect = pygame.Rect(x_pad - 5, y_control_inicio, self.left_panel_width - 2 * x_pad + 10, control_area_height)
            
            # Crear surface temporal para renderizar con clip
            control_surface = pygame.Surface((control_rect.width, control_rect.height))
            control_surface.fill((30, 30, 35))
            
            # Título de control
            titulo_control = self.fuente_normal.render("GESTIÓN DE AVIONES", True, (100, 200, 100))
            control_surface.blit(titulo_control, (5, 5))
            
            y_pos = 35
            
            # Dibujar campos extras (agregar/eliminar aviones)
            if extra_fields:
                box_w = max(60, control_rect.width - 20)
                box_h = 50
                label_height = 18
                spacing = 75
                
                # Calcular altura total necesaria
                total_height_needed = len(extra_fields) * spacing + 35
                max_scroll = max(0, total_height_needed - control_area_height + 40)
                
                # Limitar scroll
                self.extra_fields_scroll = min(max(self.extra_fields_scroll, 0), max_scroll)
                
                # Dibujar con offset de scroll
                y_content = y_pos - self.extra_fields_scroll
                
                for i, (clave, valor) in enumerate(extra_fields):
                    y_field = y_content + i * spacing
                    
                    # Solo dibujar si está visible
                    if y_field + spacing > 0 and y_field < control_area_height:
                        # Etiqueta
                        etiqueta = self.fuente_pequeña.render(f"{clave}", True, (100, 200, 100))
                        control_surface.blit(etiqueta, (10, y_field))
                        
                        # Caja de entrada
                        rect = pygame.Rect(10, y_field + label_height + 2, box_w - 20, box_h)
                        pygame.draw.rect(control_surface, (50, 70, 50), rect)
                        borde_color = (100, 255, 100) if i == extra_index else (80, 100, 80)
                        pygame.draw.rect(control_surface, borde_color, rect, 2)
                        
                        # Valor dentro de la caja
                        texto_val = valor if valor is not None else ''
                        linea = self.fuente_normal.render(texto_val, True, (100, 200, 100))
                        control_surface.blit(linea, (rect.x + 8, rect.y + 8))
            
            # Blit de surface al pantalla
            self.pantalla.blit(control_surface, control_rect.topleft)
            
            # Borde del área de control
            pygame.draw.rect(self.pantalla, (80, 80, 80), control_rect, 1)
            
            # Barra de scroll para control (si es necesario)
            if extra_fields and total_height_needed > control_area_height:
                scrollbar_x = self.left_panel_width - 12
                scrollbar_y = y_control_inicio
                scrollbar_h = control_area_height
                
                # Fondo de scrollbar
                pygame.draw.rect(self.pantalla, (50, 50, 50), 
                               pygame.Rect(scrollbar_x, scrollbar_y, 8, scrollbar_h))
                
                # Thumb de scrollbar
                thumb_h = max(20, int((control_area_height / total_height_needed) * scrollbar_h))
                thumb_y = scrollbar_y + int((self.extra_fields_scroll / max_scroll) * (scrollbar_h - thumb_h)) if max_scroll > 0 else scrollbar_y
                pygame.draw.rect(self.pantalla, (100, 150, 100), 
                               pygame.Rect(scrollbar_x, thumb_y, 8, thumb_h))
            
            # Controles al final del panel (siempre visible)
            y_hints = self.alto - 80
            
            # Línea separadora
            pygame.draw.line(self.pantalla, (80, 80, 80), 
                           (x_pad, y_hints - 8), 
                           (self.left_panel_width - x_pad, y_hints - 8), 1)
            
            # Fondo para hints (área destacada)
            hints_bg_rect = pygame.Rect(0, y_hints - 10, self.left_panel_width, self.alto - (y_hints - 10))
            pygame.draw.rect(self.pantalla, (40, 40, 45), hints_bg_rect)
            pygame.draw.line(self.pantalla, (100, 150, 100), (0, y_hints - 10), (self.left_panel_width, y_hints - 10), 2)
            
            # Hints con múltiples líneas - TAMAÑO GRANDE
            hints_lines = [
                "ESC: Volver",
                "ENTER: Aplicar",
              
            ]
            
            y_hint_pos = y_hints + 5
            for line_idx, hint_text in enumerate(hints_lines):
                # Usar fuente normal para hints (más grande que mini)
                if hint_text.startswith("━"):
                    # Línea separadora visual
                    hint_render = self.fuente_mini.render(hint_text, True, (80, 120, 80))
                else:
                    hint_render = self.fuente_pequeña.render(hint_text, True, (150, 200, 150))
                
                # Centrar hints
                hint_width = hint_render.get_width()
                x_hint = x_pad + (self.left_panel_width - 2 * x_pad - hint_width) // 2
                self.pantalla.blit(hint_render, (x_hint, y_hint_pos + line_idx * 13))
    
    def dibujar(self, aviones, estadisticas, pareja_cercana=None, stats_algoritmo=None, mostrar_historial=False, colision=False, input_mode=False, campos=None, input_index=0, umbral=15, parejas_riesgo=None, extra_fields=None, extra_index=-1):
        """Dibuja la escena completa."""
        # Fondo general (negro)
        self.pantalla.fill(self.NEGRO)

        # Panel izquierdo de información / entradas (gris oscuro)
        panel_rect = pygame.Rect(0, 0, self.left_panel_width, self.alto)
        pygame.draw.rect(self.pantalla, (30, 30, 30), panel_rect)
        pygame.draw.rect(self.pantalla, self.GRIS, panel_rect, 1)
        
        # Activar clipping para que nada se dibuje fuera del recuadro del plano
        self.pantalla.set_clip(self.plano_rect)
        
        # Dibuja fondo de cuadrícula dentro del rect del plano (opcional)
        if self.mostrar_grid:
            for i in range(-int(self.rango), int(self.rango) + 1, 40):
                x, y = self.coordenada_pantalla(i, -self.rango)
                x2, y2 = self.coordenada_pantalla(i, self.rango)
                pygame.draw.line(self.pantalla, self.GRIS_CLARO, (x, y), (x2, y2), 1)

                x, y = self.coordenada_pantalla(-self.rango, i)
                x2, y2 = self.coordenada_pantalla(self.rango, i)
                pygame.draw.line(self.pantalla, self.GRIS_CLARO, (x, y), (x2, y2), 1)
        
        # Dibuja ejes
        self.dibujar_ejes()
        
        # Dibuja historial si está habilitado
        if mostrar_historial:
            for idx, avion in enumerate(aviones):
                color = self.colores_aviones[idx % len(self.colores_aviones)]
                self.dibujar_historial(avion.obtener_historial(), color)
        
        # Preparar parejas en riesgo: conjunto de ids y lista
        parejas_riesgo = parejas_riesgo or []
        ids_riesgo = set()
        for p in parejas_riesgo:
            if p and p.punto1 and p.punto2:
                ids_riesgo.add(p.punto1.id)
                ids_riesgo.add(p.punto2.id)

        # No dibujar líneas entre parejas: sólo resaltar puntos en riesgo

        # Dibuja aviones: si forman parte de alguna pareja en riesgo los resaltamos en rojo
        for idx, avion in enumerate(aviones):
            x, y = avion.obtener_posicion()
            if avion.id_avion in ids_riesgo:
                color = self.ROJO
                resaltado = True
            elif pareja_cercana and pareja_cercana.punto1 and avion.id_avion in {pareja_cercana.punto1.id, pareja_cercana.punto2.id} and pareja_cercana.distancia <= umbral:
                color = self.ROJO
                resaltado = True
            else:
                color = self.AMARILLO
                resaltado = False

            self.dibujar_avion(x, y, color, avion.id_avion, avion.angulo, resaltado)
        
        # Dibuja línea de pareja más cercana
        self.dibujar_pareja_mas_cercana(pareja_cercana)
        
        # Desactivar clipping para dibujar la interfaz sin restricciones
        self.pantalla.set_clip(None)

        # Dibuja interfaz (panel izquierdo) -> pasar también parejas_riesgo y umbral
        kwargs = dict(input_mode=input_mode, campos=campos, input_index=input_index, parejas_riesgo=parejas_riesgo, extra_fields=extra_fields, extra_index=extra_index)
        self.dibujar_interfaz(estadisticas, pareja_cercana, stats_algoritmo, colision, **kwargs)
        
        # Ajustar el rect del plano si el panel de parejas está visible
        if self.mostrar_panel_parejas and parejas_riesgo:
            # Acotar el plano para que no se sobreponga con el panel lateral
            self.plano_rect = pygame.Rect(self.left_panel_width, 0, 
                                         self.ancho - self.left_panel_width - self.panel_parejas_ancho, 
                                         self.alto)
            self.centro_x = self.plano_rect.x + self.plano_rect.width // 2
            self._calcular_escala()
            
            # Dibuja panel lateral de parejas
            self.dibujar_panel_parejas_lateral(parejas_riesgo)
        else:
            # Restaurar rect del plano a su tamaño completo
            self.plano_rect = pygame.Rect(self.left_panel_width, 0, 
                                         self.ancho - self.left_panel_width, 
                                         self.alto)
            self.centro_x = self.plano_rect.x + self.plano_rect.width // 2
            self._calcular_escala()

        pygame.display.flip()

    def dibujar_parametros_overlay(self, campos, indice_activo, buffer_texto):
        """
        Dibuja un pequeño panel para editar parámetros: campos es lista de tuples (clave, valor)
        indice_activo: índice del campo activo
        buffer_texto: texto actualmente escrito para el campo activo
        """
        # Panel semi-transparente
        ancho_panel = 360
        alto_panel = 140
        x0 = 20
        y0 = 80
        s = pygame.Surface((ancho_panel, alto_panel))
        s.set_alpha(220)
        s.fill((240, 240, 240))
        self.pantalla.blit(s, (x0, y0))

        titulo = self.fuente_grande.render("Parámetros (P para cerrar)", True, self.NEGRO)
        self.pantalla.blit(titulo, (x0 + 10, y0 + 8))

        y = y0 + 42
        for i, (clave, valor) in enumerate(campos):
            if i == indice_activo:
                texto = f"> {clave}: {buffer_texto}"
            else:
                texto = f"  {clave}: {valor}"

            linea = self.fuente_normal.render(texto, True, self.NEGRO)
            self.pantalla.blit(linea, (x0 + 12, y))
            y += 28

    def dibujar_panel_parejas_lateral(self, parejas_riesgo):
        """
        Dibuja un panel lateral derecho mostrando todas las parejas en riesgo
        en una lista scrolleable con distancias.
        
        Args:
            parejas_riesgo: Lista de objetos Pareja
        """
        # Panel lateral en el lado derecho
        panel_x = self.ancho - self.panel_parejas_ancho
        panel_y = 0
        
        # Fondo del panel (gris oscuro)
        panel_rect = pygame.Rect(panel_x, panel_y, self.panel_parejas_ancho, self.alto)
        pygame.draw.rect(self.pantalla, (35, 35, 35), panel_rect)
        pygame.draw.rect(self.pantalla, (100, 150, 255), panel_rect, 2)
        
        # Título
        titulo_text = f"PAREJAS EN RIESGO ({len(parejas_riesgo)})"
        titulo = self.fuente_pequeña.render(titulo_text, True, (100, 150, 255))
        self.pantalla.blit(titulo, (panel_x + 10, panel_y + 8))
        
        # Línea separadora
        sep_y = panel_y + 28
        pygame.draw.line(self.pantalla, (80, 80, 80), 
                        (panel_x + 5, sep_y), 
                        (self.ancho - 5, sep_y), 1)
        
        # Área de contenido
        contenido_x = panel_x + 8
        contenido_y = sep_y + 8
        contenido_max_y = self.alto - 5
        alto_fila = 18
        
        # Dibujar cada pareja
        fila_index = 0
        for pareja in parejas_riesgo:
            if pareja and pareja.punto1 and pareja.punto2:
                # Calcular posición con scroll
                fila_y = contenido_y + fila_index * alto_fila - self.panel_parejas_scroll
                
                # Si está fuera del área visible, saltar
                if fila_y > contenido_max_y or fila_y + alto_fila < contenido_y:
                    fila_index += 1
                    continue
                
                # Formatear la información: "A0-A5 (12.34)"
                pareja_str = f"A{pareja.punto1.id}-A{pareja.punto2.id}"
                dist_str = f"({pareja.distancia:.1f})"
                
                # Color según distancia
                if pareja.distancia <= 15:
                    color = (255, 80, 80)  # Rojo más brillante
                else:
                    color = (100, 200, 100)  # Verde
                
                # Renderizar en línea
                linea = self.fuente_mini.render(f"{pareja_str} {dist_str}", True, color)
                self.pantalla.blit(linea, (contenido_x, fila_y))
                
                fila_index += 1
        
        # Barra de scroll (si hay muchas parejas)
        total_parejas = len([p for p in parejas_riesgo if p and p.punto1 and p.punto2])
        area_scroll_alto = contenido_max_y - contenido_y
        
        if total_parejas * alto_fila > area_scroll_alto:
            # Barra de fondo
            barra_x = self.ancho - 12
            barra_rect = pygame.Rect(barra_x, contenido_y, 8, area_scroll_alto)
            pygame.draw.rect(self.pantalla, (50, 50, 50), barra_rect)
            
            # Posición del thumb
            total_scroll = max(1, total_parejas * alto_fila - area_scroll_alto)
            thumb_altura = max(15, area_scroll_alto * area_scroll_alto / (total_parejas * alto_fila))
            thumb_y = contenido_y + (self.panel_parejas_scroll / total_scroll) * (area_scroll_alto - thumb_altura)
            thumb_rect = pygame.Rect(barra_x, thumb_y, 8, thumb_altura)
            
            # Dibujar thumb con efecto hover
            pygame.draw.rect(self.pantalla, (120, 180, 255), thumb_rect)
            pygame.draw.rect(self.pantalla, (150, 200, 255), thumb_rect, 1)
        
        # Hint al pie
        hint_text = "CLIC + ARRASTRA BARRA | P: cerrar"
        hint = self.fuente_mini.render(hint_text, True, (150, 150, 150))
        self.pantalla.blit(hint, (contenido_x, self.alto - 22))

    def obtener_fps(self):
        """Retorna los FPS actuales."""
        return self.reloj.get_fps()

    def _split_text_for_box(self, text, font, max_width):
        """Split `text` so the first returned value fits within `max_width`.

        Returns a tuple (line, overflow). `line` is the text that fits (prefer
        whole words). `overflow` is the remaining text (may start with the
        part of a word that didn't fit) that should be drawn below the box.
        """
        if not text:
            return '', ''
        try:
            full_w = font.size(text)[0]
        except Exception:
            return text, ''
        if full_w <= max_width:
            return text, ''

        # Prefer whole words on the first line
        if ' ' in text:
            words = text.split(' ')
            line = ''
            for i, word in enumerate(words):
                cand = (line + (' ' if line else '') + word).strip()
                if font.size(cand)[0] <= max_width:
                    line = cand
                else:
                    # The current word doesn't fit on the first line.
                    # The overflow should include this word and the rest.
                    rest = ' '.join(words[i:])
                    return line, rest
            # If loop finishes, the entire text fit (shouldn't happen due to earlier check)
            return line, ''

        # No spaces (single long token), split at char boundary: show leftmost chunk that fits
        chunk = ''
        for ch in text:
            if font.size(chunk + ch)[0] <= max_width:
                chunk += ch
            else:
                break
        overflow = text[len(chunk):]
        return chunk, overflow
    
    def obtener_fps(self):
        """Retorna los FPS actuales."""
        return self.reloj.get_fps()

    def ajustar_tamano(self, nuevo_ancho, nuevo_alto):
        """Ajusta el tamaño de la ventana y recalcula rects/escala.

        Este método debe llamarse cuando el usuario cambia el tamaño
        de la ventana (por ejemplo, al maximizar)."""
        # Guardar nuevos tamaños
        self.ancho = max(200, int(nuevo_ancho))
        self.alto = max(200, int(nuevo_alto))

        # Recrear la superficie de pantalla manteniendo la bandera RESIZABLE
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto), pygame.RESIZABLE)

        # Recalcular rectángulo del plano (panel izquierdo mantiene su ancho)
        self.plano_rect = pygame.Rect(self.left_panel_width, 0, self.ancho - self.left_panel_width, self.alto)

        # Recalcular centro y escala
        self.centro_x = self.plano_rect.x + self.plano_rect.width // 2
        self.centro_y = self.plano_rect.y + self.plano_rect.height // 2
        self._calcular_escala()

        # Ajustar el reloj (no necesario, pero asegurar consistencia)
        self.reloj = pygame.time.Clock()

    def _calcular_escala(self):
        """Calcula la escala interna aplicando zoom."""
        base = (min(self.plano_rect.width, self.plano_rect.height) // 2) / max(1, self.rango)
        # Aplicar zoom con límites razonables
        self.zoom = max(0.2, min(self.zoom, 5.0))
        self.escala = base * self.zoom

    def ajustar_zoom(self, factor):
        """Ajusta el zoom multiplicando el factor dado (ej. 1.1 para +10%)."""
        try:
            self.zoom *= factor
            # Recalcular escala aplicando nuevo zoom
            self._calcular_escala()
        except Exception:
            pass
    
    def tick(self, fps=60):
        """Controla los FPS."""
        self.reloj.tick(fps)
    
    def cerrar(self):
        """Cierra pygame."""
        pygame.quit()
