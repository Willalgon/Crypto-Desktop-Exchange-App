from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.ActivoVO import ActivoVO

class ActivoDaoJDBC(Conexion):
    def consultarTodos(self):
        SQL = "SELECT simbolo, nombre, precio_actual, 'CRIPTOMONEDA' FROM ACTIVOS"
        try:
            cursor = self.getCursor()
            cursor.execute(SQL)
            filas = cursor.fetchall()
            # Convertimos cada fila en un ActivoVO
            return [ActivoVO(f[0], f[1], f[2], f[3]) for f in filas]
        except Exception as e:
            print("Error al consultar activos:", e)
            return []
        finally:
            cursor.close()