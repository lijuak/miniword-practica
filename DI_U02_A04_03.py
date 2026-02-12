import os
import platform
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence, QColor, QFont, QTextCursor, QTextCharFormat, QTextDocument
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction,
    QToolBar, QLabel, QFileDialog, QMessageBox,
    QColorDialog, QFontDialog, QInputDialog,
    QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QCheckBox, QDockWidget
)

# Importar componente reutilizable
from contadorWidget import WordCounterWidget


class MiniWord(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mini Word - PyQt5")
        self.current_file = ""

        
        self.text_area = QTextEdit()
        self.setCentralWidget(self.text_area)

       
        self.highlight_selections = []

        
        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()
        self.create_search_panel()

    def create_menu(self):
        barra_menus = self.menuBar()

        menu_archivo = barra_menus.addMenu("&Archivo")

        act_nuevo = QAction("Nuevo", self)
        act_nuevo.setShortcut(QKeySequence.New)
        act_nuevo.triggered.connect(self.nuevo)
        menu_archivo.addAction(act_nuevo)

        act_abrir = QAction("Abrir", self)
        act_abrir.setShortcut(QKeySequence.Open)
        act_abrir.triggered.connect(self.abrir)
        menu_archivo.addAction(act_abrir)

        act_guardar = QAction("Guardar", self)
        act_guardar.setShortcut(QKeySequence.Save)
        act_guardar.triggered.connect(self.guardar)
        menu_archivo.addAction(act_guardar)

        menu_archivo.addSeparator()
        act_salir = QAction("Salir", self)
        act_salir.triggered.connect(self.close)
        menu_archivo.addAction(act_salir)

        menu_editar = barra_menus.addMenu("&Editar")

        act_deshacer = QAction("Deshacer", self)
        act_deshacer.setShortcut(QKeySequence.Undo)
        act_deshacer.triggered.connect(self.text_area.undo)

        act_rehacer = QAction("Rehacer", self)
        act_rehacer.setShortcut(QKeySequence.Redo)
        act_rehacer.triggered.connect(self.text_area.redo)

        menu_editar.addAction(act_deshacer)
        menu_editar.addAction(act_rehacer)
        menu_editar.addSeparator()

        act_cortar = QAction("Cortar", self)
        act_cortar.setShortcut(QKeySequence.Cut)
        act_cortar.triggered.connect(self.text_area.cut)

        act_copiar = QAction("Copiar", self)
        act_copiar.setShortcut(QKeySequence.Copy)
        act_copiar.triggered.connect(self.text_area.copy)

        act_pegar = QAction("Pegar", self)
        act_pegar.setShortcut(QKeySequence.Paste)
        act_pegar.triggered.connect(self.text_area.paste)

        menu_editar.addAction(act_cortar)
        menu_editar.addAction(act_copiar)
        menu_editar.addAction(act_pegar)

        menu_editar.addSeparator()

        act_buscar = QAction("Buscar", self)
        act_buscar.setShortcut(QKeySequence.Find)
        act_buscar.triggered.connect(lambda: self.focus_search_input())
        menu_editar.addAction(act_buscar)

        act_reemplazar = QAction("Reemplazar", self)
        act_reemplazar.triggered.connect(lambda: self.focus_replace_input())
        menu_editar.addAction(act_reemplazar)

        self.edit_actions = [
            act_nuevo, act_abrir, act_guardar,
            act_deshacer, act_rehacer,
            act_cortar, act_copiar, act_pegar,
            act_buscar, act_reemplazar
        ]

        menu_pers = barra_menus.addMenu("&Personalizar")

        act_color = QAction("Color de fondo", self)
        act_color.triggered.connect(self.cambiar_color)
        menu_pers.addAction(act_color)

        act_fuente = QAction("Cambiar fuente", self)
        act_fuente.triggered.connect(self.cambiar_fuente)
        menu_pers.addAction(act_fuente)

    def create_toolbar(self):
        toolbar = QToolBar("Barra de herramientas")
        self.addToolBar(toolbar)

        for action in self.edit_actions:
            toolbar.addAction(action)

    def create_statusbar(self):
        # Crear el widget contador con señales
        self.word_counter = WordCounterWidget(
            wpm=200,
            mostrarPalabras=True,
            mostrarCaracteres=True,
            mostrarTiempoLectura=True
        )
        
        # Conectar el cambio de texto al método update_from_text del widget
        self.text_area.textChanged.connect(
            lambda: self.word_counter.update_from_text(self.text_area.toPlainText())
        )
        
        # (Opcional) Conectar la señal para logging o procesamiento adicional
        # self.word_counter.conteoActualizado.connect(self.on_conteo_actualizado)

        barra_estado = self.statusBar()
        barra_estado.addPermanentWidget(QLabel(platform.system()))
        barra_estado.addPermanentWidget(self.word_counter)
        barra_estado.showMessage("Listo.", 3000)
    
    # (Opcional) Método para recibir la señal del widget
    # def on_conteo_actualizado(self, palabras, caracteres):
    #     print(f"Señal recibida: {palabras} palabras, {caracteres} caracteres")

    
    def nuevo(self):
        self.text_area.clear()
        self.current_file = ""
        self.statusBar().showMessage("Documento nuevo.")

    def abrir(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir archivo")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.text_area.setPlainText(f.read())
                self.current_file = file_path
                self.statusBar().showMessage("Archivo abierto.")
                self.clear_highlight()
            except Exception:
                QMessageBox.warning(self, "Error", "No se pudo abrir el archivo.")

    def guardar(self):
        if not self.current_file:
            self.current_file, _ = QFileDialog.getSaveFileName(self, "Guardar archivo")
            if not self.current_file:
                return
        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text_area.toPlainText())
            self.statusBar().showMessage("Archivo guardado.")
        except Exception:
            QMessageBox.warning(self, "Error", "No se pudo guardar el archivo.")

   
    def create_search_panel(self):
        dock = QDockWidget("Buscar / Reemplazar avanzado", self)
        dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)

        panel = QWidget()
        layout = QVBoxLayout()

        
        self.buscar_input = QLineEdit()
        self.buscar_input.setPlaceholderText("Texto a buscar")
        layout.addWidget(self.buscar_input)

        
        self.match_case = QCheckBox("Coincidir mayúsc/minúsc")
        self.whole_word = QCheckBox("Coincidir palabra completa")
        layout.addWidget(self.match_case)
        layout.addWidget(self.whole_word)

        
        btn_siguiente = QPushButton("Buscar siguiente")
        btn_siguiente.clicked.connect(self.buscar_siguiente)
        layout.addWidget(btn_siguiente)

        btn_anterior = QPushButton("Buscar anterior")
        btn_anterior.clicked.connect(self.buscar_anterior)
        layout.addWidget(btn_anterior)

        btn_todos = QPushButton("Buscar todas las ocurrencias")
        btn_todos.clicked.connect(self.buscar_todos)
        layout.addWidget(btn_todos)

        
        self.reemplazar_input = QLineEdit()
        self.reemplazar_input.setPlaceholderText("Reemplazar por...")
        layout.addWidget(self.reemplazar_input)

        btn_reemplazar = QPushButton("Reemplazar")
        btn_reemplazar.clicked.connect(self.reemplazar_uno)
        layout.addWidget(btn_reemplazar)

        btn_reemplazar_todo = QPushButton("Reemplazar todos")
        btn_reemplazar_todo.clicked.connect(self.reemplazar_todos)
        layout.addWidget(btn_reemplazar_todo)

       
        btn_limpiar = QPushButton("Limpiar resaltados")
        btn_limpiar.clicked.connect(self.clear_highlight)
        layout.addWidget(btn_limpiar)

        panel.setLayout(layout)
        dock.setWidget(panel)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

    def focus_search_input(self):
        self.buscar_input.setFocus()

    def focus_replace_input(self):
        self.reemplazar_input.setFocus()

    def get_find_flags(self):
        flags = QTextDocument.FindFlags()
        if self.match_case.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.whole_word.isChecked():
            flags |= QTextDocument.FindWholeWords
        return flags

    def buscar_siguiente(self):
        texto = self.buscar_input.text()
        if texto:
            found = self.text_area.find(texto, self.get_find_flags())
            if not found:
                
                self.statusBar().showMessage("No encontrado (siguiente).")

    def buscar_anterior(self):
        texto = self.buscar_input.text()
        if texto:
            found = self.text_area.find(texto, self.get_find_flags() | QTextDocument.FindBackward)
            if not found:
                self.statusBar().showMessage("No encontrado (anterior).")

    def buscar_todos(self):
        texto = self.buscar_input.text()
        if not texto:
            return

        self.clear_highlight()

        document = self.text_area.document()
        pos = 0

        while True:
            cursor = document.find(texto, pos, self.get_find_flags())
            if cursor.isNull():
                break
          
            extra = QTextEdit.ExtraSelection()
            extra.cursor = cursor
            fmt = QTextCharFormat()
            fmt.setBackground(QColor("yellow"))
            extra.format = fmt
            self.highlight_selections.append(extra)
            pos = cursor.selectionEnd()

        self.text_area.setExtraSelections(self.highlight_selections)
        self.statusBar().showMessage(f"{len(self.highlight_selections)} ocurrencia(s) resaltada(s).")

    def clear_highlight(self):
        self.highlight_selections = []
        self.text_area.setExtraSelections([])

    def reemplazar_uno(self):
        buscar = self.buscar_input.text()
        reemplazar = self.reemplazar_input.text()

        if buscar == "":
            return

        cursor = self.text_area.textCursor()

        
        if cursor.hasSelection() and cursor.selectedText() == buscar:
            cursor.insertText(reemplazar)
            self.statusBar().showMessage("Reemplazado (uno).")
        else:
           
            found = self.text_area.find(buscar, self.get_find_flags())
            if found:
                cur = self.text_area.textCursor()
                if cur.hasSelection() and cur.selectedText() == buscar:
                    cur.insertText(reemplazar)
                    self.statusBar().showMessage("Reemplazado (uno).")
            else:
                self.statusBar().showMessage("No encontrado para reemplazar.")

       
        self.clear_highlight()

    def reemplazar_todos(self):
        buscar = self.buscar_input.text()
        reemplazar = self.reemplazar_input.text()

        if buscar == "":
            return

        document = self.text_area.document()

      
        count = 0
        flags = self.get_find_flags()

        while True:
            cursor = document.find(buscar, pos, flags)
            if cursor.isNull():
                break
            cursor.beginEditBlock()
            cursor.insertText(reemplazar)
            cursor.endEditBlock()
            count += 1
            pos = cursor.position() 

        self.statusBar().showMessage(f"Reemplazadas {count} ocurrencia(s).")
        self.clear_highlight()

    def cambiar_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_area.setStyleSheet(f"background-color: {color.name()};")

    def cambiar_fuente(self):
        fuente, ok = QFontDialog.getFont(self)
        if ok:
            self.text_area.setFont(fuente)

    # Método update_word_count() eliminado - ahora usa WordCounterWidget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiniWord()
    ventana.resize(900, 600)
    ventana.show()
    sys.exit(app.exec_())
