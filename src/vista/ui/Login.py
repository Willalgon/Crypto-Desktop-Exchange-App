import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

# Ruta a tu archivo .ui
ui_path = "/home/guillee/Documents/2AÑO/2SEMESTRE/IS/GITHUB_ULE/src/vista/ui/Login.ui"
Form, Window = uic.loadUiType(ui_path)

class MiVentana(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Conectar el botón. Asegúrate de que en el Designer se llame "Boton"
        self.Boton.clicked.connect(self.on_button_click)

    def on_button_click(self):
        # Obtenemos los textos de los inputs del Designer
        usuario = self.input_usuario.text()
        password = self.input_password.text()

        # Validación temporal (mientras no vemos bases de datos)
        if usuario == "admin" and password == "1234":
            print(f"¡Bienvenido {usuario}! Login correcto.")
        else:
            print("Error: Usuario o contraseña incorrectos.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())