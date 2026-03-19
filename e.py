import pymssql

# 1. Configurar los datos de conexión
# Reemplaza 'localhost' por la IP de tu servidor de Azure si no lo corres en local
servidor = 'localhost' 
usuario = 'sa'
contrasena = '221322S@muel'
base_datos = 'CryptoTracker' # El nombre real de tu BD según el archivo SQL

try:
    # 2. Establecer la conexión
    conexion = pymssql.connect(
        server=servidor,
        user=usuario,
        password=contrasena,
        database=base_datos
    )
    print("¡Conexión exitosa a SQL Server!")

    # 3. Crear un cursor para ejecutar consultas
    cursor = conexion.cursor()

    # (Opcional) Probar una consulta rápida para ver si lee tus tablas
    cursor.execute("SELECT COUNT(*) FROM USUARIOS")
    resultado = cursor.fetchone()
    print(f"Número de usuarios en la base de datos: {resultado[0]}")

    # 4. Cerrar todo al terminar
    cursor.close()
    conexion.close()
    print("Conexión cerrada.")

except Exception as e:
    print("Ocurrió un error al conectar:", e)