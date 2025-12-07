"""
Modelo: Contiene la lógica de negocio para generar y gestionar los aviones.
"""
import random
import math


class Avion:
    """Representa un avión con coordenadas en el plano cartesiano."""
    
    def __init__(self, id_avion, x, y, velocidad=1.0, angulo=0):
        """
        Inicializa un avión.
        
        Args:
            id_avion: Identificador único del avión
            x: Coordenada X
            y: Coordenada Y
            velocidad: Velocidad del avión en unidades por frame
            angulo: Ángulo de dirección en grados
        """
        self.id_avion = id_avion
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.angulo = angulo
        self.historial = [(x, y)]  # Guarda las posiciones anteriores
    
    def mover(self):
        """Mueve el avión en base a su velocidad y ángulo."""
        pass
    
    def cambiar_direccion(self, nuevo_angulo):
        """Cambia la dirección del avión."""
        pass
    
    def cambiar_velocidad(self, nueva_velocidad):
        """Cambia la velocidad del avión."""
        pass
    
    def obtener_posicion(self):
        """Retorna la posición actual del avión."""
        return (self.x, self.y)
    
    def obtener_historial(self):
        """Retorna el historial de posiciones."""
        pass
    
    def __repr__(self):
        return f"Avión {self.id_avion}: ({self.x:.2f}, {self.y:.2f})"


