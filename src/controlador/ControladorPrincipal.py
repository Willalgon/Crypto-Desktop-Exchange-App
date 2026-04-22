<<<<<<< HEAD
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
=======
import hashlib
from src.modelo.vo.LoginVO import LoginVO
from src.modelo.Logica import Logica
from src.modelo.vo.RegistroVo import RegistroVo
class ControladorPrincipal:
    def __init__(self,ref_vista_login,ref_vista_registro, ref_modelo):
        self.__vista_login=ref_vista_login
        self.__vista_registro=ref_vista_registro
        self.__modelo=ref_modelo
        
    def abrirIniciarSesion(self):
        self.__vista_login.show()

    def comprobarLogin(self,nombre,contrasena):
        contrasena_encriptada=self.__encriptar_contrasena(contrasena)
        loginVO=LoginVO(nombre,contrasena_encriptada)
        resultado=self.__modelo.hacerLogin(loginVO)

        if resultado==None:
            self.__vista_login.lanzaraviso()
        else:
            self.__vista_login.close()

    def abrirVentanaRegistro(self):
        self.__vista_login.hide()
        self.__vista_registro.show()

    def volverAlLogin(self):
        self.__vista_registro.hide()
        self.__vista_login.show()

    def procesarRegistro(self,dni,nombre,ape1,ape2,email,contrasena):
        contrasena_encriptada=self.__encriptar_contrasena(contrasena)
        registroVo=RegistroVo(nombre,ape1,ape2,email,dni,contrasena_encriptada)
        resultado=self.__modelo.hacerRegistro(registroVo)

        if resultado==True:
            self.__vista_registro.mostrarExito()
            self.volverAlLogin()
        else:
            self.__vista_registro.mostrarError("Error: No se pudo registrar en la Base de Datos.")

    
    def __encriptar_contrasena(self,contrasena):
        sha256=hashlib.sha256()
        sha256.update(contrasena.encode('utf-8'))
        return sha256.hexdigest()
>>>>>>> 77ee610af2f1cae1c2b645341f2832edcf5a0f26
