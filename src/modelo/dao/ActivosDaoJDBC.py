from src.Modelo.conexion.Conexion import Conexion

class ActivosDaoJDBC(Conexion):
    def obtener_activos_admin(self):
        cursor = self.getCursor()
        activos = []
        try:
            cursor.execute("SELECT id_activo, nombre, simbolo, precio_actual, activo FROM ACTIVOS")
            rows = cursor.fetchall()
            for row in rows:
                activos.append(row)
        except Exception as e:
            print("Error en obtener_activos_admin:", e)
        finally:
            self.closeConnection()
        return activos

    def retirar_activo(self, id_activo):
        cursor = self.getCursor()
        try:
            cursor.execute("UPDATE ACTIVOS SET activo = 0 WHERE id_activo = ?", (id_activo,))
            self.conexion.commit()
            return True
        except Exception as e:
            print("Error en retirar_activo:", e)
            return False
        finally:
            self.closeConnection()