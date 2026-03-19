import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from src.Modelo.vo.LoginVo import LoginVo

Form, Window = uic.loadUiType("/Users/samuelllamas/Documents/data/IngSoftware/github/PROYECTO_SOFTWARE/src/vista/ui/MainWindow.ui")

class MiVentana(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
       
        self.Aceptar.clicked.connect(self.on_button_click)

    def on_button_click(self):

        nombre = self.lineEdit.text()
        password = self.lineEdit_2.text()
        
        print("Nombre capturado:", nombre)
        print("Password capturada:", password)

        
        login = LoginVo(nombre, password)
        
        print("Objeto VO creado:", login)
        
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())