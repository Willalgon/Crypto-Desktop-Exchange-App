from src.modelo.dao.UsersDaoJDBC import UsersDaoJDBC
class Logica:
    def pruebaSelect(self):
        user_dao=UsersDaoJDBC()
        users=user_dao.select()

        for usuario in users:
            print(usuario.dni)
    
    def hacerLogin(self,loginVO):
        login_dao=UsersDaoJDBC()
        resultado=login_dao.checkLogin(loginVO)
        
        return resultado

    def hacerRegistro(self,registroVo):
        registro_dao=UsersDaoJDBC()
        resultado=registro_dao.insertarUsuario(registroVo)
        
        return resultado