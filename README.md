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

## 🎤 Reconocimiento de Voz (Speech Recognition)

### Componente AudioWidget

`AudioWidget` es un componente reutilizable que permite **dictar texto por voz** usando el micrófono.

**Archivo:** `audioWidget.py`

#### Señal Personalizada

```python
class AudioWidget(QWidget):
    # Señal que emite el texto reconocido
    textoReconocido = pyqtSignal(str)
```

#### Características

- **Reconocimiento en tiempo real**: Captura audio del micrófono y lo convierte a texto
- **Hilo separado**: No bloquea la interfaz durante la grabación
- **Manejo de errores robusto**: Detecta problemas de micrófono, conexión, y audio ininteligible
- **Multiidioma**: Soporta español, inglés, francés, etc.
- **Feedback visual**: El botón cambia de color según el estado (🎤 → 🔴 Grabando → ⏳ Procesando)

#### Cómo Usar

1. **Hacer clic en el botón "🎤 Dictar"** en la barra de herramientas
2. **Hablar claramente** cerca del micrófono
3. **Esperar** a que procese (el botón mostrará "⏳ Procesando...")
4. **El texto aparecerá** automáticamente en el editor

#### Tecnologías Utilizadas

- **PyAudio**: Captura de audio desde el micrófono
- **SpeechRecognition**: Biblioteca para reconocimiento de voz
- **Google Speech Recognition API**: Motor gratuito de reconocimiento (requiere internet)

#### Configuración de Idioma

Por defecto el widget está configurado para español (`es-ES`). Puedes cambiarlo:

```python
# En DI_U02_A04_03.py
self.audio_widget = AudioWidget(language='en-US')  # Inglés
self.audio_widget = AudioWidget(language='fr-FR')  # Francés
```

**Idiomas soportados:**
- `es-ES` - Español (España)
- `es-MX` - Español (México)
- `en-US` - Inglés (Estados Unidos)
- `en-GB` - Inglés (Reino Unido)
- `fr-FR` - Francés
- `de-DE` - Alemán
- Y muchos más...

### Integración en MiniWord

```python
def create_toolbar(self):
    # ... otras acciones ...
    
    # Añadir widget de audio
    self.audio_widget = AudioWidget(language='es-ES')
    self.audio_widget.textoReconocido.connect(self.insertar_texto_dictado)
    toolbar.addWidget(self.audio_widget)

def insertar_texto_dictado(self, texto):
    """Inserta el texto dictado en la posición del cursor"""
    cursor = self.text_area.textCursor()
    cursor.insertText(texto + " ")
```

### Manejo de Errores

El widget maneja automáticamente varios tipos de errores:

| Error | Causa | Solución |
|-------|-------|----------|
| "No se detectó audio" | Silencio o micrófono desconectado | Verificar micrófono y hablar más cerca |
| "No se pudo entender el audio" | Audio poco claro o ruido de fondo | Hablar más claro en ambiente silencioso |
| "Error de conexión" | Sin conexión a internet | Verificar conexión a internet |
| "No se detectó micrófono" | Micrófono no disponible | Conectar micrófono y reiniciar app |

### Flujo de Eventos

```
Usuario hace clic en 🎤 Dictar
        ↓
AudioWidget inicia hilo de grabación
        ↓
Botón cambia a 🔴 Grabando...
        ↓
Captura audio del micrófono (máx 10 segundos)
        ↓
Botón cambia a ⏳ Procesando...
        ↓
Google Speech API convierte audio a texto
        ↓
AudioWidget emite señal textoReconocido(texto)
        ↓
MiniWord recibe texto y lo inserta en el editor
        ↓
Botón vuelve a 🎤 Dictar
```

### Requisitos

> [!IMPORTANT]
> - **Micrófono funcional** conectado al ordenador
> - **Conexión a internet** (para Google Speech Recognition API)
> - **Ambiente silencioso** para mejor reconocimiento
> - **PyAudio instalado** (ver sección de instalación)

---

## 🛠️ Instalación y Ejecución

### Requisitos
```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# O instalar manualmente
pip install PyQt5
pip install SpeechRecognition
pip install pyaudio
```

> [!WARNING]
> **Instalación de PyAudio en Windows:**
> Si `pip install pyaudio` falla, usa:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### Ejecutar la aplicación
```bash
python DI_U02_A04_03.py
```

### Probar Speech Recognition

1. Ejecutar la aplicación
2. Hacer clic en el botón "🎤 Dictar" en la barra de herramientas
3. Hablar claramente: "Hola, esto es una prueba de dictado"
4. El texto aparecerá automáticamente en el editor

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
