from src.modelo.conexion.Conexion import Conexion


class OperacionDaoJDBC(Conexion):

    def realizar_operacion(self, operacionVO) -> dict:
        cursor = self.getCursor()
        try:
            cursor.execute(
                "CALL sp_realizar_operacion(?, ?, ?, ?)",
                (
                    operacionVO.id_usuario,
                    operacionVO.id_activo,
                    operacionVO.tipo,
                    operacionVO.cantidad,
                )
            )
            self.conexion.commit()
            return {
                "exito":   True,
                "mensaje": f"{operacionVO.tipo.capitalize()} ejecutada correctamente."
            }
        except Exception as e:
            return {"exito": False, "mensaje": getattr(e, "msg", str(e))}
        finally:
            self.closeConnection()

    def obtener_activos(self) -> list:
        from src.modelo.vo.ActivoVO import ActivoVO
        cursor = self.getCursor()
        activos = []
        try:
            cursor.execute("""
                SELECT id_activo, nombre, simbolo,
                       precio_actual, descripcion_especial
                FROM ACTIVOS
                ORDER BY nombre
            """)
            for row in cursor.fetchall():
                activos.append(ActivoVO(
                    id_activo            = row[0],
                    nombre               = row[1],
                    simbolo              = row[2],
                    precio_actual        = row[3],
                    descripcion_especial = row[4],
                ))
        except Exception as e:
            print(f"[OperacionDao] Error al obtener activos: {e}")
        finally:
            self.closeConnection()
        return activos

    def obtener_cartera(self, id_usuario: int):
        from src.modelo.vo.CarteraVO import CarteraVO
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT liquidez_disponible, valor_activos, patrimonio_total
                FROM vw_estado_cartera
                WHERE id_usuario = ?
            """, (id_usuario,))
            row = cursor.fetchone()
            return CarteraVO(row[0], row[1], row[2]) if row else None
        except Exception as e:
            print(f"[OperacionDao] Error obtener_cartera: {e}")
            return None
        finally:
            self.closeConnection()

    def obtener_posiciones(self, id_usuario: int) -> list:
        from src.modelo.vo.PosicionVO import PosicionVO
        cursor = self.getCursor()
        posiciones = []
        try:
            cursor.execute("""
                SELECT simbolo, activo, cantidad,
                       precio_medio_compra, precio_actual,
                       pnl_ganancia_perdida_fiat, roi_porcentaje
                FROM vw_rendimiento_posiciones
                WHERE id_cartera = (
                    SELECT id_cartera FROM CARTERAS WHERE id_usuario = ?
                )
            """, (id_usuario,))
            for row in cursor.fetchall():
                posiciones.append(PosicionVO(
                    simbolo             = row[0],
                    activo              = row[1],
                    cantidad            = row[2],
                    precio_medio_compra = row[3],
                    precio_actual       = row[4],
                    pnl                 = row[5],
                    roi                 = row[6],
                ))
        except Exception as e:
            print(f"[OperacionDao] Error obtener_posiciones: {e}")
        finally:
            self.closeConnection()
        return posiciones

    def obtener_historial(self, id_usuario: int) -> list:
        cursor = self.getCursor()
        historial = []
        try:
            cursor.execute("""
                SELECT vo.id_operacion, vo.fecha_hora, vo.operacion,
                       vo.simbolo, vo.cantidad,
                       vo.precio_ejecucion, vo.total_fiat
                FROM vw_historial_operaciones vo
                JOIN CARTERAS c ON vo.id_cartera = c.id_cartera
                WHERE c.id_usuario = ?
                ORDER BY vo.fecha_hora DESC
                LIMIT 100
            """, (id_usuario,))
            for row in cursor.fetchall():
                historial.append({
                    "id_operacion":     row[0],
                    "fecha_hora":       row[1],
                    "operacion":        row[2],
                    "simbolo":          row[3],
                    "cantidad":         float(row[4]),
                    "precio_ejecucion": float(row[5]),
                    "total_fiat":       float(row[6]),
                })
        except Exception as e:
            print(f"[OperacionDao] Error al obtener historial: {e}")
        finally:
            self.closeConnection()
        return historial

    def obtener_ultimo_aviso(self):
        from src.modelo.vo.AvisoVO import AvisoVO
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT titulo, cuerpo FROM NOTICIAS
                WHERE es_aviso = TRUE
                ORDER BY fecha_publicacion DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            return AvisoVO(row[0], row[1]) if row else None
        except Exception as e:
            print(f"[OperacionDao] Error obtener_ultimo_aviso: {e}")
            return None
        finally:
            self.closeConnection()