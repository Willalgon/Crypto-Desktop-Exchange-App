from PyQt5.QtWidgets import QApplication

from controlador.ControladorPrincipal import ControladorPrincipal


class Login():
    def __init__(self):
        self.setupUi(self)
        self._controlador = None
        self.Aceptar.clicked.connect(self.on_login_click)

    def on_login_click(self):
        email = self.lineEdit.text().strip()
        contrasena = self.lineEdit2.text().strip()
        if self._controlador:
            self._controlador.comprobarLogin(email, contrasena)

    def lanzar_aviso(self, mensaje="Error en el Login"):
        QMessageBox.warning(self, "Aviso", mensaje)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref):
        self._controlador = ref

# ------
# main.py
app = QApplication([])

ventana_login = Login()
controlador = ControladorPrincipal(ventana_login)
ventana_login._controlador = controlador



# ------
# ControladorPrincipal.py
class ControladorPrincipal:
    def __init__(self, ventana_login):
        self.__vista_login = ventana_login

    def comprobarLogin(self, email, password):
        if not email and not password:
            self.__vista_login.lanzar_aviso("Error en el login")

        contraseña_encriptada = self.encriptar_contraseña(password)



    def encriptar_contraseña(self, pssw):
        #encriptado de contraseña, con función extraña
        return contraseña_encriptada