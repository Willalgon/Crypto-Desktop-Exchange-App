from src.Modelo.conexion.Conexion import Conexion
from src.Modelo.vo.UsersVo import UsuarioVo

class UserDaoJDBC(Conexion):
    SQL_SELECT = "SELECT dni, nombre, primer_apellido, segundo_apellido, email FROM usuarios"
    SQL_INSERT = "INSERT INTO(dni, nombre, primer_apellido, segundo_apellido, email) VALUES(?, ?, ?, ?)"
    def select(self):
        cursor = self.Cursor()
        usuarios = []

        try:   
            cursor.execute(self.SQL_SELECT)
            rows = cursor.fetchall()

            for row in rows:
                dni, nombre, primer_apellido, segundo_apellido, email = row
                usuario = UsuarioVo(dni, nombre, primer_apellido, segundo_apellido, email)
                usuarios.append(usuario)
        except Exception as e:
            print(e)
    
        return usuarios