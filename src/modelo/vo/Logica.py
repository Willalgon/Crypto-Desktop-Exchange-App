from src.modelo.dao.UsersDaoJDBC import Conexion
class Logica:
    def pruebaSelect(self):
        user_dao=UsersDaoJDBC()
        users=user_dao.select()

        for usuario in users:
            print(usuario.dni)
    
    def hacerLogin(self,loginVO):
        login_dao=UserDaoJDBC()
        resultado=login_dao.checkLogin(login_dao)
        
        return resultado