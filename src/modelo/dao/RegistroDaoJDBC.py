from src.modelo.conexion.Conexion import Conexion

class RegistroDaoJDBC(Conexion):

    SQL_INSERT = """
        INSERT INTO USUARIOS (dni, nombre, apellidos, email, password, rol)
        VALUES (?, ?, ?, ?, ?, 'TRADER')
    """
    # El TRIGGER trg_crear_cartera_trader crea la cartera con 10.000€ automáticamente

    def insertarUsuario(self, registroVO):
        cursor = self.getCursor()
        try:
            apellidos = f"{registroVO.primerapellido} {registroVO.segundoapellido}".strip()
            cursor.execute(self.SQL_INSERT, (
                registroVO.dni,
                registroVO.nombre,
                apellidos,
                registroVO.mail,        # ← comprueba que RegistroVO tiene .mail
                registroVO.contrasena   # ← ya llega encriptada en SHA-256
            ))
            self.conexion.commit()
            return True
        except Exception as e:
            print("Error en insertarUsuario:", e)
            self.conexion.rollback()
            return False
        finally:
            cursor.close()