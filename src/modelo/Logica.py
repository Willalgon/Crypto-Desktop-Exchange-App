from src.modelo.dao.LoginDaoJDBC import UsersDaoJDBC
from src.modelo.vo.UsuarioVO import UsuarioVO

class Logica:
    def __init__(self):
        self.__users_dao = UsersDaoJDBC()

    def hacerLogin(self, loginVO):
        return self.__users_dao.checkLogin(loginVO)

    def hacerRegistro(self, registroVO):
        try:
            self.__users_dao.insertar(registroVO)
            return True
        except Exception as e:
            print(f"Error en registro: {e}")
            return False

    def obtenerActivos(self):
        from src.modelo.dao.ActivosDaoJDBC import ActivosDaoJDBC
        return ActivosDaoJDBC().obtener_todos()