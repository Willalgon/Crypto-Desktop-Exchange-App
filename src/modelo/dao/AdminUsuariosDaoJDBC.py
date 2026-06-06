from src.modelo.conexion.Conexion import Conexion
from src.modelo.factory.VOFactory import VOFactory

class AdminUsuariosDaoJDBC(Conexion):

    def obtener_usuarios_admin(self):
        cursor = self.getCursor()
        usuarios = []
        try:
            cursor.execute(
                "SELECT id_usuario, dni, nombre, apellidos, email, rol, activo "
                "FROM USUARIOS"
            )
            for row in cursor.fetchall():
                vo = VOFactory.crear_vo("usuario",
                    id_usuario=row[0],
                    dni=row[1],
                    nombre=row[2],
                    apellidos=row[3],
                    email=row[4],
                    rol=row[5],
                    activo=row[6],
                )
                usuarios.append(vo)
        except Exception as e:
            print("Error en obtener_usuarios_admin:", e)
        finally:
            self.closeConnection()
        return usuarios

    def desactivar_usuario(self, email):
        cursor = self.getCursor()
        try:
            # Obtenemos el rol del usuario a desactivar
            cursor.execute(
                "SELECT rol FROM USUARIOS WHERE email = ?", (email,)
            )
            fila = cursor.fetchone()
            if fila is None:
                return False

            # Si es ADMIN, comprobamos que no sea el último
            if fila[0] == "ADMIN":
                cursor.execute(
                    "SELECT COUNT(*) FROM USUARIOS WHERE rol = 'ADMIN' AND activo = 1"
                )
                total_admins = cursor.fetchone()[0]
                if total_admins <= 1:
                    return "ultimo_admin"

            cursor.execute(
                "UPDATE USUARIOS SET activo = 0 WHERE email = ?", (email,)
            )
            return True
        except Exception as e:
            print("Error en desactivar_usuario:", e)
            return False
        finally:
            self.closeConnection()

    def actualizar_usuario(self, usuario_vo):
        cursor = self.getCursor()
        try:
            cursor.execute(
                "UPDATE USUARIOS SET nombre = ?, apellidos = ?, rol = ? "
                "WHERE email = ?",
                (usuario_vo.nombre, usuario_vo.apellidos,
                 usuario_vo.rol, usuario_vo.email)
            )
            return True
        except Exception as e:
            print("Error en actualizar_usuario:", e)  # ← este es el que importa
            return False
        finally:
            self.closeConnection()