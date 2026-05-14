# main.py
from PyQt5.QtWidgets import QApplication
from src.vista.Login    import Login
from src.vista.Registro import VentanaRegistro
from src.modelo.Logica  import Logica
from src.controlador.ControladorPrincipal import ControladorPrincipal

if __name__ == "__main__":
    app = QApplication([])

    ventana_login = Login()
    ventana_registro = VentanaRegistro()
    modelo = Logica()

    controlador = ControladorPrincipal(ventana_login, ventana_registro, modelo)

    ventana_login.controlador = controlador
    ventana_registro.controlador = controlador

    controlador.abrirIniciarSesion()
    app.exec_()