"""
Vista: Maneja toda la visualización usando pygame.
"""
import pygame
import math


class VistaPlanoCartesiano:
    """Gestiona la visualización del plano cartesiano con pygame."""
    
    def __init__(self, ancho=900, alto=700, rango_x=120, rango_y=120, left_panel_width=200):
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
        # Siempre usar 120x120 para escala (ignorar rangos de entrada para evitar distorsión)
        self.rango_x = 120
        self.rango_y = 120
        # Tamaño del panel izquierdo (entradas / información)
        self.left_panel_width = left_panel_width = 320
        # Área del plano a la derecha
        self.plano_rect = pygame.Rect(self.left_panel_width, 0, self.ancho - self.left_panel_width, self.alto)

        # Para escala usamos siempre 120 (rango fijo)
        self.rango = 120
        self.pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("SISTEMA DE PREVENCIÓN DE COLISIONES DE AVIONES")
        self.reloj = pygame.time.Clock()
        
        # Centro del plano en pantalla (dentro del rectángulo derecho)
        self.centro_x = self.plano_rect.x + self.plano_rect.width // 2
        self.centro_y = self.plano_rect.y + self.plano_rect.height // 2
        # Escala basada en el tamaño del rectángulo del plano
        self.escala = (min(self.plano_rect.width, self.plano_rect.height) // 2) / self.rango
        
        # Colores (tema oscuro)
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.GRIS_CLARO = (50, 50, 50)      # Cuadrícula más oscura
        self.GRIS = (150, 150, 150)         # Bordes más claros
        self.ROJO = (255, 0, 0)
        self.AZUL = (0, 150, 255)
        self.VERDE = (0, 255, 100)
        self.NARANJA = (255, 165, 0)
        self.AMARILLO = (255, 255, 0)
        
        # Colores para aviones
        self.colores_aviones = [
            self.ROJO,
            self.AZUL,
            self.VERDE,
            self.NARANJA,
            self.AMARILLO,
            (255, 0, 255),  # Magenta
        ]
        
        # Fuentes
        self.fuente_grande = pygame.font.Font(None, 28)
        self.fuente_normal = pygame.font.Font(None, 20)
        self.fuente_pequeña = pygame.font.Font(None, 16)
        self.fuente_mini = pygame.font.Font(None, 10)
    
    def coordenada_pantalla(self, x_cart, y_cart):
        """Convierte coordenadas cartesianas a coordenadas de pantalla."""
        x_pantalla = self.centro_x + x_cart * self.escala
        y_pantalla = self.centro_y - y_cart * self.escala
        return (int(x_pantalla), int(y_pantalla))
    
    def dibujar_ejes(self):
        """Dibuja los ejes cartesianos."""
        # Eje X dentro del rect del plano (blanco)
        pygame.draw.line(self.pantalla, self.BLANCO,
                 (self.plano_rect.x, self.centro_y),
                 (self.plano_rect.x + self.plano_rect.width, self.centro_y), 2)

        # Eje Y dentro del rect del plano (blanco)
        pygame.draw.line(self.pantalla, self.BLANCO,
                 (self.centro_x, self.plano_rect.y),
                 (self.centro_x, self.plano_rect.y + self.plano_rect.height), 2)
        
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
        
        # Dibuja triángulo (avión) rotado según ángulo
        tamaño = 15 if resaltado else 12
        radianes = math.radians(angulo + 90)
        
        # Vértices del triángulo
        p1 = (
            x_pantalla + tamaño * math.cos(radianes),
            y_pantalla + tamaño * math.sin(radianes)
        )
        p2 = (
            x_pantalla + tamaño * math.cos(radianes + 2.094),
            y_pantalla + tamaño * math.sin(radianes + 2.094)
        )
        p3 = (
            x_pantalla + tamaño * math.cos(radianes + 4.189),
            y_pantalla + tamaño * math.sin(radianes + 4.189)
        )
        
        pygame.draw.polygon(self.pantalla, color, [p1, p2, p3])
        grosor = 3 if resaltado else 2
        pygame.draw.polygon(self.pantalla, self.NEGRO, [p1, p2, p3], grosor)
        
        # Etiqueta con ID y coordenadas
        texto = self.fuente_pequeña.render(f"A{id_avion}: ({x:.1f}, {y:.1f})", True, color)
        self.pantalla.blit(texto, (x_pantalla + 15, y_pantalla - 15))
    
    def dibujar_historial(self, historial, color):
        """Dibuja el historial de posiciones (rastro)."""
        if len(historial) > 1:
            puntos_pantalla = [self.coordenada_pantalla(x, y) for x, y in historial]
            # Dibuja líneas con opacidad decreciente
            for i in range(len(puntos_pantalla) - 1):
                # Usa un color con menor brillo para el historial
                pygame.draw.line(self.pantalla, color, 
                               puntos_pantalla[i], puntos_pantalla[i + 1], 1)
    
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
    
    def dibujar_interfaz(self, estadisticas, pareja_cercana=None, stats_algoritmo=None, colision=False, input_mode=False, campos=None, input_index=0):
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
            # Dibujar SOLO campos de entrada (sin duplicar información)
            box_x = x_pad
            box_w = self.left_panel_width - 2 * x_pad
            box_h = 30
            label_height = 22  # Altura para la etiqueta
            spacing = 60  # Espacio total entre campos

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
                linea = self.fuente_normal.render(texto_val, True, self.BLANCO)
                self.pantalla.blit(linea, (rect.x + 8, rect.y + 6))

                y_pos += spacing

            # Hint (gris claro)
            hint = self.fuente_pequeña.render("Ingresa los valores y presiona ENTER para INICIAR", True, (200, 200, 200))
            self.pantalla.blit(hint, (x_pad, y_pos + 8))

        else:
            # Información general (SOLO lo esencial, sin duplicación) - blanco
            info = [
                f"Aviones: {estadisticas.get('cantidad_aviones', 0)}",
            ]

            if pareja_cercana and pareja_cercana.punto1:
                info.append(f"Pareja: A{pareja_cercana.punto1.id} - A{pareja_cercana.punto2.id}")
                info.append(f"Distancia: {pareja_cercana.distancia:.2f}")
            
            # Mostrar colisiones evitadas
            colisiones_evitadas = estadisticas.get('colisiones_evitadas', 0)
            info.append(f"Colisiones evitadas: {colisiones_evitadas}")

            for texto_info in info:
                linea = self.fuente_normal.render(texto_info, True, self.BLANCO)
                self.pantalla.blit(linea, (x_pad, y_pos))
                y_pos += 26

            # Controles al final del panel (gris claro)
            y_pos = self.alto - 60
            controles = [
                "ESC: Volver a ingresar"
            ]
            for control in controles:
                linea = self.fuente_pequeña.render(control, True, (200, 200, 200))
                self.pantalla.blit(linea, (x_pad, y_pos))
                y_pos += 20
    
    def dibujar(self, aviones, estadisticas, pareja_cercana=None, stats_algoritmo=None, mostrar_historial=False, colision=False, input_mode=False, campos=None, input_index=0, umbral=15):
        """Dibuja la escena completa."""
        # Fondo general (negro)
        self.pantalla.fill(self.NEGRO)

        # Panel izquierdo de información / entradas (gris oscuro)
        panel_rect = pygame.Rect(0, 0, self.left_panel_width, self.alto)
        pygame.draw.rect(self.pantalla, (30, 30, 30), panel_rect)
        pygame.draw.rect(self.pantalla, self.GRIS, panel_rect, 1)
        
        # Activar clipping para que nada se dibuje fuera del recuadro del plano
        self.pantalla.set_clip(self.plano_rect)
        
        # Dibuja fondo de cuadrícula dentro del rect del plano
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
        
        # Dibuja aviones
        ids_pareja = set()
        if pareja_cercana and pareja_cercana.punto1:
            ids_pareja = {pareja_cercana.punto1.id, pareja_cercana.punto2.id}
        
        for idx, avion in enumerate(aviones):
            x, y = avion.obtener_posicion()
            if avion.id_avion in ids_pareja and pareja_cercana and pareja_cercana.distancia <= umbral:
                color = self.ROJO
            else:
                color = self.AMARILLO
            resaltado = False  # No cambiar tamaño, solo color
            self.dibujar_avion(x, y, color, avion.id_avion, avion.angulo, resaltado)
        
        # Dibuja línea de pareja más cercana
        self.dibujar_pareja_mas_cercana(pareja_cercana)
        
        # Desactivar clipping para dibujar la interfaz sin restricciones
        self.pantalla.set_clip(None)
        
        # Dibuja interfaz (panel izquierdo)
        self.dibujar_interfaz(estadisticas, pareja_cercana, stats_algoritmo, colision,
                      input_mode=input_mode, campos=campos, input_index=input_index)

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

    def dibujar_formulario_entrada(self, campos, indice_activo, mensaje_error=None):
        """
        Dibuja un formulario con cajas de texto para que el usuario ingrese
        los parámetros iniciales antes de comenzar la simulación.

        campos: lista de tuples (clave, valor_str)
        indice_activo: índice del campo activo (resaltado)
        mensaje_error: texto de error a mostrar (opcional)
        """
        ancho_panel = 420
        alto_panel = 220
        x0 = 40
        y0 = 60
        s = pygame.Surface((ancho_panel, alto_panel))
        s.set_alpha(230)
        s.fill((245, 245, 245))
        self.pantalla.blit(s, (x0, y0))

        titulo = self.fuente_grande.render("Parámetros iniciales", True, self.NEGRO)
        self.pantalla.blit(titulo, (x0 + 12, y0 + 8))

        # Campos: dibujar etiqueta y caja
        box_w = 320
        box_h = 28
        spacing = 44
        y = y0 + 48
        for i, (clave, valor) in enumerate(campos):
            # Etiqueta
            etiqueta = self.fuente_normal.render(f"{clave}", True, self.NEGRO)
            self.pantalla.blit(etiqueta, (x0 + 10, y + 2))

            # Caja
            rect_x = x0 + 120
            rect = pygame.Rect(rect_x, y, box_w, box_h)
            color_fondo = (255, 255, 255)
            pygame.draw.rect(self.pantalla, color_fondo, rect)

            # Borde
            borde_color = (0, 120, 215) if i == indice_activo else self.GRIS
            pygame.draw.rect(self.pantalla, borde_color, rect, 2)

            # Texto dentro de la caja
            texto_val = valor if valor is not None else ''
            linea = self.fuente_normal.render(texto_val, True, self.NEGRO)
            self.pantalla.blit(linea, (rect_x + 6, y + 4))

            y += spacing

        # Indicaciones
        hint = self.fuente_pequeña.render("Ingrese valores y presione ENTER para INICIAR", True, self.GRIS)
        self.pantalla.blit(hint, (x0 + 12, y0 + alto_panel - 36))

        if mensaje_error:
            err = self.fuente_normal.render(mensaje_error, True, (200, 0, 0))
            self.pantalla.blit(err, (x0 + 12, y0 + alto_panel - 64))
    
    def obtener_fps(self):
        """Retorna los FPS actuales."""
        return self.reloj.get_fps()
    
    def tick(self, fps=60):
        """Controla los FPS."""
        self.reloj.tick(fps)
    
    def cerrar(self):
        """Cierra pygame."""
        pygame.quit()
