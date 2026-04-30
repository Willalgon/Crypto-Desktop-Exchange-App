from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/MainWindow.ui")

class MiVentana(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
        self.setWindowState(Qt.WindowMaximized)
        self.controlador = None
        
        # Conexiones de botones
        self.Aceptar.clicked.connect(self.on_button_click)
        self.btn_ir_registro.clicked.connect(self.on_registro_click)

    # ... Tus funciones como on_button_click siguen igual aquí debajo ...

    # ... Siguen tus funciones (on_button_click, etc.) ...
    def on_button_click(self):
        """Esta función se ejecuta SOLO cuando el usuario hace clic en el botón."""
        
        # 4. RECOGER DATOS:
        # Usamos los nombres exactos que tienen los campos en QtDesigner (lineEdit y lineEdit_2)
        # El método .text() extrae lo que el usuario ha escrito dentro.
        texto_nombre = self.lineEdit.text() 
        texto_contrasena = self.lineEdit_2.text()
        
        # 5. DELEGAR EN EL CONTROLADOR (La regla de oro del MVC):
        # La Vista es "tonta". No sabe de bases de datos. Solo coge el texto y se lo pasa al Controlador.
        if self.controlador is not None:
            self.controlador.comprobarLogin(texto_nombre, texto_contrasena)
        else:
            print("Error: El controlador no está conectado a la vista.")

    def on_registro_click(self):
        if self.controlador is not None:
            # Le pedimos al jefe que nos cambie de ventana
            self.controlador.abrirVentanaRegistro()

    def lanzaraviso(self):
        """El controlador llamará a esta función si los datos son incorrectos."""
        QMessageBox.information(self, "Info", "Login incorrecto. Verifica tus credenciales.")

    # Getters y Setters para inyectar el controlador desde el main.py
    @property
    def controlador(self):
        return self._controlador
    
    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador