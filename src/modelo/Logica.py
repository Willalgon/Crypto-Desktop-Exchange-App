from src.Modelo.dao.UserDaoJDBC import UserDaoJDBC
class Logica:
    def pruebaSelect(self):
        #aqui se hace el cliente
        user_dao = UserDaoJDBC()
        users = user_dao.select()

        for usuario in users:
            print(usuario.ui)