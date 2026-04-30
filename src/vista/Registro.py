from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/RegistroWindow.ui")

class VentanaRegistro(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
        self._controlador = None
        
        self.btn_registrar.clicked.connect(self.on_registrar_click)
        self.btn_volver.clicked.connect(self.on_volver_click)

    def on_registrar_click(self):
        dni = self.lineEdit_dni.text()
        nombre = self.lineEdit_nombre.text()
        ape1 = self.lineEdit_apellido1.text()
        ape2 = self.lineEdit_apellido2.text()
        email = self.lineEdit_email.text()
        password = self.lineEdit_pass.text()
        
        if self._controlador:
            self._controlador.procesarRegistro(dni, nombre, ape1, ape2, email, password)

    def on_volver_click(self):
        if self._controlador:
            self._controlador.volverAlLogin()

    def mostrarExito(self):
        QMessageBox.information(self, "Éxito", "Usuario registrado correctamente.")

    def mostrarError(self, mensaje):
        QMessageBox.warning(self, "Error", mensaje)

    @property
    def controlador(self):
        return self._controlador
    
    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador