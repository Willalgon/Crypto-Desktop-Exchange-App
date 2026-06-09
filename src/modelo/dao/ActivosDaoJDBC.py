from src.modelo.factory.VOFactory import VOFactory
from src.modelo.conexion.Conexion import Conexion

class ActivosDaoJDBC(Conexion):

    def obtener_todos(self):
        return self.obtener_activos_admin()

    def obtener_activos_admin(self):
        cursor = self.getCursor()
        activos = []
        try:
            cursor.execute(
                "SELECT id_activo, nombre, simbolo, precio_actual FROM ACTIVOS"
            )
            for row in cursor.fetchall():
                activos.append(VOFactory.crear_vo("activo",
                    id_activo     = row[0],
                    nombre        = row[1],
                    simbolo       = row[2],
                    precio_actual = row[3],
                ))
        except Exception as e:
            print("Error en obtener_activos_admin:", e)
        finally:
            self.closeConnection()
        return activos

    def obtener_activos_mercado(self):
        cursor = self.getCursor()
        activos = []
        try:
            cursor.execute("""
                SELECT id_activo, nombre, simbolo, precio_actual,
                       descripcion_especial, es_cripto
                FROM ACTIVOS
                ORDER BY nombre ASC
            """)
            for row in cursor.fetchall():
                activos.append(VOFactory.crear_vo("activo",
                    id_activo            = row[0],
                    nombre               = row[1],
                    simbolo              = row[2],
                    precio_actual        = row[3],
                    descripcion_especial = row[4],
                    es_cripto            = row[5],
                ))
        except Exception as e:
            print("Error en obtener_activos_mercado:", e)
        finally:
            self.closeConnection()
        return activos

    def retirar_activo(self, id_activo):
        cursor = self.getCursor()
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM POSICIONES WHERE id_activo = ? AND cantidad > 0",
                (id_activo,)
            )
            if cursor.fetchone()[0] > 0:
                return "operaciones_pendientes"
            cursor.execute("DELETE FROM ACTIVOS WHERE id_activo = ?", (id_activo,))
            return True
        except Exception as e:
            print("Error en retirar_activo:", e)
            return False
        finally:
            self.closeConnection()

    def obtener_historial_precios(self, id_activo):
        cursor = self.getCursor()
        historial = []
        try:
            cursor.execute("""
                SELECT precio, fecha_hora
                FROM HISTORIAL_PRECIOS
                WHERE id_activo = ?
                ORDER BY fecha_hora ASC
            """, (id_activo,))
            historial = [(float(row[0]), row[1]) for row in cursor.fetchall()]
        except Exception as e:
            print("Error en obtener_historial_precios:", e)
        finally:
            self.closeConnection()
        return historial