class GestorAviones:
    """Gestor principal de los aviones."""
    
    def __init__(self, rango_x=120, rango_y=120, rango_plano=None):
        """
        Inicializa el gestor de aviones.
        
        Args:
            rango_x: Rango en eje X (de -rango_x a +rango_x)
            rango_y: Rango en eje Y (de -rango_y a +rango_y)
        """
        self.aviones = {}
        # Compatibilidad: si se pasa rango_plano, usarlo para ambos ejes
        if rango_plano is not None:
            self.rango_x = rango_plano
            self.rango_y = rango_plano
        else:
            self.rango_x = rango_x
            self.rango_y = rango_y
        self.contador_id = 0
        self.algoritmo = AlgoritmoDividirYVencer()
        self.pareja_mas_cercana = None
        self.colisiones_evitadas = 0  # Contador de colisiones evitadas
        self.todos_fuera = False  # Flag para saber si todos salieron del plano
        self.inicial_cantidad = 0  # Cantidad inicial de aviones generados
        self.colisiones_reportadas = False  # Flag para evitar contar varias veces
    
    def generar_aviones_aleatorios(self, cantidad=2, distancia_minima=50):
        """
        Genera aviones aleatorios garantizando que estén separados.
        
        Args:
            cantidad: Cantidad de aviones a generar
            distancia_minima: Distancia mínima entre aviones
        
        Returns:
            Lista de aviones generados
        """
        aviones_generados = []
        posiciones = []
        
        for _ in range(cantidad):
            distancia = 0
            while True:
                x = random.uniform(-self.rango_x, self.rango_x)
                y = random.uniform(-self.rango_y, self.rango_y)
                
                # Verificar distancia con otros aviones
                valido = True
                for px, py in posiciones:
                    distancia = math.sqrt((x - px)**2 + (y - py)**2)
                    if distancia < distancia_minima:
                        valido = False
                        break
                
                if valido:
                    break
            
            # Crear avión con dirección aleatoria (velocidad un poco más alta)
            velocidad = random.uniform(0.10, 0.40)
            angulo = random.uniform(0, 360)
            
            avion = Avion(self.contador_id, x, y, velocidad, angulo)
            self.aviones[self.contador_id] = avion
            self.contador_id += 1
            
            posiciones.append((x, y))
            aviones_generados.append(avion)
        
        return aviones_generados
    
    def obtener_avion(self, id_avion):
        """Obtiene un avión por su ID."""
        return self.aviones.get(id_avion)
    
    def obtener_todos_aviones(self):
        """Retorna todos los aviones."""
        return list(self.aviones.values())
    
    def actualizar_aviones(self):
        """Actualiza la posición de todos los aviones."""
        pass
    
    def ejecutar_algoritmo_pareja_cercana(self):
        """Ejecuta el algoritmo Dividir y Vencer para encontrar pareja más cercana."""
        aviones_list = list(self.aviones.values())
        if len(aviones_list) >= 2:
            self.pareja_mas_cercana = self.algoritmo.encontrar_pareja_mas_cercana(aviones_list)
        return self.pareja_mas_cercana
    
    def obtener_pareja_mas_cercana(self):
        """Retorna la pareja más cercana encontrada."""
        return self.pareja_mas_cercana
    
    def obtener_estadisticas_algoritmo(self):
        """Retorna estadísticas del algoritmo ejecutado."""
        return {
            'comparaciones': self.algoritmo.comparaciones,
            'llamadas_recursivas': self.algoritmo.llamadas_recursivas
        }
    
    def calcular_distancia_entre_aviones(self, id_avion1, id_avion2):
        """Calcula la distancia entre dos aviones."""
        if id_avion1 in self.aviones and id_avion2 in self.aviones:
            x1, y1 = self.aviones[id_avion1].obtener_posicion()
            x2, y2 = self.aviones[id_avion2].obtener_posicion()
            return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return None
    
    def verificar_todos_fuera_del_plano(self):
        """Verifica si todos los aviones están fuera del plano cartesiano."""
        if not self.aviones:
            return False
        
        for avion in self.aviones.values():
            x, y = avion.obtener_posicion()
            # Si al menos un avión está dentro del rango, no todos están fuera
            if abs(x) <= self.rango_x and abs(y) <= self.rango_y:
                return False
        
        return True
    
    def incrementar_colisiones_evitadas(self):
        """Incrementa el contador de colisiones evitadas."""
        pass
    
    def detectar_colision(self, distancia_minima=10):
        """Detecta si hay colisión entre aviones."""
        pass

    def encontrar_parejas_en_riesgo(self, distancia_umbral):
        """Devuelve una lista de objetos Pareja con todas las parejas cuya
        distancia es menor o igual que `distancia_umbral`.

        Args:
            distancia_umbral: umbral en las mismas unidades del plano (float)

        Returns:
            Lista de `Pareja`.
        """
        parejas = []
        ids_aviones = list(self.aviones.keys())
        for i in range(len(ids_aviones)):
            for j in range(i + 1, len(ids_aviones)):
                dist = self.calcular_distancia_entre_aviones(ids_aviones[i], ids_aviones[j])
                if dist is not None and dist <= distancia_umbral:
                    p1 = Punto(self.aviones[ids_aviones[i]])
                    p2 = Punto(self.aviones[ids_aviones[j]])
                    parejas.append(Pareja(p1, p2, dist))
        return parejas
    
    def limpiar_aviones(self):
        """Elimina todos los aviones."""
        self.aviones.clear()
        self.contador_id = 0
    
    def obtener_estadisticas(self):
        """Retorna estadísticas del sistema."""
        return {
            'cantidad_aviones': len(self.aviones),
            'rango_x': self.rango_x,
            'rango_y': self.rango_y,
            'colisiones_evitadas': self.colisiones_evitadas,
            'todos_fuera': self.verificar_todos_fuera_del_plano(),
            'aviones': [str(a) for a in self.aviones.values()]
        }


class Punto:
    """Representa un punto en el plano con ID de avión."""
    
    def __init__(self, avion):
        self.id = avion.id_avion
        self.x = avion.x
        self.y = avion.y
        self.avion = avion
    
    def distancia_a(self, otro):
        """Calcula la distancia euclidiana a otro punto."""
        return math.sqrt((self.x - otro.x)**2 + (self.y - otro.y)**2)


class Pareja:
    """Representa una pareja de puntos con su distancia."""
    
    def __init__(self, punto1=None, punto2=None, distancia=float('inf')):
        self.punto1 = punto1
        self.punto2 = punto2
        self.distancia = distancia
    
    def __repr__(self):
        if self.punto1 and self.punto2:
            return f"Pareja(A{self.punto1.id}, A{self.punto2.id}, d={self.distancia:.2f})"
        return "Pareja(vacía)"


