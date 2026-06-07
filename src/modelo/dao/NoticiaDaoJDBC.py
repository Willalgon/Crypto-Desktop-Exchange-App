from src.modelo.conexion.Conexion import Conexion

class NoticiaDaoJDBC(Conexion):

    def insertarNoticia(self, noticiaVO, id_analista):
        SQL = """
              INSERT INTO NOTICIAS (id_analista, titulo, cuerpo, es_aviso)
              VALUES (?, ?, ?, ?)
              """
        try:
            cursor = self.getCursor()
            cursor.execute(SQL, (
                id_analista,
                noticiaVO.titulo,
                noticiaVO.cuerpo,
                1 if noticiaVO.es_aviso else 0
            ))
            return True
        except Exception as e:
            print(f"[NoticiaDaoJDBC] Error al insertar noticia: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return False

    def obtenerNoticias(self):
        SQL = """
              SELECT DATE_FORMAT(fecha_publicacion, '%d/%m/%Y  %H:%i'), titulo, cuerpo, es_aviso
              FROM NOTICIAS
              ORDER BY fecha_publicacion DESC
              """
        try:
            cursor = self.getCursor()  # ← igual aquí
            cursor.execute(SQL)
            return cursor.fetchall()
        except Exception as e:
            print(f"[NoticiaDaoJDBC] Error al obtener noticias: {e}")
            return []