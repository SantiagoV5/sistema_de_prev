# Mejoras en Visualización de Parejas en Riesgo

## 🎯 Problema Solucionado
Cuando hay muchos aviones (y por lo tanto muchas parejas en riesgo), el panel izquierdo no tenía suficiente espacio para mostrar todas las parejas, haciendo imposible visualizarlas todas de una sola vista.

## ✨ Soluciones Implementadas

### 1. **Panel Expandido Modal**
Se agregó un panel modal grande y centrado que aparece al presionar **P** o al hacer click en el botón "VER TODO" (cuando hay más de 3 parejas).

**Características del panel:**
- **Tabla compacta** con dos columnas:
  - Columna 1: ID de la pareja (Ej: `A0 - A2`)
  - Columna 2: Distancia entre aviones (Ej: `14.53`)
- **Colores dinámicos**: La distancia se muestra en ROJO si está en riesgo, VERDE si es segura
- **Scroll integrado**: Permite navegar por todas las parejas si hay muchas
- **Barra de desplazamiento visual**: Muestra la posición del scroll

### 2. **Interacción Intuitiva**

| Acción | Efecto |
|--------|--------|
| **P** | Abre/cierra el panel de parejas |
| **ARRIBA/ABAJO** | Desplaza el contenido del panel |
| **ESC** | Cierra el panel |
| **Click en "VER TODO"** | Abre el panel (solo visible en modo entrada) |

### 3. **Botón de Acceso Rápido**
Cuando hay más de 3 parejas en riesgo, aparece un botón en el panel izquierdo:
```
VER TODO (5 parejas)
```
Al hacerle click, se abre el panel expandido.

## 🎨 Diseño Visual

### Panel Expandido
- Fondo oscuro con borde azul brillante
- Overlay semi-transparente detrás para enfocar atención
- Encabezados claros ("Pareja" y "Distancia")
- Fuente compacta para mostrar más parejas por pantalla
- Línea separadora entre encabezados y datos

### Colores
- **Azul**: Título y borde del panel
- **Rojo**: Distancias en riesgo (≤ umbral)
- **Verde**: Distancias seguras (> umbral)
- **Blanco**: Texto principal
- **Gris**: Hint y instrucciones

## 📊 Ejemplo de Uso

1. **Inicia la aplicación**
   ```
   python main.py
   ```

2. **Ingresa parámetros**
   - Número de aviones: `20`
   - Umbral de NM: `15`

3. **Presiona P** para abrir el panel de parejas
   - Verás todas las parejas detectadas en una tabla
   - Las distancias aparecen en rojo si están en riesgo

4. **Usa ARRIBA/ABAJO** para navegar si hay muchas parejas

5. **Presiona ESC** para cerrar el panel

## 🔧 Cambios Técnicos

### Archivos Modificados

#### `vista.py`
- Se agregaron atributos: `mostrar_panel_parejas` y `scroll_parejas`
- Nuevo método: `dibujar_panel_parejas_expandido()`
- Actualizado: `dibujar_interfaz()` con botón "VER TODO"
- Actualizado: `dibujar()` para mostrar el panel cuando está activo

#### `controlador.py`
- Actualizado: `manejar_eventos()` para:
  - Detectar click en botón "VER TODO"
  - Manejar tecla **P** para toggle del panel
  - Manejar navegación con ARRIBA/ABAJO en el panel
  - Cerrar panel al presionar ESC

## 📈 Beneficios

✅ **Visualización completa**: Ver todas las parejas sin límite de espacio
✅ **Mejor legibilidad**: Tabla clara con distancias explícitas
✅ **Mejor UX**: Botón intuitivo y atajos de teclado
✅ **Información clara**: Colores indican estado (riesgo vs seguro)
✅ **Escabilidad**: Funciona bien con 2 parejas o 100+ parejas

## 🚀 Próximas Mejoras (Opcionales)

- [ ] Exportar lista de parejas a CSV
- [ ] Filtrar parejas por rango de distancia
- [ ] Ordenar parejas por distancia ascendente/descendente
- [ ] Resaltar pareja seleccionada en el plano cartesiano
