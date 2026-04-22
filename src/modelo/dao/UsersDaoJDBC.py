from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuarioVo import UsuarioVo
class UsersDaoJDBC(Conexion):
    SQL_SELECT = "SELECT dni, nombre, primer_apellido, segundo_apellido, email FROM Usuarios"
    SQL_INSERT="INSERT INTO Usuarios(dni,nombre,primer_apellido,segundo_apellido,email,contrasena) VALUES (?, ?, ?, ?, ?, ?)"
    SQL_CHECK_LOGIN="SELECT dni, nombre, primer_apellido, segundo_apellido, email FROM Usuarios WHERE nombre = ? AND Constraseña = ?"

    def checkLogin(self,loginVO):
        cursor=self.getCursor()
        try:
            cursor.execute(self.SQL_CHECK_LOGIN, (loginVO.nombre,loginVO.contrasena))
            row = cursor.fetchone()

            if row:
                dni,nombre,primer_apellido,segundo_apellido,email=row
                usuario=UsuarioVo(dni,nombre,primer_apellido,segundo_apellido,email)
                return usuario
            else:
                return None

        except Exception as e:
            print("Error en checkLogin:", e)
            return None

    def select(self):
        cursor= self.getCursor()
        usuarios=[]
        try:
            cursor.execute(self.SQL_SELECT)
            rows=cursor.fetchall()

            for row in rows:
                dni,nombre,primer_apellido,segundo_apellido,email=row
                usuario=UsuarioVo(dni,nombre,primer_apellido,segundo_apellido,email)
                usuarios.append(usuario)

        except Exception as e:
            print("Error en select:", e)


        return usuarios

    def insertarUsuario(self,registroVo):
        cursor=self.getCursor()
        try:
            datos_a_insertar=(registroVo.dni,registroVo.nombre,registroVo.primerapellido,registroVo.segundoapellido,registroVo.mail,registroVo.contrasena)
            cursor.execute(self.SQL_INSERT, datos_a_insertar)
            self.conexion.commit()
            return True

        except Exception as e:
            print("Error en insertatUsuario:", e)
            return False