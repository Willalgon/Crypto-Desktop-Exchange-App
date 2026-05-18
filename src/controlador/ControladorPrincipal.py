# controlador/ControladorPrincipal.py
import hashlib
import re
from src.modelo.vo.LoginVO  import LoginVO
from src.modelo.vo.RegistroVO import RegistroVO
from src.modelo.vo.NoticiaVO import NoticiaVO

class ControladorPrincipal:
    def __init__(self, ref_vista_login, ref_vista_registro, ref_modelo):
        self.__vista_login = ref_vista_login
        self.__vista_registro = ref_vista_registro
        self.__vista_principal = None   # se asigna tras login según rol
        self.__modelo = ref_modelo

    def abrirIniciarSesion(self):
        self.__vista_login.showMaximized()

    def comprobarLogin(self, email, passw):
        if not email or not passw:
            self.__vista_login.lanzaraviso("Por favor, rellena todos los campos.")
            return
        pass_encriptada = self.__encriptar_contrasena(passw)
        loginVO = LoginVO(email, pass_encriptada)
        resultado = self.__modelo.hacerLogin(loginVO)  # devuelve UsuarioVO o None

        if resultado:
            self.__vista_login.hide()
            self.__redirigir_segun_rol(resultado)
        else:
            self.__vista_login.lanzar_aviso("Login incorrecto. Verifica tus credenciales.")

    def __redirigir_segun_rol(self, usuario):
        self.__usuario_actual = usuario
        rol = usuario.rol
        print(f"ROL RECIBIDO: '{rol}'")
        # if rol == "TRADER":
        #     from src.vista.VentanaTrader import VentanaTrader
        #     self.__vista_principal = VentanaTrader()
        # elif rol == "ADMIN":
        #     from src.vista.VentanaAdmin import VentanaAdmin
        #     self.__vista_principal = VentanaAdmin()

        if rol == "ANALISTA":
            from src.vista.Analista import Analista
            self.__vista_principal = Analista()

        self.__vista_principal.controlador = self
        self.__vista_principal.showMaximized()

    def abrirVentanaRegistro(self):
        self.__vista_login.hide()
        self.__vista_registro.showMaximized()

    def volverAlLogin(self):
        self.__vista_registro.hide()
        self.__vista_login.showMaximized()

    def procesarRegistro(self, dni, nombre, ape1, ape2, email, contrasena):
        error = self.__validar_datos_registro(dni, nombre, ape1, ape2, email, contrasena)
        if error:
            self.__vista_registro.mostrarError(error)
            return

        contrasena_encriptada = self.__encriptar_contrasena(contrasena)
        registroVO = RegistroVO(dni, nombre, ape1, ape2, email, contrasena_encriptada)
        resultado = self.__modelo.hacerRegistro(registroVO)

        if resultado:
            self.__vista_registro.mostrarExito()
            self.volverAlLogin()
        else:
            self.__vista_registro.mostrarError("Error: No se pudo conectar con el servidor.")

    def cerrarSesion(self):
        if self.__vista_principal:
            self.__vista_principal.hide()
        self.__vista_login.showMaximized()

    def __validar_datos_registro(self, dni, nombre, ape1, ape2, email, contra):
        if not all([dni, nombre, ape1, ape2, email, contra]):
            return "Todos los campos son obligatorios."
        if len(dni) != 9:
            return "El DNI/NIE debe tener 9 caracteres."
        if not re.search(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$', email):
            return "El formato del email no es válido."
        if len(contra) < 4:
            return "La contraseña debe tener al menos 4 caracteres."
        return None

    def __encriptar_contrasena(self, contrasena):
        sha256 = hashlib.sha256()
        sha256.update(contrasena.encode('utf-8'))
        return sha256.hexdigest()

    def publicarNoticia(self, titulo, cuerpo, es_aviso):
        noticiaVO = NoticiaVO(titulo, cuerpo, es_aviso)
        resultado = self.__modelo.publicarNoticia(noticiaVO, self.__usuario_actual.id_usuario)
        if resultado:
            self.__vista_principal.mostrarExitoPublicacion(titulo, es_aviso)
        else:
            self.__vista_principal.mostrar_error("No se pudo publicar la noticia.")

    def cargarHistorial(self):
        noticias = self.__modelo.obtenerNoticias()
        self.__vista_principal.cargarHistorial(noticias)