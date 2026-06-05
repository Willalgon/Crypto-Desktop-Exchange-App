# src/Modelo/dao/OperacionDaoJDBC.py
# ─────────────────────────────────────────────────────────────────────────────
# DAO — CU6 / CU7 / CU8
# Patrón: igual que ActivosDaoJDBC.py, AdminUsuariosDaoJDBC.py, etc.
# Responsabilidad: SOLO hablar con la BD. Sin lógica de negocio.
# Usa Conexion.py exactamente igual que los otros DAOs del proyecto.
# ─────────────────────────────────────────────────────────────────────────────

from src.Modelo.conexion.Conexion import Conexion


class OperacionDaoJDBC:

    # ── CU6 + CU7 + CU8 ──────────────────────────────────────────────────────

    def realizar_operacion(self, operacionVO) -> dict:
        """
        Llama a sp_realizar_operacion, que internamente:
          · CU7: verifica saldo fiat (compra) o cantidad poseída (venta)
          · CU8: hace INSERT en OPERACIONES y UPDATE en CARTERAS/POSICIONES

        Retorna dict  {'exito': bool, 'mensaje': str}
        """
        conn   = None
        cursor = None
        try:
            conn   = Conexion.obtener_conexion()
            cursor = conn.cursor()
            cursor.callproc(
                "sp_realizar_operacion",
                [
                    operacionVO.id_usuario,
                    operacionVO.id_activo,
                    operacionVO.tipo,      # 'COMPRA' | 'VENTA'
                    operacionVO.cantidad,
                ]
            )
            conn.commit()
            return {
                "exito":   True,
                "mensaje": f"{operacionVO.tipo.capitalize()} ejecutada correctamente."
            }

        except Exception as e:
            # El SP lanza SIGNAL con textos como "Saldo fiat insuficiente…"
            # mysql.connector los propaga como excepción normal.
            mensaje = getattr(e, "msg", str(e))
            return {"exito": False, "mensaje": str(mensaje)}

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    # ── Datos para cargar la pantalla del Trader ──────────────────────────────

    def obtener_activos(self) -> list:
        """
        Lista de todos los activos disponibles en el mercado.
        Retorna lista de dicts:
          {id_activo, nombre, simbolo, precio_actual, descripcion_especial}
        """
        conn   = None
        cursor = None
        try:
            conn   = Conexion.obtener_conexion()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_activo, nombre, simbolo,
                       precio_actual, descripcion_especial
                FROM   ACTIVOS
                ORDER  BY nombre
            """)
            return cursor.fetchall()

        except Exception as e:
            print(f"[OperacionDao] Error al obtener activos: {e}")
            return []

        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def obtener_cartera(self, id_usuario: int) -> dict | None:
        """
        Estado de la cartera del trader usando la vista vw_estado_cartera.
        Retorna dict:
          {saldo_fiat, valor_activos, patrimonio_total, posiciones: [...]}
        O None si no existe cartera.
        """
        conn   = None
        cursor = None
        try:
            conn   = Conexion.obtener_conexion()
            cursor = conn.cursor(dictionary=True)

            # Resumen económico de la cartera
            cursor.execute("""
                SELECT liquidez_disponible AS saldo_fiat,
                       valor_activos,
                       patrimonio_total
                FROM   vw_estado_cartera
                WHERE  id_usuario = %s
            """, (id_usuario,))
            resumen = cursor.fetchone()
            if not resumen:
                return None

            # Posiciones abiertas con PNL
            cursor.execute("""
                SELECT simbolo, activo, cantidad,
                       precio_medio_compra, precio_actual,
                       pnl_ganancia_perdida_fiat, roi_porcentaje
                FROM   vw_rendimiento_posiciones
                WHERE  id_cartera = (
                    SELECT id_cartera
                    FROM   CARTERAS
                    WHERE  id_usuario = %s
                )
            """, (id_usuario,))
            resumen["posiciones"] = cursor.fetchall()
            return resumen

        except Exception as e:
            print(f"[OperacionDao] Error al obtener cartera: {e}")
            return None

        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def obtener_historial(self, id_usuario: int) -> list:
        """
        Historial de operaciones del trader (CU8/CU9).
        Retorna lista de dicts:
          {id_operacion, fecha_hora, operacion, simbolo,
           cantidad, precio_ejecucion, total_fiat}
        """
        conn   = None
        cursor = None
        try:
            conn   = Conexion.obtener_conexion()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT vo.id_operacion, vo.fecha_hora, vo.operacion,
                       vo.simbolo, vo.cantidad,
                       vo.precio_ejecucion, vo.total_fiat
                FROM   vw_historial_operaciones vo
                JOIN   CARTERAS c ON vo.id_cartera = c.id_cartera
                WHERE  c.id_usuario = %s
                ORDER  BY vo.fecha_hora DESC
                LIMIT  100
            """, (id_usuario,))
            return cursor.fetchall()

        except Exception as e:
            print(f"[OperacionDao] Error al obtener historial: {e}")
            return []

        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()