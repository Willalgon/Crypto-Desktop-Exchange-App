from src.Modelo.conexion.Conexion import Conexion

class AdminUsuariosDaoJDBC(Conexion):
    def obtener_usuarios_admin(self):
        cursor = self.getCursor()
        usuarios = []
        try:
            cursor.execute("SELECT id_usuario, dni, nombre, apellidos, email, rol, activo FROM USUARIOS")
            rows = cursor.fetchall()
            for row in rows:
                usuarios.append(row) # Guardamos la tupla entera
        except Exception as e:
            print("Error en obtener_usuarios_admin:", e)
        finally:
            self.closeConnection()
        return usuarios

    def desactivar_usuario(self, email):
        cursor = self.getCursor()
        try:
            cursor.execute("UPDATE USUARIOS SET activo = 0 WHERE email = ?", (email,))
            self.conexion.commit()
            return True
        except Exception as e:
            print("Error en desactivar_usuario:", e)
            return False
        finally:
            self.closeConnection()