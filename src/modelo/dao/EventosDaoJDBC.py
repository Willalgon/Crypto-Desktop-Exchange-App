from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.EventoMercadoVO import EventoMercadoVO


class EventosDaoJDBC(Conexion):

    def lanzar_evento(self, evento_vo: EventoMercadoVO):
        if not evento_vo.es_valido():
            print("EventoMercadoVO inválido:", evento_vo)
            return False

        cursor = self.getCursor()
        try:
            cursor.execute(
                "CALL sp_ejecutar_evento_mercado(?, ?, ?)",
                (evento_vo.id_admin, evento_vo.nombre_evento, evento_vo.descripcion)
            )
            return True

        except Exception as e:
            print("Error en lanzar_evento:", e)
            return False

        finally:
            self.closeConnection()

    def obtener_ultimo_evento(self):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT id_admin, nombre_evento, descripcion, fecha_ejecucion
                FROM EVENTOS_MERCADO
                ORDER BY fecha_ejecucion DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                vo = EventoMercadoVO(
                    id_admin=row[0],
                    nombre_evento=row[1],
                    descripcion=row[2] or "",
                )
                vo.fecha_ejecucion = row[3]
                return vo
            return None
        except Exception as e:
            print("Error en obtener_ultimo_evento:", e)
            return None
        finally:
            self.closeConnection()