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
            apellidos = f"{registroVO.primer_apellido} {registroVO.segundo_apellido}".strip()
            cursor.execute(self.SQL_INSERT, (
                registroVO.dni,
                registroVO.nombre,
                apellidos,
                registroVO.email,       # ← era .mail, correcto es .email
                registroVO.contrasena
            ))
            return True
        except Exception as e:
            print("Error en insertarUsuario:", e)
            try:
                self.conexion.rollback()
            except Exception:
                pass
            return False
        finally:
            cursor.close()
            self.closeConnection()