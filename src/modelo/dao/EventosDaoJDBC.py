from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.EventoMercadoVO import EventoMercadoVO


class EventosDaoJDBC(Conexion):

    def lanzar_evento(self, evento_vo: EventoMercadoVO):
        if not evento_vo.es_valido():
            print("EventoMercadoVO inválido:", evento_vo)
            return False

        cursor = self.getCursor()
        try:
            cursor.callproc(
                "sp_ejecutar_evento_mercado",
                (evento_vo.id_admin,
                 evento_vo.nombre_evento,
                 evento_vo.descripcion)
            )
            return True
        except Exception as e:
            print("Error en lanzar_evento:", e)
            return False
        finally:
            self.closeConnection()
