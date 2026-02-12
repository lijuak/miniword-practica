import speech_recognition as sr
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QColor


class AudioRecognitionThread(QThread):
    """
    Hilo separado para capturar y procesar audio sin bloquear la UI.
    """
    textoReconocido = pyqtSignal(str)
    errorOcurrido = pyqtSignal(str)
    
    def __init__(self, language='es-ES'):
        super().__init__()
        self.language = language
    
    def run(self):
        """
        Ejecuta la captura y reconocimiento de voz.
        """
        recognizer = sr.Recognizer()
        
        try:
            # Verificar que hay micrófonos disponibles
            mic_list = sr.Microphone.list_microphone_names()
            if not mic_list:
                self.errorOcurrido.emit("No se detectó ningún micrófono. Conecta un micrófono e intenta de nuevo.")
                return
            
            # Usar el micrófono como fuente de audio
            with sr.Microphone() as source:
                # Ajustar el ruido ambiental
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Capturar audio (timeout de 5 segundos de silencio)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            # Reconocer el texto usando Google Speech Recognition
            texto = recognizer.recognize_google(audio, language=self.language)
            self.textoReconocido.emit(texto)
            
        except sr.WaitTimeoutError:
            self.errorOcurrido.emit("No se detectó audio. Intenta hablar más cerca del micrófono.")
        except sr.UnknownValueError:
            self.errorOcurrido.emit("No se pudo entender el audio. Intenta hablar más claro.")
        except sr.RequestError as e:
            self.errorOcurrido.emit(f"Error de conexión: {str(e)}")
        except (OSError, AttributeError) as e:
            self.errorOcurrido.emit("No se pudo acceder al micrófono. Verifica que esté conectado y que la aplicación tenga permisos.")
        except Exception as e:
            self.errorOcurrido.emit(f"Error inesperado: {str(e)}")


class AudioWidget(QWidget):
    """
    Widget reutilizable para reconocimiento de voz.
    
    Señales:
        textoReconocido(str): Emitida cuando se reconoce texto del audio.
                              Parámetro: texto reconocido
    
    Parámetros:
        language (str): Código de idioma para reconocimiento (default: 'es-ES' para español)
        parent (QWidget): Widget padre (opcional)
    """
    
    # Señal que emite el texto reconocido
    textoReconocido = pyqtSignal(str)
    
    def __init__(self, language='es-ES', parent=None):
        """
        Constructor del widget de audio.
        
        Args:
            language (str): Código de idioma ('es-ES', 'en-US', 'fr-FR', etc.)
            parent (QWidget): Widget padre (opcional)
        """
        super().__init__(parent)
        self.language = language
        self.recording_thread = None
        
        # Crear botón de grabación
        self.btn_record = QPushButton("🎤 Dictar")
        self.btn_record.setToolTip("Haz clic y habla para dictar texto")
        self.btn_record.clicked.connect(self.toggle_recording)
        
        # Estilo del botón
        self.btn_record.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.btn_record)
    
    def toggle_recording(self):
        """
        Inicia o detiene la grabación.
        """
        if self.recording_thread and self.recording_thread.isRunning():
            # Ya está grabando, no hacer nada
            return
        
        self.iniciar_grabacion()
    
    def iniciar_grabacion(self):
        """
        Inicia la captura y reconocimiento de audio en un hilo separado.
        """
        # Cambiar estado del botón
        self.btn_record.setText("🔴 Grabando...")
        self.btn_record.setEnabled(False)
        self.btn_record.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        
        # Crear y configurar el hilo
        self.recording_thread = AudioRecognitionThread(self.language)
        self.recording_thread.textoReconocido.connect(self.on_texto_reconocido)
        self.recording_thread.errorOcurrido.connect(self.on_error)
        self.recording_thread.finished.connect(self.on_finished)
        
        # Iniciar el hilo
        self.recording_thread.start()
    
    def on_texto_reconocido(self, texto):
        """
        Slot que recibe el texto reconocido y emite la señal.
        
        Args:
            texto (str): Texto reconocido del audio
        """
        # Cambiar estado a "Procesando..."
        self.btn_record.setText("⏳ Procesando...")
        
        # Emitir señal con el texto
        self.textoReconocido.emit(texto)
    
    def on_error(self, mensaje_error):
        """
        Maneja los errores del reconocimiento de voz.
        
        Args:
            mensaje_error (str): Descripción del error
        """
        QMessageBox.warning(self, "Error de Reconocimiento", mensaje_error)
    
    def on_finished(self):
        """
        Restablece el botón al estado inicial cuando termina el reconocimiento.
        """
        self.btn_record.setText("🎤 Dictar")
        self.btn_record.setEnabled(True)
        self.btn_record.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
    
    def set_language(self, language):
        """
        Cambia el idioma de reconocimiento.
        
        Args:
            language (str): Código de idioma ('es-ES', 'en-US', etc.)
        """
        self.language = language
