from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuarioVO import UsuarioVo
class UsersDaoJDBC(Conexion):
    SQL_SELECT = "SELECT dni, nombre, primer_apellido, segundo_apellido, email FROM Usuarios"
    SQL_INSERT="INSERT INTO Usuarios(dni,nombre,primer_apellido,segundo_apellido,email) VALUES (?, ?, ?, ?, ?)"
    SQL_CHECK_LOGIN="SELECT dni, nombre, primer_apellido, segundo_apellido, email FROM Usuarios WHERE nombre = ? AND Constraseña = ?"

    def checkLogin(self,loginVO):
        cursor=self.getCursor()
        try:
            cursor.execute(self.SQL_CHECK_LOGIN, (loginVO.nombre,loginVO.contrasena))
            row = cursor.fetchone()

            if row:
                dni,nombre,primer_apellido,segundo_apellido,email=row
                usuario=UsuarioVO(dni,nombre,primer_apellido,segundo_apellido,email)
                return usuario
            else:
                return None

        except Exception as e:
            print(e)

def select(self):
    cursor= self.getCursor()
    usuarios=[]
    try:
        cursor.execute(self.SQL_SELECT)
        rows=cursor.fetchall()

        for row in rows:
            dni,nombre,primer_apellido,segundo_apellido,email=row
            usuario=Usuario(dnu,nombre,primer_apellido,segundo_apellido,email)
            usuarios.append(usuario)

    except Exception as e:
        print(e)


    return usuario