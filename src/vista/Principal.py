from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtCore import Qt
Form, Window = uic.loadUiType("./src/vista/ui/VentanaPrincipal.ui")

class VentanaPrincipal(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowState(Qt.WindowMaximized)
        self._controlador = None
        # Conexiones de botones del Trader
        self.btn_logout.clicked.connect(self.on_logout_click)
        self.btn_mercado.clicked.connect(self.on_ver_mercado_click)

    def on_ver_mercado_click(self):
        if self.controlador:
            self.controlador.solicitarListaClientes() # Usamos la misma función para pedir los datos a la lógica

    def refrescar_tabla(self, lista_datos):
        # Limpia y rellena la tabla con los datos del simulacro
        self.tabla_datos.setRowCount(len(lista_datos))
        for fila, dato in enumerate(lista_datos):
            self.tabla_datos.setItem(fila, 0, QTableWidgetItem(str(dato['id'])))
            self.tabla_datos.setItem(fila, 1, QTableWidgetItem(dato['estado']))
            self.tabla_datos.setItem(fila, 2, QTableWidgetItem(dato['fecha']))
            self.tabla_datos.setItem(fila, 3, QTableWidgetItem(dato['perf']))

    def on_logout_click(self):
        if self.controlador: self.controlador.cerrarSesion()

    @property
    def controlador(self): return self._controlador
    
    @controlador.setter
    def controlador(self, val): self._controlador = val