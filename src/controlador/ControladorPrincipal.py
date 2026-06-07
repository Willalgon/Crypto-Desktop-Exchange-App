import hashlib
import re

from src.modelo.vo.LoginVO    import LoginVO
from src.modelo.vo.RegistroVO import RegistroVO
from src.modelo.vo.UsuarioVO  import UsuarioVO
from src.modelo.vo.NoticiaVO  import NoticiaVO


class ControladorPrincipal:
    def __init__(self, ref_vista_login, ref_vista_registro, ref_modelo):
        self.__vista_login     = ref_vista_login
        self.__vista_registro  = ref_vista_registro
        self.__vista_principal = None
        self.__modelo          = ref_modelo
        self.__usuario_actual  = None   # se asigna tras login exitoso

    # Login
    def abrirIniciarSesion(self):
        self.__vista_login.showMaximized()

    # Login
    def comprobarLogin(self, email, passw):
        if not email or not passw:
            self.__vista_login.lanzar_aviso("Por favor, rellena todos los campos.")
            return
        pass_encriptada = self.__encriptar_contrasena(passw)
        loginVO  = LoginVO(email, pass_encriptada)
        resultado = self.__modelo.hacerLogin(loginVO)
        if resultado:
            self.__vista_login.hide()
            self.__redirigir_segun_rol(resultado)
        else:
            self.__vista_login.lanzar_aviso("Login incorrecto. Verifica tus credenciales.")

    # Login, Registro
    def __encriptar_contrasena(self, contrasena):
        sha256 = hashlib.sha256()
        sha256.update(contrasena.encode('utf-8'))
        return sha256.hexdigest()

    # Login
    def __redirigir_segun_rol(self, usuario_vo):
        self.__usuario_actual = usuario_vo
        rol = usuario_vo.rol

        if rol == "ADMIN":
            from src.vista.Administrador import Administrador
            self.__vista_principal = Administrador()
            self.__vista_principal.controlador = self
            self.actualizar_vista_admin()
            self.__vista_principal.showMaximized()

        elif rol == "TRADER":
            from src.vista.Trader import Trader
            self.__vista_principal = Trader()
            self.__vista_principal.controlador = self
            self._cargar_vista_trader()
            self.__vista_principal.showMaximized()

        elif rol == "ANALISTA":
            from src.vista.Analista import Analista
            self.__vista_principal = Analista()
            self.__vista_principal.controlador = self
            self.__vista_principal.showMaximized()

    # Login / registro
    def abrirVentanaRegistro(self):
        self.__vista_login.hide()
        self.__vista_registro.showMaximized()

    # Registro
    def volverAlLogin(self):
        self.__vista_registro.hide()
        self.__vista_login.showMaximized()

    # Registro
    def procesarRegistro(self, dni, nombre, ape1, ape2, email, contrasena):
        error = self.__validar_datos_registro(dni, nombre, ape1, ape2, email, contrasena)
        if error:
            self.__vista_registro.mostrarError(error)
            return

        contrasena_encriptada = self.__encriptar_contrasena(contrasena)
        registroVO = RegistroVO(dni, nombre, ape1, ape2, email, contrasena_encriptada)
        resultado  = self.__modelo.hacerRegistro(registroVO)

        if resultado:
            self.__vista_registro.mostrarExito()
            self.volverAlLogin()
        else:
            self.__vista_registro.mostrarError("Error: No se pudo conectar con el servidor.")

    # Registro
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

    # Trader / Analista / Administrador
    def cerrarSesion(self):
        if self.__vista_principal:
            self.__vista_principal.hide()
        self.__vista_principal = None
        self.__usuario_actual  = None
        self.__vista_login.showMaximized()

    def actualizar_vista_admin(self):
        usuarios = self.__modelo.obtener_usuarios_para_admin()
        self.__vista_principal.cargar_usuarios(usuarios)
        activos  = self.__modelo.obtener_activos_admin()
        self.__vista_principal.cargar_activos(activos)

    def admin_desactivar_usuario(self, email):
        resultado = self.__modelo.desactivar_usuario(email)
        if resultado == "ultimo_admin":
            self.__vista_principal.mostrar_aviso_ultimo_admin()
        elif resultado:
            self.actualizar_vista_admin()
        else:
            self.__vista_principal.mostrar_error("No se pudo desactivar el usuario.")

    def admin_editar_usuario(self, usuario_vo: UsuarioVO):
        resultado = self.__modelo.actualizar_usuario(usuario_vo)
        if resultado:
            self.actualizar_vista_admin()
        else:
            self.__vista_principal.mostrar_error("No se pudo actualizar el usuario.")

    def admin_retirar_activo(self, id_activo):
        resultado = self.__modelo.admin_retirar_activo(id_activo)
        if resultado == "operaciones_pendientes":
            self.__vista_principal.mostrar_aviso_operaciones_pendientes()
        elif resultado:
            self.actualizar_vista_admin()
        else:
            self.__vista_principal.mostrar_error("No se pudo retirar el activo.")


    def admin_lanzar_evento(self, nombre_evento, descripcion):
        id_admin = self.__usuario_actual.id_usuario
        exito = self.__modelo.lanzar_evento_mercado(id_admin, nombre_evento, descripcion)
        if exito:
            self.actualizar_vista_admin()  # recarga activos con precios actualizados
        else:
            self.__vista_principal.mostrar_error("No se pudo lanzar el evento de mercado.")

    # Analista
    def publicarNoticia(self, titulo, cuerpo, es_aviso):
        noticiaVO = NoticiaVO(titulo, cuerpo, es_aviso)
        resultado = self.__modelo.publicarNoticia(noticiaVO, self.__usuario_actual.id_usuario)
        if resultado:
            self.__vista_principal.mostrarExitoPublicacion(titulo, cuerpo, es_aviso)
        else:
            self.__vista_principal.mostrar_error("No se pudo publicar la noticia.")

    # Analista
    def cargarHistorial(self):
        noticias = self.__modelo.obtenerNoticias()
        self.__vista_principal.cargarHistorial(noticias)

    def consultar_criptomonedas(self):
        try:
            activos = self.__modelo.obtener_activos_mercado()
            self.__vista_principal.cargar_mercado(activos)
        except Exception as e:
            print("Error en consultar las criptomonedas:", e)
            self.__vista_principal.mostrar_error("Error al cargar el mercado. Inténtelo de nuevo.")

    def ver_detalles_activo(self, id_activo, nombre, simbolo, descripcion):
        from src.vista.DetalleActivo import DetalleActivo
        historial = self.__modelo.obtener_historial_precios(id_activo)
        dialogo = DetalleActivo(nombre, simbolo, descripcion, historial)
        dialogo.exec_()

    def _cargar_vista_trader(self):
        nombre_completo = f"{self.__usuario_actual.nombre} {self.__usuario_actual.apellidos}"
        self.__vista_principal.actualizar_nombre(nombre_completo)
        self._refrescar_datos_trader()
        activos = self.__modelo.obtener_activos_para_trader()
        self.__vista_principal.cargar_mercado(activos)
        operaciones = self.__modelo.obtener_historial_operaciones(self.__usuario_actual.id_usuario)
        self.__vista_principal.cargar_historial(operaciones)

    def trader_realizar_operacion(self, id_activo: int, tipo: str, cantidad: float):
        from src.modelo.vo.OperacionVO import OperacionVO

        if cantidad <= 0:
            self.__vista_principal.mostrar_error("La cantidad debe ser mayor que cero.")
            return

        operacionVO = OperacionVO(
            id_usuario=self.__usuario_actual.id_usuario,
            id_activo=id_activo,
            tipo=tipo,
            cantidad=cantidad,
        )

        resultado = self.__modelo.realizar_operacion(operacionVO)

        if resultado["exito"]:
            self.__vista_principal.mostrar_exito_operacion(resultado["mensaje"])
            self._refrescar_datos_trader()
        else:
            self.__vista_principal.mostrar_error(resultado["mensaje"])

    def _refrescar_datos_trader(self):
        cartera = self.__modelo.obtener_cartera(self.__usuario_actual.id_usuario)
        if cartera:
            self.__vista_principal.actualizar_saldo(
                saldo_fiat=cartera.saldo_fiat,
                patrimonio_total=cartera.patrimonio_total,
            )
        operaciones = self.__modelo.obtener_historial_operaciones(self.__usuario_actual.id_usuario)
        self.__vista_principal.cargar_historial(operaciones)

    def solicitarEstadoCarteraTrader(self):
        id_u = self.__usuario_actual.id_usuario
        cartera = self.__modelo.obtener_cartera(id_u)
        posiciones = self.__modelo.obtenerPosiciones(id_u)
        self.__vista_principal.refrescar_cartera(cartera, posiciones)

    def solicitarNoticias(self):
        noticias = self.__modelo.obtenerTodasLasNoticias()
        if noticias:
            self.__vista_principal.refrescar_noticias(noticias)
        else:
            self.__vista_principal.mostrar_mensaje("Noticias", "No hay noticias recientes.")

    def solicitarMercado(self):
        activos = self.__modelo.obtener_activos_mercado()
        self.__vista_principal.refrescar_mercado(activos)  # ← typo corregido (__vista__principal)

    def solicitarAvisoUrgente(self):
        return self.__modelo.obtenerAvisoUrgente()

    def solicitarUltimoEvento(self):
        return self.__modelo.obtenerUltimoEvento()

    def cargar_historial_trader(self):
        operaciones = self.__modelo.obtener_historial_operaciones(
            self.__usuario_actual.id_usuario
        )
        self.__vista_principal.cargar_historial(operaciones)