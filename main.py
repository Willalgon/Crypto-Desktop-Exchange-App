from PyQt5.QtWidgets import QApplication, QMainWind
from PyQt5 import uic
from src.modelo.BussinessObject import BussinessObj
from src.vista.Login import MiVentana
from src.controlador.ControladorPrincipal import ControladorPrinicipal
import os.path
os.path.dirname(os.path.abspath(__file__))
if __name__=="__main__":
    app=QApplication([])
    ventana=MiVentana()
    modelo=Logica()
    controlador=ControladorPrinicpal(ventana,modelo)
    ventana.controlador=controlador
    controlador.abrirIniciarSesion()
    app.exec_()
