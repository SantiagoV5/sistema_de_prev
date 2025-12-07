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
    LEFT_PANEL_WIDTH = 320
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
    
    def dibujar_interfaz(self, estadisticas, pareja_cercana=None, stats_algoritmo=None, colision=False, input_mode=False, campos=None, input_index=0, parejas_riesgo=None):
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
            hint = self.fuente_pequeña.render("INGRESE LOS VALORES Y PRESIONE ENTER PARA INICIAR", True, (200, 200, 200))
            self.pantalla.blit(hint, (x_pad, y_pos + 8))

        else:
            # Información general (SOLO lo esencial, sin duplicación) - blanco
            info = [
                f"Aviones: {estadisticas.get('CANTIDAD_AVIONES', 0)}",
            ]

            # Lista de parejas en riesgo (mostrar pares formateados)
            pr = parejas_riesgo or []
            # Preparar pares como lista de tokens "A# - A#"
            try:
                lista_pares = [f"A{p.punto1.id} - A{p.punto2.id}" for p in pr if p and p.punto1 and p.punto2]
            except Exception:
                lista_pares = []

            # Construir líneas envueltas para que no se salgan del panel izquierdo
            pair_lines = []
            if lista_pares:
                x_pad_inner = 10
                max_w = self.left_panel_width - 2 * x_pad_inner
                # Primer prefijo
                prefix = "PAREJAS: ["
                current = prefix
                for i, token in enumerate(lista_pares):
                    token_text = (", " if current != prefix else " ") + token
                    # Probar si cabe
                    if self.fuente_normal.size(current + token_text + ("]" if i == len(lista_pares) - 1 else ""))[0] <= max_w:
                        current += token_text
                        # Si es el último, cerrar corchete
                        if i == len(lista_pares) - 1:
                            current += "]"
                            pair_lines.append(current)
                    else:
                        # Añadir la línea actual y comenzar nueva línea con token (sin prefijo)
                        pair_lines.append(current)
                        current = "  " + token
                        if i == len(lista_pares) - 1:
                            current += "]"
                            pair_lines.append(current)
                # Si quedó texto sin añadir
                if current and (not pair_lines or pair_lines[-1] != current):
                    pair_lines.append(current)
            else:
                pair_lines = ["PAREJAS: []"]

            info.append(f"PAREJAS EN RIESGO: {len(pr)}")

            # Dibujar la primera línea de info (Aviones)
            if info:
                linea = self.fuente_normal.render(info[0], True, self.BLANCO)
                self.pantalla.blit(linea, (x_pad, y_pos))
                y_pos += 26

            # Dibujar las líneas de parejas (envueltas) si existen
            for pl in pair_lines:
                linea = self.fuente_normal.render(pl, True, self.BLANCO)
                self.pantalla.blit(linea, (x_pad, y_pos))
                y_pos += 20

            # Dibujar el resto de las líneas de info (ej. Parejas en riesgo)
            for texto_info in info[1:]:
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
    
    def dibujar(self, aviones, estadisticas, pareja_cercana=None, stats_algoritmo=None, mostrar_historial=False, colision=False, input_mode=False, campos=None, input_index=0, umbral=15, parejas_riesgo=None):
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
        kwargs = dict(input_mode=input_mode, campos=campos, input_index=input_index, parejas_riesgo=parejas_riesgo)
        self.dibujar_interfaz(estadisticas, pareja_cercana, stats_algoritmo, colision, **kwargs)

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
