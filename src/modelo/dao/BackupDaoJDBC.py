from src.modelo.conexion.Conexion import Conexion

class BackupDaoJDBC(Conexion):

    TABLAS = [
        "USUARIOS", "ACTIVOS", "CARTERAS", "POSICIONES",
        "OPERACIONES", "HISTORIAL_PRECIOS", "EVENTOS_MERCADO", "NOTICIAS"
    ]

    def hacer_backup(self):
        cursor = self.getCursor()
        lineas = []
        try:
            for tabla in self.TABLAS:
                cursor.execute(f"SELECT * FROM {tabla}")
                filas = cursor.fetchall()
                cols = [desc[0] for desc in cursor.description]
                lineas.append(f"-- TABLA: {tabla}")
                for fila in filas:
                    valores = ", ".join(
                        f"'{str(v).replace(chr(39), chr(39)+chr(39))}'" if v is not None else "NULL"
                        for v in fila
                    )
                    lineas.append(
                        f"INSERT INTO {tabla} ({', '.join(cols)}) VALUES ({valores});"
                    )
                lineas.append("")
            return "\n".join(lineas)
        except Exception as e:
            print("Error en hacer_backup:", e)
            return None
        finally:
            self.closeConnection()