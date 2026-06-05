from src.modelo.dao.RegistroDaoJDBC import RegistroDaoJDBC
from src.modelo.dao.LoginDaoJDBC import LoginDaoJDBC
from src.modelo.dao.NoticiaDaoJDBC import NoticiaDaoJDBC
from src.modelo.dao.TraderDaoJDBC import TraderDaoJDBC
from src.modelo.dao.ActivoDaoJDBC import ActivoDaoJDBC

class Logica:
    def __init__(self):
        self.__registro_dao = RegistroDaoJDBC()
        self.__login_dao = LoginDaoJDBC()
        self.__noticia_dao = NoticiaDaoJDBC()
        self.__trader_dao = TraderDaoJDBC()
        self.__activo_dao=ActivoDaoJDBC()


    def hacerLogin(self, loginVO):
        return self.__login_dao.checkLogin(loginVO)

    def hacerRegistro(self, registroVO):
        return self.__registro_dao.insertarUsuario(registroVO)

    def obtenerActivos(self):
        from src.modelo.dao.ActivosDaoJDBC import ActivosDaoJDBC
        return ActivosDaoJDBC().obtener_todos()

    def publicarNoticia(self, noticiaVO, id_analista):
        return self.__noticia_dao.insertarNoticia(noticiaVO, id_analista)

    def obtenerEstadoPortfolio(self, id_usuario):
        return self.__trader_dao.consultarEstadoCartera(id_usuario)

    def obtenerPosiciones(self, id_usuario):
        return self.__trader_dao.consultarPosiciones(id_usuario)
    
    def obtenerTodasLasNoticias(self):
        return self.__trader_dao.consultarNoticias()
    
    def obtenerTodosLosActivos(self):
        return self.__activo_dao.consultarTodos()
    
    def obtenerAvisoUrgente(self):
        return self.__trader_dao.consultarUltimoAviso()