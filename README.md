# MiniWord - Editor de Texto con PyQt5

Editor de texto simple pero potente desarrollado con PyQt5, con funcionalidades avanzadas de edición, búsqueda y componentes reutilizables.

## 🚀 Características

### 1. Gestión de archivos
- Crear nuevo documento
- Abrir archivos de texto
- Guardar documentos
- Guardado en UTF-8

### 2. Edición de texto
- Deshacer
- Rehacer
- Cortar, copiar y pegar
- Contador de palabras en tiempo real

### 3. Búsqueda y reemplazo avanzada

Se incorpora un panel lateral fijo que permite:
- Buscar texto hacia delante
- Buscar texto hacia atrás
- Buscar todas las coincidencias
- Reemplazar una sola coincidencia
- Reemplazar todas
- Resaltar coincidencias encontradas

### 4. Personalización
- Cambiar el color de fondo
- Cambiar la fuente del texto

### 5. Funcionalidades extra añadidas
- Panel lateral de búsqueda persistente
- Botones explícitos para cada modo de búsqueda
- Resaltado temporal de coincidencias
- Diseño más intuitivo para acciones de búsqueda y reemplazo

---

## 📊 Componente Reutilizable: WordCounterWidget con Señales

### ¿Qué son las Señales en PyQt5?

Las **señales** son un mecanismo fundamental en PyQt5 que permite la **comunicación entre objetos** de forma desacoplada. Cuando ocurre un evento (como un clic, un cambio de texto, o cualquier acción personalizada), un objeto puede **emitir una señal**, y otros objetos pueden **conectarse** a esa señal para responder al evento.

**Beneficios de usar señales:**
- ✅ **Desacoplamiento**: El emisor no necesita conocer a los receptores
- ✅ **Reutilización**: Los componentes pueden usarse en diferentes contextos
- ✅ **Flexibilidad**: Múltiples objetos pueden responder a la misma señal
- ✅ **Mantenibilidad**: El código es más fácil de entender y modificar

### El Componente WordCounterWidget

`WordCounterWidget` es un componente reutilizable que muestra estadísticas de texto en tiempo real. Utiliza una señal personalizada para notificar cuando los contadores se actualizan.

**Archivo:** `contadorWidget.py`

#### Señal Personalizada

```python
class WordCounterWidget(QWidget):
    # Señal que emite (palabras: int, caracteres: int)
    conteoActualizado = pyqtSignal(int, int)
```

Esta señal se emite cada vez que el texto cambia, permitiendo que otros componentes reaccionen a los cambios.

#### Parámetros de Configuración

```python
WordCounterWidget(
    wpm=200,                      # Palabras por minuto para calcular tiempo de lectura
    mostrarPalabras=True,         # Mostrar contador de palabras
    mostrarCaracteres=True,      # Mostrar contador de caracteres
    mostrarTiempoLectura=True,   # Mostrar tiempo estimado de lectura
    parent=None                   # Widget padre
)
```

#### Métodos Principales

**`update_from_text(text: str)`**
- Actualiza todos los contadores basándose en el texto
- Emite la señal `conteoActualizado`
- Calcula automáticamente: palabras, caracteres y tiempo de lectura

### Ejemplo de Uso

#### Uso Básico
```python
from contadorWidget import WordCounterWidget

# Crear el widget
contador = WordCounterWidget()

# Actualizar con texto
contador.update_from_text("Hola mundo")
```

#### Uso Avanzado con Señales
```python
# Crear el widget con configuración personalizada
contador = WordCounterWidget(
    wpm=150,                    # Lectura más lenta
    mostrarCaracteres=False     # Ocultar caracteres
)

# Conectar a la señal para recibir notificaciones
def on_texto_cambiado(palabras, caracteres):
    print(f"Texto actualizado: {palabras} palabras, {caracteres} caracteres")

contador.conteoActualizado.connect(on_texto_cambiado)

# Actualizar texto (esto emitirá la señal)
contador.update_from_text("Este es un texto de ejemplo")
```

#### Integración en MiniWord

En `DI_U02_A04_03.py`:

```python
def create_statusbar(self):
    # Crear el widget contador
    self.word_counter = WordCounterWidget(
        wpm=200,
        mostrarPalabras=True,
        mostrarCaracteres=True,
        mostrarTiempoLectura=True
    )
    
    # Conectar cambios de texto al widget
    self.text_area.textChanged.connect(
        lambda: self.word_counter.update_from_text(self.text_area.toPlainText())
    )
    
    # Añadir a la barra de estado
    self.statusBar().addPermanentWidget(self.word_counter)
```

### Flujo de Eventos con Señales

```
Usuario escribe texto
        ↓
QTextEdit emite textChanged
        ↓
Lambda llama update_from_text()
        ↓
WordCounterWidget calcula estadísticas
        ↓
WordCounterWidget emite conteoActualizado (señal personalizada)
        ↓
Cualquier objeto conectado recibe la señal
```

### Ventajas sobre el Método Anterior

**Antes (sin componente reutilizable):**
```python
def update_word_count(self):
    texto = self.text_area.toPlainText().strip()
    palabras = len(texto.split()) if texto else 0
    self.word_label.setText(f"Palabras: {palabras}")
```

**Ahora (con WordCounterWidget):**
- ✅ Código más limpio y organizado
- ✅ Componente reutilizable en otros proyectos
- ✅ Funcionalidades adicionales (caracteres, tiempo de lectura)
- ✅ Configuración flexible
- ✅ Uso de señales para comunicación desacoplada
- ✅ Mejor mantenibilidad y extensibilidad

---

## 🛠️ Instalación y Ejecución

### Requisitos
```bash
pip install PyQt5
```

### Ejecutar la aplicación
```bash
python DI_U02_A04_03.py
```

---

## 📝 Estructura del Proyecto

```
miniword-practica/
├── DI_U02_A04_03.py      # Aplicación principal
├── contadorWidget.py      # Componente reutilizable con señales
└── README.md              # Este archivo
```

---

## 🎓 Conceptos Aprendidos

- **Señales y Slots en PyQt5**: Comunicación entre objetos
- **Componentes Reutilizables**: Diseño modular y escalable
- **pyqtSignal**: Creación de señales personalizadas
- **Layouts**: Organización de widgets (QHBoxLayout)
- **Expresiones Regulares**: Conteo preciso de palabras con `re.findall(r"\b\w+\b", text)`

---

## 📚 Referencias

- [PyQt5 Signals and Slots](https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html)
- [Qt for Python Documentation](https://doc.qt.io/qtforpython/)
- [Regular Expressions in Python](https://docs.python.org/3/library/re.html)
