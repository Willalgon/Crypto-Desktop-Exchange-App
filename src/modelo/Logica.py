from src.Modelo.dao.RegistroDaoJDBC import RegistroDaoJDBC
from src.Modelo.dao.LoginDaoJDBC import LoginDaoJDBC
from src.Modelo.dao.NoticiaDaoJDBC import NoticiaDaoJDBC
from src.Modelo.dao.AdminUsuariosDaoJDBC import AdminUsuariosDaoJDBC
from src.Modelo.dao.ActivosDaoJDBC import ActivosDaoJDBC
from src.Modelo.dao.OperacionDaoJDBC import OperacionDaoJDBC

class Logica:
    def __init__(self):
        self.__registro_dao = RegistroDaoJDBC()
        self.__login_dao = LoginDaoJDBC()
        self.__noticia_dao = NoticiaDaoJDBC()
        self.__operacion_dao = OperacionDaoJDBC()


    def hacerLogin(self, loginVO):
        return self.__login_dao.checkLogin(loginVO)

    def hacerRegistro(self, registroVO):
        return self.__registro_dao.insertarUsuario(registroVO)

    def obtenerActivos(self):
        from src.Modelo.dao.ActivosDaoJDBC import ActivosDaoJDBC
        return ActivosDaoJDBC().obtener_todos()

    def publicarNoticia(self, noticiaVO, id_analista):
        return self.__noticia_dao.insertarNoticia(noticiaVO, id_analista)

    def obtenerNoticias(self):
        return self.__noticia_dao.obtenerNoticias()

    def obtener_usuarios_para_admin(self):
        dao = AdminUsuariosDaoJDBC()
        return dao.obtener_usuarios_admin()

    def desactivar_usuario(self, email):
        dao = AdminUsuariosDaoJDBC()
        return dao.desactivar_usuario(email)

    def obtener_activos_admin(self):
        return ActivosDaoJDBC().obtener_activos_admin()

    def admin_retirar_activo(self, id_activo):
        return ActivosDaoJDBC().retirar_activo(id_activo)

    def realizar_operacion(self, operacionVO) -> dict:
        """
        CU6 + CU7 + CU8.
        Delega en OperacionDaoJDBC, que llama al stored procedure.
        Retorna {'exito': bool, 'mensaje': str}
        """
        return self.__operacion_dao.realizar_operacion(operacionVO)

    def obtener_activos_para_trader(self) -> list:
        """CU4 / CU6 — lista de activos del mercado para la VentanaTrader."""
        return self.__operacion_dao.obtener_activos()

    def obtener_cartera_trader(self, id_usuario: int) -> dict | None:
        """CU9 — saldo, patrimonio y posiciones abiertas del trader."""
        return self.__operacion_dao.obtener_cartera(id_usuario)

    def obtener_historial_operaciones(self, id_usuario: int) -> list:
        """CU8 / CU9 — últimas 100 operaciones del trader."""
        return self.__operacion_dao.obtener_historial(id_usuario)
