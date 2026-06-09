from src.modelo.factory.VOFactory import VOFactory
from src.modelo.conexion.Conexion import Conexion

class LoginDaoJDBC(Conexion):
    # variable de clase entonces hay que llamarlo con self.
    SQL_CHECK_LOGIN = """
        SELECT id_usuario, dni, nombre, apellidos, email, rol
        FROM USUARIOS
        WHERE email = ? AND password = ? AND activo = TRUE
    """

    def checkLogin(self, loginVO):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CHECK_LOGIN, (loginVO.email, loginVO.contrasena))
            fila = cursor.fetchone()
            if not fila:
                return None
            id_usuario, dni, nombre, apellidos, email, rol = fila
            return VOFactory.crear_vo("usuario",
                id_usuario = id_usuario,
                dni = dni,
                nombre = nombre,
                apellidos = apellidos,
                email = email,
                rol = rol,
            )
        except Exception as e:
            print("Error en checkLogin:", e)
            return None
        finally:
            cursor.close()
            self.closeConnection()
