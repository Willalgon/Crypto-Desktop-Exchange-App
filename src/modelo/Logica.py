from src.modelo.dao.RegistroDaoJDBC      import RegistroDaoJDBC
from src.modelo.dao.LoginDaoJDBC         import LoginDaoJDBC
from src.modelo.dao.NoticiaDaoJDBC       import NoticiaDaoJDBC
from src.modelo.dao.AdminUsuariosDaoJDBC import AdminUsuariosDaoJDBC
from src.modelo.dao.ActivosDaoJDBC       import ActivosDaoJDBC
from src.modelo.dao.EventosDaoJDBC       import EventosDaoJDBC
from src.modelo.vo.EventoMercadoVO       import EventoMercadoVO
from src.modelo.dao.OperacionDaoJDBC import OperacionDaoJDBC


class Logica:
    def __init__(self):
        self.__registro_dao       = RegistroDaoJDBC()
        self.__login_dao          = LoginDaoJDBC()
        self.__noticia_dao        = NoticiaDaoJDBC()
        self.__admin_usuarios_dao = AdminUsuariosDaoJDBC()
        self.__activos_dao        = ActivosDaoJDBC()
        self.__eventos_dao        = EventosDaoJDBC()
        self.__operacion_dao = OperacionDaoJDBC()

    # Login/Registro
    def hacerLogin(self, loginVO):
        return self.__login_dao.checkLogin(loginVO)

    # Login/Registro
    def hacerRegistro(self, registroVO):
        return self.__registro_dao.insertarUsuario(registroVO)

    # Analista
    def publicarNoticia(self, noticiaVO, id_analista):
        return self.__noticia_dao.insertarNoticia(noticiaVO, id_analista)

    # Analista
    def obtenerNoticias(self):
        return self.__noticia_dao.obtenerNoticias()


    def obtener_usuarios_para_admin(self):
        return self.__admin_usuarios_dao.obtener_usuarios_admin()

    def desactivar_usuario(self, email):
        return self.__admin_usuarios_dao.desactivar_usuario(email)

    def actualizar_usuario(self, usuario_vo):
        return self.__admin_usuarios_dao.actualizar_usuario(usuario_vo)

    def obtener_activos_admin(self):
        return self.__activos_dao.obtener_activos_admin()

    def admin_retirar_activo(self, id_activo):
        return self.__activos_dao.retirar_activo(id_activo)

    def obtener_activos_mercado(self):
        return self.__activos_dao.obtener_activos_mercado()

    def obtener_historial_precios(self, id_activo):
        return self.__activos_dao.obtener_historial_precios(id_activo)

    def lanzar_evento_mercado(self, id_admin, nombre_evento, descripcion):
        evento_vo = EventoMercadoVO(
            id_admin=id_admin,
            nombre_evento=nombre_evento,
            descripcion=descripcion,
        )
        return EventosDaoJDBC().lanzar_evento(evento_vo)

    def realizar_operacion(self, operacionVO) -> dict:
        return self.__operacion_dao.realizar_operacion(operacionVO)

    def obtener_activos_para_trader(self) -> list:
        return self.__operacion_dao.obtener_activos()

    def obtener_historial_operaciones(self, id_usuario: int) -> list:
        return self.__operacion_dao.obtener_historial(id_usuario)

    def obtener_cartera(self, id_usuario: int):
        return self.__operacion_dao.obtener_cartera(id_usuario)

    def obtenerPosiciones(self, id_usuario: int) -> list:
        return self.__operacion_dao.obtener_posiciones(id_usuario)

    def obtenerTodasLasNoticias(self):
        return self.__noticia_dao.obtenerNoticias()

    def obtenerAvisoUrgente(self):
        return self.__operacion_dao.obtener_ultimo_aviso()

    def obtenerUltimoEvento(self):
        from src.modelo.dao.EventosDaoJDBC import EventosDaoJDBC
        return EventosDaoJDBC().obtener_ultimo_evento()

    def hacer_backup(self):
        from src.modelo.dao.BackupDaoJDBC import BackupDaoJDBC
        return BackupDaoJDBC().hacer_backup()