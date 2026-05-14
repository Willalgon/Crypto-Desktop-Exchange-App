from src.modelo.conexion.Conexion import Conexion

class NoticiasDaoJDBC(Conexion):

    def insertarNoticia(self, noticiaVO, id_analista):  # ← recibe id_analista por parámetro
        SQL = """
            INSERT INTO NOTICIAS (id_analista, titulo, cuerpo, es_aviso)
            VALUES (?, ?, ?, ?)
        """
        try:
            conn = self.getConexion()
            cursor = conn.cursor()
            cursor.execute(SQL, [
                id_analista,           # ← viene del controlador
                noticiaVO.titulo,
                noticiaVO.cuerpo,
                1 if noticiaVO.es_aviso else 0
            ])
            conn.commit()
            return True
        except Exception as e:
            print(f"[NoticiasDaoJDBC] Error al insertar noticia: {e}")
            return False

    def obtenerNoticias(self):
        SQL = """
            SELECT DATE_FORMAT(fecha_publicacion, '%d/%m/%Y  %H:%i'), titulo, es_aviso
            FROM NOTICIAS
            ORDER BY fecha_publicacion DESC
        """
        try:
            conn = self.getConexion()
            cursor = conn.cursor()
            cursor.execute(SQL)
            return cursor.fetchall()
        except Exception as e:
            print(f"[NoticiasDaoJDBC] Error al obtener noticias: {e}")
            return []