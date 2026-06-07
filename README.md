# CryptoLearning app
Compra y vende las criptomonedas disponibles!
El administrador de la app publicará eventos cuando menos te lo esperes y tu patrimonio variará! Suerte!

---

## Cómo ejecutar la aplicación

### 1. Requisitos previos
- Python 3.10 o superior
- MySQL Server activo
- Java JDK instalado (necesario para la conexión JDBC)

### 2. Importar la base de datos
Importa el fichero `DATABASE.sql` en tu servidor MySQL:
```bash
mysql -u root -p < DATABASE.sql
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la conexión
Abre el archivo `src/modelo/conexion/Conexion.py` y ajusta los datos de tu servidor:
```python
self.__url  = "jdbc:mysql://localhost:3306/CryptoLearning"
self.__user = "root"
self.__pwd  = "tu_contraseña"
```

### 5. Lanzar la aplicación
```bash
python main.py
```

---

## Usuarios de prueba

### Analista
| Campo | Valor |
|-------|-------|
| Email | analista@unileon.es |
| Contraseña | analista123 |

### Administrador
| Campo | Valor |
|-------|-------|
| Email | admin@unileon.es |
| Contraseña | admin123 |
