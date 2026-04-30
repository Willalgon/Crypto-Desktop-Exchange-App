import hashlib
from src.modelo.vo.LoginVO import LoginVO
from src.modelo.Logica import Logica
from src.modelo.vo.RegistroVo import RegistroVo

class ControladorPrincipal:
    def __init__(self,ref_vista_login,ref_vista_registro, ref_vista_principal, ref_modelo):
        self.__vista_login=ref_vista_login
        self.__vista_registro=ref_vista_registro
        self.__vista_principal=ref_vista_principal
        self.__modelo=ref_modelo
        
    def abrirIniciarSesion(self):
        self.__vista_login.show()

    def comprobarLogin(self, nombre, passw):
        pass_encriptada = self.__encriptar_contrasena(passw)
        from src.modelo.vo.LoginVO import LoginVO
        loginVO = LoginVO(nombre, pass_encriptada)
        
        # Llamamos a la lógica (que ahora es el simulacro)
        resultado = self.__modelo.hacerLogin(loginVO)

        if resultado:
            self.__vista_login.hide()
            self.__vista_principal.show()
            # Al entrar, cargamos los datos en la tabla automáticamente
            self.solicitarListaClientes()
        else:
            self.__vista_login.lanzaraviso()

    def solicitarListaClientes(self):
        # Pide los datos de la tabla y ordena a la vista que los pinte
        datos = self.__modelo.obtenerDatosSimulados()
        self.__vista_principal.refrescar_tabla(datos)

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

    def cerrarSesion(self):
        self.__vista_principal.hide()
        self.__vista_login.show()
    
    def __encriptar_contrasena(self,contrasena):
        sha256=hashlib.sha256()
        sha256.update(contrasena.encode('utf-8'))
        return sha256.hexdigest()