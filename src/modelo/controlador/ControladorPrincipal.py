from src.modelo.vo.LoginVO import LoginVO
from src.modelo.Logica import Logica
class ControladorPrincipal:
    def __init__(self,ref_vista,ref_modelo):
        self.__vista=ref_vista
        self.__modelo=ref_modelo
        
    def abrirIniciarSesion(self):
        self.__vista.show()

    def comprobarLogin(self,nombre,passw):
        #Comp
        loginVO=LoginVO(nombre,passw)
        resultado=self.__modelo.hacerLogin(loginVO)

        if resultado==None:
            self.__vista.lanzaviso()
        else:
            self.__vista.close()