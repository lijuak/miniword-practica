import re
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout


class WordCounterWidget(QWidget):
    """
    Widget reutilizable que muestra estadísticas de texto en tiempo real.
    
    Señales:
        conteoActualizado(int, int): Emitida cuando cambian las palabras y caracteres.
                                     Parámetros: (palabras, caracteres)
    
    Parámetros de configuración:
        wpm (int): Palabras por minuto para calcular tiempo de lectura (default: 200)
        mostrarPalabras (bool): Mostrar contador de palabras (default: True)
        mostrarCaracteres (bool): Mostrar contador de caracteres (default: True)
        mostrarTiempoLectura (bool): Mostrar tiempo de lectura estimado (default: True)
    """
    
    # Señal personalizada que emite (palabras, caracteres)
    conteoActualizado = pyqtSignal(int, int)

    def __init__(self, wpm=200, mostrarPalabras=True, mostrarCaracteres=True, 
                 mostrarTiempoLectura=True, parent=None):
        """
        Constructor del widget contador de palabras.
        
        Args:
            wpm (int): Palabras por minuto para calcular tiempo de lectura
            mostrarPalabras (bool): Si True, muestra el contador de palabras
            mostrarCaracteres (bool): Si True, muestra el contador de caracteres
            mostrarTiempoLectura (bool): Si True, muestra el tiempo estimado de lectura
            parent (QWidget): Widget padre (opcional)
        """
        super().__init__(parent)
        
        # Validar y guardar configuración
        self.wpm = max(1, int(wpm))  # Mínimo 1 palabra por minuto
        self.mostrarPalabras = bool(mostrarPalabras)
        self.mostrarCaracteres = bool(mostrarCaracteres)
        self.mostrarTiempoLectura = bool(mostrarTiempoLectura)

        # Crear labels para cada métrica
        self.lblP = QLabel("Palabras: 0")
        self.lblC = QLabel("Caracteres: 0")
        self.lblT = QLabel("Lectura: 0 min")

        # Configurar layout horizontal
        lay = QHBoxLayout(self)
        lay.setContentsMargins(6, 2, 6, 2)
        lay.setSpacing(12)
        lay.addWidget(self.lblP)
        lay.addWidget(self.lblC)
        lay.addWidget(self.lblT)
        lay.addStretch()

        # Aplicar configuración de visibilidad
        self._apply_visibility()

    def _apply_visibility(self):
        """Aplica la configuración de visibilidad a los labels."""
        self.lblP.setVisible(self.mostrarPalabras)
        self.lblC.setVisible(self.mostrarCaracteres)
        self.lblT.setVisible(self.mostrarTiempoLectura)

    def update_from_text(self, text: str):
        """
        Actualiza los contadores basándose en el texto proporcionado.
        
        Este método:
        1. Cuenta las palabras usando expresión regular
        2. Cuenta los caracteres totales
        3. Calcula el tiempo de lectura estimado
        4. Actualiza los labels visuales
        5. Emite la señal conteoActualizado
        
        Args:
            text (str): Texto a analizar
        """
        text = text or ""
        
        # Contar palabras usando regex (busca secuencias de caracteres alfanuméricos)
        palabras = len(re.findall(r"\b\w+\b", text))
        
        # Contar caracteres totales
        caracteres = len(text)
        
        # Calcular tiempo de lectura en segundos
        seg = int((palabras / self.wpm) * 60) if self.wpm > 0 else 0

        # Actualizar labels
        self.lblP.setText(f"Palabras: {palabras}")
        self.lblC.setText(f"Caracteres: {caracteres}")
        
        # Formatear tiempo de lectura (segundos o minutos)
        if seg < 60:
            self.lblT.setText(f"Lectura: {seg}s")
        else:
            minutos = round(seg / 60)
            self.lblT.setText(f"Lectura: {minutos} min")

        # Emitir señal con los valores actualizados
        self.conteoActualizado.emit(palabras, caracteres)
