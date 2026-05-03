# modelo/dao/UsersDaoJDBC.py
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuarioVO import UsuarioVO

class UsersDaoJDBC:                        # <-- NO hereda de Conexion

    # Columnas reales de tu BD
    SQL_CHECK_LOGIN = """
        SELECT dni, nombre, apellidos, email, rol
        FROM USUARIOS
        WHERE email = %s AND password = %s AND activo = TRUE
    """
    SQL_SELECT_ALL = """
        SELECT dni, nombre, apellidos, email, rol
        FROM USUARIOS
        WHERE activo = TRUE
    """
    SQL_INSERT = """
        INSERT INTO USUARIOS (dni, nombre, apellidos, email, password, rol)
        VALUES (%s, %s, %s, %s, %s, 'TRADER')
    """
    # El trigger trg_crear_cartera_trader crea la cartera automáticamente

    # ── helper privado ──────────────────────
    def __fila_a_vo(self, fila):
        dni, nombre, apellidos, email, rol = fila
        # apellidos es un solo campo en tu BD, lo separamos para mantener
        # compatibilidad con tu VO (primer y segundo apellido)
        partes = apellidos.split(" ", 1) if apellidos else ["", ""]
        primer_ape  = partes[0]
        segundo_ape = partes[1] if len(partes) > 1 else ""
        return UsuarioVO(dni, nombre, primer_ape, segundo_ape, email, rol)

    # ── login ───────────────────────────────
    def checkLogin(self, loginVO):
        """
        Recibe LoginVO con email + contraseña ya encriptada en SHA-256.
        Devuelve UsuarioVO si las credenciales son válidas, None si no.
        """
        conexion = Conexion.obtener_conexion()
        cursor   = conexion.cursor()
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

    # ── select todos ────────────────────────
    def select(self):
        """Devuelve lista de UsuarioVO con todos los usuarios activos."""
        conexion = Conexion.obtener_conexion()
        cursor   = conexion.cursor()
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

    # ── insertar ────────────────────────────
    def insertarUsuario(self, registroVO):
        """
        Inserta un nuevo Trader. El rol se fija a 'TRADER' directamente
        en la SQL porque el registro solo es para alumnos.
        La contraseña ya llega encriptada en SHA-256 desde el controlador.
        """
        conexion = Conexion.obtener_conexion()
        cursor   = conexion.cursor()
        try:
            apellidos = f"{registroVO.primerapellido} {registroVO.segundoapellido}".strip()
            cursor.execute(self.SQL_INSERT, (
                registroVO.dni,
                registroVO.nombre,
                apellidos,
                registroVO.mail,
                registroVO.contrasena
            ))
            conexion.commit()
            return True
        except Exception as e:
            print("Error en insertarUsuario:", e)
            conexion.rollback()
            return False
        finally:
            cursor.close()