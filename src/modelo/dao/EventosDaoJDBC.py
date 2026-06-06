from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.EventoMercadoVO import EventoMercadoVO


_MULTIPLICADORES = {
    "Bull Market":     1.15,
    "Bear Market":     0.80,
    "Crisis Fiat":     1.20,
    "Guerra Mundial":  0.70,
    "Halving Bitcoin": 1.25,
    "Hack Exchange":   0.60,
}


class EventosDaoJDBC(Conexion):

    def lanzar_evento(self, evento_vo: EventoMercadoVO):
        if not evento_vo.es_valido():
            print("EventoMercadoVO inválido:", evento_vo)
            return False

        factor = _MULTIPLICADORES.get(evento_vo.nombre_evento, 1.0)
        cursor = self.getCursor()
        try:
            cursor.execute(
                "INSERT INTO EVENTOS_MERCADO (id_admin, nombre_evento, descripcion) VALUES (?, ?, ?)",
                (evento_vo.id_admin, evento_vo.nombre_evento, evento_vo.descripcion),
            )
            cursor.execute(
                "UPDATE ACTIVOS SET precio_actual = ROUND(precio_actual * ?, 8)",
                (factor,),
            )
            cursor.execute(
                "INSERT INTO HISTORIAL_PRECIOS (id_activo, precio) SELECT id_activo, precio_actual FROM ACTIVOS"
            )
            return True

        except Exception as e:
            print("Error en lanzar_evento:", e)
            try:
                self.conexion.rollback()
            except Exception:
                pass
            return False

        finally:
            self.closeConnection()

    def obtener_ultimo_evento(self):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT id_admin, nombre_evento, descripcion
                FROM EVENTOS_MERCADO
                ORDER BY fecha_ejecucion DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                return EventoMercadoVO(
                    id_admin=row[0],
                    nombre_evento=row[1],
                    descripcion=row[2] or "",
                )
            return None
        except Exception as e:
            print("Error en obtener_ultimo_evento:", e)
            return None
        finally:
            self.closeConnection()