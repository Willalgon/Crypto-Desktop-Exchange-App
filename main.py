from PyQt5.QtWidgets import QApplication

from src.vista.Login import MiVentana
from src.vista.Registro import VentanaRegistro
from src.vista.Principal import VentanaPrincipal
from src.modelo.Logica import Logica 
from src.controlador.ControladorPrincipal import ControladorPrincipal

if __name__ == "__main__":
    app = QApplication([])
    
    
    ventana_login = MiVentana()
    ventana_registro=VentanaRegistro()
    ventana_principal=VentanaPrincipal()

    modelo = Logica()
    
    controlador = ControladorPrincipal(ventana_login, ventana_registro, ventana_principal, modelo)
    
    ventana_login.controlador = controlador
    ventana_registro.controlador=controlador
    ventana_principal.controlador=controlador
    controlador.abrirIniciarSesion()
    
    app.exec_()