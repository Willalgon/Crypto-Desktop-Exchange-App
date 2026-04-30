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
import hashlib
import re # Necesario para validar el email con expresiones regulares
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
        if not nombre or not passw:
            self.__vista_login.lanzaraviso("Por favor, rellena todos los campos.")
            return

        pass_encriptada = self.__encriptar_contrasena(passw)
        loginVO = LoginVO(nombre, pass_encriptada)
        resultado = self.__modelo.hacerLogin(loginVO)

        if resultado:
            self.__vista_login.hide()
            self.__vista_principal.show()
            self.solicitarListaClientes()
        else:
            self.__vista_login.lanzaraviso("Login incorrecto. Verifica tus credenciales.")

    def abrirVentanaRegistro(self):
        self.__vista_login.hide()
        self.__vista_registro.show()

    def volverAlLogin(self):
        self.__vista_registro.hide()
        self.__vista_login.show()

    def procesarRegistro(self, dni, nombre, ape1, ape2, email, contrasena):
        # 1. VALIDACIÓN DE DATOS
        error = self.__validar_datos_registro(dni, nombre, ape1, ape2, email, contrasena)
        
        if error:
            self.__vista_registro.mostrarError(error)
            return # Cortamos aquí si hay error

        # 2. ENCRIPTACIÓN Y REGISTRO (Si todo está OK)
        contrasena_encriptada = self.__encriptar_contrasena(contrasena)
        registroVo = RegistroVo(nombre, ape1, ape2, email, dni, contrasena_encriptada)
        resultado = self.__modelo.hacerRegistro(registroVo)

        if resultado:
            self.__vista_registro.mostrarExito()
            self.volverAlLogin()
        else:
            self.__vista_registro.mostrarError("Error: No se pudo conectar con el servidor.")

    def __validar_datos_registro(self, dni, nombre, ape1, ape2, email, contra):
        """Devuelve un mensaje de error si algo falla, o None si todo está bien."""
        
        # Comprobar si hay campos vacíos
        if not all([dni, nombre, ape1, ape2, email, contra]):
            return "Todos los campos son obligatorios."
        
        # Validar DNI (Formato básico: 9 caracteres)
        if len(dni) != 9:
            return "El DNI/NIE debe tener 9 caracteres."
        
        # Validar Email (Uso de expresión regular)
        regex_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(regex_email, email):
            return "El formato del email no es válido."
        
        # Validar Contraseña (Mínimo 8 caracteres)
        if len(contra) < 8:
            return "La contraseña debe tener al menos 8 caracteres."
        
        return None # Todo correcto

    def cerrarSesion(self):
        self.__vista_principal.hide()
        self.__vista_login.show()
    
    def __encriptar_contrasena(self, contrasena):
        sha256 = hashlib.sha256()
        sha256.update(contrasena.encode('utf-8'))
        return sha256.hexdigest()
