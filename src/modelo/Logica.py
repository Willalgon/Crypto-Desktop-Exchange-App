from src.modelo.dao.RegistroDaoJDBC import RegistroDaoJDBC
from src.modelo.dao.LoginDaoJDBC import LoginDaoJDBC
from src.modelo.vo.RegistroVO import RegistroVO

class Logica:
    def __init__(self):
        self.__registro_dao = RegistroDaoJDBC()
        self.__login_dao = LoginDaoJDBC()
        self.__noticia_dao = NoticiaDaoJDBC()


    def hacerLogin(self, loginVO):
        return self.__login_dao.checkLogin(loginVO)

    def hacerRegistro(self, registroVO):
        return self.__registro_dao.insertarUsuario(registroVO)

    def obtenerActivos(self):
        from src.modelo.dao.ActivosDaoJDBC import ActivosDaoJDBC
        return ActivosDaoJDBC().obtener_todos()

    def publicarNoticia(self, noticiaVO):
        return self.__noticia_dao.insertarNoticia(noticiaVO, id_analista)