class AlgoritmoDividirYVencer:
    """Implementa el algoritmo de encontrar la pareja más cercana usando Dividir y Vencer."""
    
    def __init__(self):
        self.comparaciones = 0
        self.llamadas_recursivas = 0
    
    def encontrar_pareja_mas_cercana(self, aviones):
        """
        Encuentra la pareja de aviones más cercanos usando Dividir y Vencer.
        
        Args:
            aviones: Lista de objetos Avion
        
        Returns:
            Objeto Pareja con los dos aviones más cercanos
        """
        if len(aviones) < 2:
            return Pareja()
        
        # Crear puntos a partir de los aviones
        puntos = [Punto(avion) for avion in aviones]
        
        # Ordenar por coordenada X
        puntos.sort(key=lambda p: p.x)
        
        # Reiniciar contadores
        self.comparaciones = 0
        self.llamadas_recursivas = 0
        
        # Ejecutar el algoritmo
        resultado = self._dividir_y_vencer(puntos)
        
        return resultado
    
    def _dividir_y_vencer(self, puntos):
        """
        Implementación recursiva del algoritmo Dividir y Vencer.
        
        Args:
            puntos: Lista de puntos ordenados por X
        
        Returns:
            Objeto Pareja con la distancia mínima
        """
        self.llamadas_recursivas += 1
        n = len(puntos)
        
        # CASO BASE: si hay 2 o 3 puntos, usar fuerza bruta
        if n <= 3:
            return self._fuerza_bruta(puntos)
        
        # DIVIDIR: Partir en dos mitades
        medio = n // 2
        puntos_izq = puntos[:medio]
        puntos_der = puntos[medio:]
        
        # CONQUISTAR: Resolver recursivamente cada mitad
        pareja_izq = self._dividir_y_vencer(puntos_izq)
        pareja_der = self._dividir_y_vencer(puntos_der)
        
        # COMBINAR: Tomar el mínimo de ambas mitades
        d = min(pareja_izq.distancia, pareja_der.distancia)
        
        # Buscar en la franja central
        x_medio = puntos[medio].x
        franja = [p for p in puntos if abs(p.x - x_medio) < d]
        pareja_franja = self._buscar_en_franja(franja, d)
        
        # Retornar la pareja con menor distancia
        candidatas = [pareja_izq, pareja_der, pareja_franja]
        mejor = min(candidatas, key=lambda p: p.distancia)
        
        return mejor
    
    def _fuerza_bruta(self, puntos):
        """
        Encuentra la pareja más cercana por fuerza bruta.
        Usado como caso base para subproblemas pequeños.
        
        Args:
            puntos: Lista de puntos
        
        Returns:
            Objeto Pareja con la distancia mínima
        """
        mejor_pareja = Pareja()
        
        for i in range(len(puntos)):
            for j in range(i + 1, len(puntos)):
                self.comparaciones += 1
                dist = puntos[i].distancia_a(puntos[j])
                
                if dist < mejor_pareja.distancia:
                    mejor_pareja = Pareja(puntos[i], puntos[j], dist)
        
        return mejor_pareja
    
    def _buscar_en_franja(self, franja, d):
        """
        Busca en la franja central si existe pareja más cercana.
        
        Args:
            franja: Lista de puntos en la franja
            d: Distancia mínima actual
        
        Returns:
            Objeto Pareja si encuentra algo, sino Pareja vacía
        """
        mejor_pareja = Pareja()
        
        # Ordenar franja por Y
        franja.sort(key=lambda p: p.y)
        
        for i in range(len(franja)):
            j = i + 1
            # Solo revisar puntos cercanos en Y (máximo d de distancia)
            while j < len(franja) and (franja[j].y - franja[i].y) < d:
                self.comparaciones += 1
                dist = franja[i].distancia_a(franja[j])
                
                if dist < mejor_pareja.distancia:
                    mejor_pareja = Pareja(franja[i], franja[j], dist)
                
                j += 1
        
        return mejor_pareja
