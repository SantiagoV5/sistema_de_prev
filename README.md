# Sistema de Aviones - Plano Cartesiano (Arquitectura MVC)

## Descripción

Aplicación basada en la arquitectura **Modelo-Vista-Controlador (MVC)** que simula aviones moviéndose en un plano cartesiano. El proyecto es una extensión mejorada del programa inicial, con una estructura más robusta y escalable.

## Estructura del Proyecto

```
mvc_aviones/
├── main.py              # Punto de entrada de la aplicación
├── modelo.py            # Capa de modelo (lógica de negocio)
├── vista.py             # Capa de vista (visualización)
├── controlador.py       # Capa de controlador (interacción)
└── README.md            # Este archivo
```

## Componentes

### 1. **Modelo** (`modelo.py`)

Contiene la lógica de negocio sin conocimiento de la interfaz gráfica.

**Clases principales:**
- `Avion`: Representa un avión con posición, velocidad y dirección.
  - `mover()`: Mueve el avión según su velocidad y ángulo
  - `cambiar_direccion()`: Cambia la dirección del avión
  - `cambiar_velocidad()`: Ajusta la velocidad
  - `obtener_posicion()`: Retorna coordenadas actuales
  - `obtener_historial()`: Retorna historial de posiciones

- `GestorAviones`: Administra todos los aviones y la lógica general.
  - `generar_aviones_aleatorios()`: Crea aviones con posiciones garantizadas
  - `actualizar_aviones()`: Actualiza posiciones de todos los aviones
  - `detectar_colision()`: Detecta colisiones entre aviones
  - `calcular_distancia_entre_aviones()`: Calcula distancias
  - `obtener_estadisticas()`: Retorna datos del sistema

### 2. **Vista** (`vista.py`)

Gestiona toda la visualización usando pygame.

**Clase principal:**
- `VistaPlanoCartesiano`: Responsable de renderizar la interfaz gráfica.
  - `dibujar_ejes()`: Dibuja los ejes cartesianos
  - `dibujar_avion()`: Dibuja un avión individual
  - `dibujar_historial()`: Muestra el rastro de los aviones
  - `dibujar()`: Dibuja la escena completa
  - `dibujar_interfaz()`: Muestra información y controles

### 3. **Controlador** (`controlador.py`)

Coordina la interacción entre el modelo y la vista.

**Clase principal:**
- `ControladorAviones`: Gestor principal de la aplicación.
  - `manejar_eventos()`: Procesa input del usuario
  - `actualizar()`: Actualiza el estado del juego
  - `detectar_colisiones()`: Verifica colisiones
  - `ejecutar()`: Bucle principal

## Características

✨ **Características Implementadas:**

- ✅ **Generación aleatoria de aviones** con separación garantizada
- ✅ **Movimiento dinámico** con velocidad y ángulo personalizables
- ✅ **Detección de colisiones** entre aviones
- ✅ **Historial de posiciones** (rastro) visualizable
- ✅ **Interfaz interactiva** con información en tiempo real
- ✅ **Cuadrícula de fondo** para mejor orientación
- ✅ **Múltiples colores** para diferenciar aviones
- ✅ **Aviones rotados** según su dirección

## Controles

| Tecla | Acción |
|-------|--------|
| **ESPACIO** | Generar nuevos aviones |
| **M** | Activar/Desactivar movimiento |
| **H** | Mostrar/Ocultar historial de posiciones |
| **A** | Añadir un avión más |
| **ESC** | Salir de la aplicación |

## Requisitos

```bash
pip install pygame
```

## Cómo Ejecutar

```bash
cd mvc_aviones
python main.py
```

## Ejemplo de Uso

```python
from modelo import GestorAviones, Avion
from vista import VistaPlanoCartesiano
from controlador import ControladorAviones

# Crear controlador
controlador = ControladorAviones()

# Ejecutar aplicación
controlador.ejecutar()
```

## Extensiones Posibles

El proyecto puede extenderse con:

- 🔹 **Sistemas de waypoints**: Los aviones siguen ruta predefinida
- 🔹 **Radar visual**: Mostrar área de detección de colisiones
- 🔹 **Persistencia**: Guardar/cargar estado en archivos
- 🔹 **Controles avanzados**: Controlar aviones con mouse o teclado
- 🔹 **Estadísticas detalladas**: Distancias, velocidades, ángulos
- 🔹 **Física mejorada**: Aceleración, fricción, fuerzas
- 🔹 **Modos de juego**: Competencia, cooperación, etc.

## Diagrama MVC

```
┌─────────────────────────────────────────┐
│         Controlador (main.py)           │
│  - Maneja eventos del usuario           │
│  - Coordina modelo y vista              │
└──────────┬────────────────┬─────────────┘
           │                │
    ┌──────▼──────┐    ┌────▼────────┐
    │ Modelo      │    │ Vista       │
    │ (modelo.py) │    │ (vista.py)  │
    │             │    │             │
    │ - Avion     │    │ - Ejes      │
    │ - Gestor    │    │ - Aviones   │
    │ - Lógica    │    │ - Interfaz  │
    └─────────────┘    └─────────────┘
```

## Notas Técnicas

- **Arquitectura:** Modelo-Vista-Controlador (MVC)
- **Lenguaje:** Python 3.7+
- **Framework Gráfico:** Pygame
- **Patrón de Diseño:** Separación de responsabilidades
- **FPS:** 60 frames por segundo (configurable)

## Autor

Proyecto educativo para demostración de arquitectura MVC.

## Licencia

Este proyecto es de código abierto y disponible para propósitos educativos.
