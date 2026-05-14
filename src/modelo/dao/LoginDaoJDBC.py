from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.RegistroVO import RegistroVO

class LoginDaoJDBC(Conexion):

    SQL_CHECK_LOGIN = """
        SELECT dni, nombre, apellidos, email, rol
        FROM USUARIOS
        WHERE email = ? AND password = ? AND activo = TRUE
    """

    def __fila_a_vo(self, fila):
        dni, nombre, apellidos, email, rol = fila
        partes      = apellidos.split(" ", 1) if apellidos else ["", ""]
        primer_ape  = partes[0]
        segundo_ape = partes[1] if len(partes) > 1 else ""
        return RegistroVO(dni, nombre, primer_ape, segundo_ape, email, rol)

    def checkLogin(self, loginVO):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CHECK_LOGIN,
                           (loginVO.email, loginVO.contrasena))
            fila = cursor.fetchone()
            return self.__fila_a_vo(fila) if fila else None
        except Exception as e:
            print("Error en checkLogin:", e)
            return None
        finally:
            cursor.close()