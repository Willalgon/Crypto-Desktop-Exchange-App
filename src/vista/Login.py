from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/MainWindow.ui")

class MiVentana(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None # Variable interna con guion bajo

        self.Aceptar.clicked.connect(self.on_button_click)
        self.btn_ir_registro.clicked.connect(self.on_registro_click)

    def on_button_click(self):
        texto_nombre = self.lineEdit.text()
        texto_contrasena = self.lineEdit_2.text()
        if self._controlador:
            self._controlador.comprobarLogin(texto_nombre, texto_contrasena)

    def on_registro_click(self):
        if self._controlador:
            self._controlador.abrirVentanaRegistro()

    def lanzaraviso(self, mensaje="Login incorrecto"):
        QMessageBox.information(self, "Info", mensaje)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador