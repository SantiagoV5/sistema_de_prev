# 🛩️ Sistema de Prevención de Colisiones Aéreas

---

## 📦 Requisitos Previos

- **Python**: 3.8 o superior
- **Pygame**: 2.6.1 o superior

---

## ⚙️ Instalación

### Paso 1: Instalar dependencias

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install pygame
```

---

## 🚀 Inicializar la Aplicación

### Opción 1 : Desde VS Code

1. Abre el proyecto en VS Code
2. Haz clic derecho en `main.py`
3. Selecciona "Run Python File"

---

## 📋 Configuración Inicial (Al Ejecutar)

Cuando inicies la aplicación, se te pedirá:

### 1️⃣ Número de Aviones
```
NUMERO DE AVIONES: [____]
```
- **Rango**: 1 a 500
- **Recomendado**: 10-50
- **Ejemplo**: `20`

### 2️⃣ Umbral de Colisión (NM)
```
UMBRAL DE NM: [____]
```
- **Rango**: Cualquier valor positivo
- **Recomendado**: 15
- **Ejemplo**: `15`

Presiona **ENTER** después de cada valor para continuar.

---

## 🎮 Controles Principales

| Acción | Efecto |
|--------|--------|
| **ESC** | Volver al formulario inicial |
| **ENTER** | Aplicar comando (agregar/eliminar) |
| **Rueda del Ratón** | Desplazar listas automáticamente |
| **Click + Arrastra** | Mover barras de scroll |
| **Números** | Escribir cantidad de aviones |
| **BACKSPACE** | Borrar último carácter |

---

## 📊 Interfaz

### Panel Izquierdo (Información y Control)

```
┌─────────────────────────────┐
│ Aviones: 20                 │  ← Contador
│ PAREJAS EN RIESGO: 3        │  ← Alerta
├─────────────────────────────┤
│ Lista de parejas (scrollable)│  ← Sección 1
├─────────────────────────────┤
│ AGREGAR AVIONES             │  ← Sección 2
│ [_______________]           │
│                             │
│ ELIMINAR AVIONES            │
│ [_______________]           │
├─────────────────────────────┤
│ ESC | TAB | ENTER           │  ← Sección 3
│ Rueda: Scroll               │     (Hints)
└─────────────────────────────┘
```

### Panel Derecho

- **Plano Cartesiano 2D**: Visualiza los aviones en movimiento
- **Ejes**: Coordenadas de referencia (X, Y)
- **Aviones**: Círculos de colores con etiquetas (A1, A2, etc.)

---

## ✨ Características

- ✅ Detección de colisiones con algoritmo **O(n log n)**
- ✅ **Gestión dinámica**: Agregar/eliminar aviones en tiempo real
- ✅ **Panel scrollable**: Navega listas largas fácilmente
- ✅ **Interfaz intuitiva**: Hints grandes y visibles
- ✅ **Arquitectura MVC**: Código limpio y mantenible
- ✅ **Rendimiento optimizado**: 28x más rápido que fuerza bruta

---

## 📂 Estructura del Proyecto

```
sistema_de_prev/
├── main.py                # Punto de entrada
├── modelo.py              # Lógica de aviones y algoritmo
├── vista.py               # Visualización Pygame
├── controlador.py         # Manejo de eventos
├── utilidades.py          # Funciones auxiliares
├── config.py              # Configuración centralizada
├── requirements.txt       # Dependencias
├── DOCUMENTACION.md       # Documentación completa
└── README.md              # Este archivo
```

---

## 🐛 Solución de Problemas

### "ModuleNotFoundError: No module named 'pygame'"
```bash
pip install pygame
```

### Aplicación muy lenta
- Reduce el número de aviones a menos de 100
- Cierra otras aplicaciones

### Campos no responden a clicks
- Asegúrate de estar en modo simulación (después del formulario)
- Haz clic dentro del área verde del campo

---

**¡Listo para usar! 🚀**
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


## Licencia

Este proyecto es de código abierto y disponible para propósitos educativos.
