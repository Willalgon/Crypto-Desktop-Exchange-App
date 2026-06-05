from src.modelo.conexion.Conexion import Conexion
class TraderDaoJDBC (Conexion):
    def consultarEstadoCartera(self, id_usuario):
            SQL = """SELECT liquidez_disponible, valor_activos, patrimonio_total 
                    FROM vw_estado_cartera WHERE id_usuario = ?"""
            try:
                cursor = self.getCursor()
                cursor.execute(SQL, (id_usuario,))
                fila = cursor.fetchone()
                if fila:
                    from src.modelo.vo.CarteraVO import CarteraVO
                    return CarteraVO(fila[0], fila[1], fila[2])
                return None
            except Exception as e:
                print("Error al consultar cartera:", e)
                return None

    def consultarPosiciones(self, id_usuario):
        SQL = """SELECT simbolo, cantidad, precio_medio_compra, pnl_ganancia_perdida_fiat, roi_porcentaje 
                    FROM vw_rendimiento_posiciones 
                    WHERE id_cartera = (SELECT id_cartera FROM CARTERAS WHERE id_usuario = ?)"""
        try:
            cursor = self.getCursor()
            cursor.execute(SQL, (id_usuario,))
            filas = cursor.fetchall()
            from src.modelo.vo.PosicionVO import PosicionVO
            return [PosicionVO(f[0], f[1], f[2], f[3], f[4]) for f in filas]
        except Exception as e:
            print("Error al consultar posiciones:", e)
            return []
        
    def consultarNoticias(self):
        SQL = "SELECT fecha_publicacion, titulo, cuerpo, es_aviso FROM NOTICIAS ORDER BY fecha_publicacion DESC"
        try:
            cursor = self.getCursor()
            cursor.execute(SQL)
            filas = cursor.fetchall()
            return filas 
        except Exception as e:
            print("Error al consultar noticias:", e)
            return []
        
    def consultarUltimoAviso(self):
        SQL="SELECT titulo, cuerpo FROM NOTICIAS WHERE es_aviso=1 ORDER BY fecha_publicacion DESC LIMIT 1"
        try:
            cursor=self.getCursor()
            cursor.execute(SQL)
            fila=cursor.fechone()
            if fila:
                return AvisoVO(fila[0], fila[1])
            return None
        except Exception as e:
            return None
