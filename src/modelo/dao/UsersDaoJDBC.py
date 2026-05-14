# modelo/dao/UsersDaoJDBC.py
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuarioVO import UsuarioVO

class UsersDaoJDBC(Conexion):   # hereda → tiene self.getCursor() y self.conexion

    SQL_CHECK_LOGIN = """
        SELECT dni, nombre, apellidos, email, rol
        FROM USUARIOS
        WHERE email = ? AND password = ? AND activo = TRUE
    """
    SQL_SELECT_ALL = """
        SELECT dni, nombre, apellidos, email, rol
        FROM USUARIOS WHERE activo = TRUE
    """
    SQL_INSERT = """
        INSERT INTO USUARIOS (dni, nombre, apellidos, email, password, rol)
        VALUES (?, ?, ?, ?, ?, 'TRADER')
    """

    def __fila_a_vo(self, fila):
        dni, nombre, apellidos, email, rol = fila
        partes      = apellidos.split(" ", 1) if apellidos else ["", ""]
        primer_ape  = partes[0]
        segundo_ape = partes[1] if len(partes) > 1 else ""
        return UsuarioVO(dni, nombre, primer_ape, segundo_ape, email, rol)

    def checkLogin(self, loginVO):
        cursor = self.getCursor()       # <-- usa el de Conexion directamente
        try:
            cursor.execute(self.SQL_CHECK_LOGIN, (loginVO.email, loginVO.contrasena))
            fila = cursor.fetchone()
            return self.__fila_a_vo(fila) if fila else None
        except Exception as e:
            print("Error en checkLogin:", e)
            return None
        finally:
            cursor.close()

    def select(self):
        cursor   = self.getCursor()
        usuarios = []
        try:
            cursor.execute(self.SQL_SELECT_ALL)
            for fila in cursor.fetchall():
                usuarios.append(self.__fila_a_vo(fila))
        except Exception as e:
            print("Error en select:", e)
        finally:
            cursor.close()
        return usuarios

    def insertarUsuario(self, registroVO):
        cursor = self.getCursor()
        try:
            apellidos = f"{registroVO.primerapellido} {registroVO.segundoapellido}".strip()
            cursor.execute(self.SQL_INSERT, (
                registroVO.dni,
                registroVO.nombre,
                apellidos,
                registroVO.mail,
                registroVO.contrasena
            ))
            self.conexion.commit()
            return True
        except Exception as e:
            print("Error en insertarUsuario:", e)
            self.conexion.rollback()
            return False
        finally:
            cursor.close()