from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/Registro.ui")

class Registro(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None

        self.btn_registrar.clicked.connect(self.on_registrar_click)
        self.btn_volver.clicked.connect(self.on_volver_click)

    def on_registrar_click(self):
        dni = self.lineEdit_dni.text().strip()
        nombre = self.lineEdit_nombre.text().strip()
        ape1 = self.lineEdit_apellido1.text().strip()
        ape2 = self.lineEdit_apellido2.text().strip()
        email = self.lineEdit_email.text().strip()
        password = self.lineEdit_pass.text().strip()

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
    def controlador(self, ref):
        self._controlador = ref