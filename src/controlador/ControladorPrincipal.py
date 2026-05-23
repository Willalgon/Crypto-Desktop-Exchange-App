# controlador/ControladorPrincipal.py
import hashlib
import re
from src.Modelo.vo.LoginVO  import LoginVO
from src.Modelo.vo.RegistroVO import RegistroVO
from src.Modelo.vo.NoticiaVO import NoticiaVO
from src.vista.Administrador import Administrador

class ControladorPrincipal:
    def __init__(self, ref_vista_login, ref_vista_registro, ref_modelo):
        self.__vista_login = ref_vista_login
        self.__vista_registro = ref_vista_registro
        self.__vista_principal = None
        self.__modelo = ref_modelo

    def abrirIniciarSesion(self):
        self.__vista_login.showMaximized()

    def comprobarLogin(self, email, passw):
        if not email or not passw:
            self.__vista_login.lanzaraviso("Por favor, rellena todos los campos.")
            return
        pass_encriptada = self.__encriptar_contrasena(passw)
        loginVO = LoginVO(email, pass_encriptada)
        resultado = self.__modelo.hacerLogin(loginVO)

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
        if rol == "ADMIN":
            self.__vista_principal = Administrador()
            self.__vista_principal.setControlador(self)
            self.actualizar_vista_admin()  # Carga los datos
            self.__vista_principal.showMaximized()

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
            self.__vista_principal.mostrarExitoPublicacion(titulo, cuerpo, es_aviso)  # ← añadir cuerpo
        else:
            self.__vista_principal.mostrar_error("No se pudo publicar la noticia.")

    def cargarHistorial(self):
        noticias = self.__modelo.obtenerNoticias()
        self.__vista_principal.cargarHistorial(noticias)

    def actualizar_vista_admin(self):
        usuarios = self.__modelo.obtener_usuarios_para_admin()
        self.__vista_principal.cargar_usuarios(usuarios)

        activos = self.__modelo.obtener_activos_admin()
        self.__vista_principal.cargar_activos(activos)

    def admin_desactivar_usuario(self, email):
        exito = self.__modelo.desactivar_usuario(email)
        if exito:
            self.actualizar_vista_admin()
        else:
            print("Error: No se pudo desactivar el usuario en la BD.")

    def admin_retirar_activo(self, id_activo):
        exito = self.__modelo.admin_retirar_activo(id_activo)
        if exito:
            self.actualizar_vista_admin()  # Recarga las tablas
        else:
            print("Error: No se pudo retirar el activo en la BD.")

    def admin_lanzar_evento(self, nombre_evento, descripcion):
        id_admin = 1

        exito = self.__modelo.lanzar_evento_mercado(id_admin, nombre_evento, descripcion)

        if exito:
            self.actualizar_vista_admin()
        else:
            print("Error crítico: El evento de mercado no pudo ejecutarse.")