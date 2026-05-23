from PyQt5.QtWidgets import QMainWindow, QMessageBox # Plantilla de ventana principal y QMessageBox para las ventanas emergentes (pop-outs)
from PyQt5 import uic # para traducir xml a python

Form, Window = uic.loadUiType("src/vista/ui/Login.ui") # Form guarda los elementos visuales y Window es la base de la ventana.

class Login(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # construye la interfaz
        self._controlador = None
        self.Aceptar.clicked.connect(self.on_login_click)
        self.btn_ir_registro.clicked.connect(self.on_registro_click)

    def on_login_click(self):
        email = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()
        if self._controlador:
            self._controlador.comprobarLogin(email, password)

    def on_registro_click(self):
        if self._controlador:
            self._controlador.abrirVentanaRegistro()

    def lanzar_aviso(self, mensaje="Login incorrecto"):
        QMessageBox.warning(self, "Aviso", mensaje)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref):
        self._controlador = ref