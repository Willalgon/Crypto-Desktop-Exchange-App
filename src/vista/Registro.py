from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt

# 1. Cargamos el archivo XML que acabas de dibujar en QtDesigner
Form, Window = uic.loadUiType("./src/vista/ui/RegistroWindow.ui")

class VentanaRegistro(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        # 2. Pintamos la ventana en la pantalla
        self.setupUi(self)  
        self.setWindowState(Qt.WindowMaximized)
        # 3. Preparamos el bolsillo secreto para guardar la tarjeta del jefe (Controlador)
        self._controlador = None
        
        # 4. Enganchamos los botones a sus funciones
        self.btn_registrar.clicked.connect(self.on_registrar_click)
        self.btn_volver.clicked.connect(self.on_volver_click)

    # 5. Qué pasa cuando hacen clic en Registrarse
    def on_registrar_click(self):
        # Sacamos el texto puro de cada una de las cajas que bautizamos en QtDesigner
        dni = self.lineEdit_dni.text()
        nombre = self.lineEdit_nombre.text()
        ape1 = self.lineEdit_apellido1.text()
        ape2 = self.lineEdit_apellido2.text()
        email = self.lineEdit_email.text()
        password = self.lineEdit_pass.text()
        
        # Si la Vista tiene el teléfono del Controlador, le pasa todos los datos
        if self.controlador is not None:
            self.controlador.procesarRegistro(dni, nombre, ape1, ape2, email, password)
        else:
            print("Error: El controlador no está conectado a la vista Registro.")

    # 6. Qué pasa cuando hacen clic en Volver
    def on_volver_click(self):
        if self.controlador is not None:
            self.controlador.volverAlLogin()

    # 7. Funciones para lanzar avisos en la pantalla
    def mostrarExito(self):
        QMessageBox.information(self, "Éxito", "Usuario registrado correctamente.")

    def mostrarError(self, mensaje):
        QMessageBox.warning(self, "Error", mensaje)

    # 8. Las ventanillas oficiales para que el main.py pueda asignar al Controlador
    @property
    def controlador(self):
        return self._controlador
    
    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador