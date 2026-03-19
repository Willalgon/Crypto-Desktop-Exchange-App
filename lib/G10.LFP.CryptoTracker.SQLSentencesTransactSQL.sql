
USE master;
GO

IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'CryptoTracker')
BEGIN
    CREATE DATABASE CryptoTracker;
END
GO

USE CryptoTracker;
GO


-- 1. PLANES
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'PLANES')
BEGIN
    CREATE TABLE PLANES (
        id_plan INT PRIMARY KEY IDENTITY(1,1),
        nombre_plan VARCHAR(100) NOT NULL,
        creditos_mensuales INT NOT NULL,
        precio_mensual DECIMAL(10,2) NOT NULL,
        descripcion VARCHAR(500) NULL,
        fecha_creacion DATETIME2 DEFAULT GETDATE(),
        activo BIT DEFAULT 1,
        CONSTRAINT CHK_PLANES_CREDITOS CHECK (creditos_mensuales > 0),
        CONSTRAINT CHK_PLANES_PRECIO CHECK (precio_mensual > 0)
    );
END
GO

-- 2. USUARIOS
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'USUARIOS')
BEGIN
    CREATE TABLE USUARIOS (
        id_usuario INT PRIMARY KEY IDENTITY(1,1),
        email VARCHAR(120) NOT NULL UNIQUE,
        nombre_completo VARCHAR(100) NOT NULL,
        pais VARCHAR(50) NOT NULL,
        idioma VARCHAR(10) NOT NULL,
        moneda_preferida VARCHAR(10) NOT NULL,
        experiencia VARCHAR(50),
        datos_email VARCHAR(120),
        datos_direccion VARCHAR(200),
        datos_telefono VARCHAR(20),
        dir_fiscal_pais VARCHAR(50),
        dir_fiscal_ciudad VARCHAR(50),
        fecha_registro DATETIME2 DEFAULT GETDATE(),
        activo BIT DEFAULT 1,
        id_plan INT NOT NULL,
        FOREIGN KEY (id_plan) REFERENCES PLANES(id_plan),
        CONSTRAINT CHK_USUARIOS_EMAIL CHECK (email LIKE '%@%.%'),
        CONSTRAINT CHK_USUARIOS_PAIS CHECK (pais <> ''),
        CONSTRAINT CHK_USUARIOS_EXPERIENCIA CHECK (experiencia IN ('Principiante', 'Intermedio', 'Avanzado', 'Experto'))
    );
END
GO

-- 3. CRIPTOMONEDAS
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CRIPTOMONEDAS')
BEGIN
    CREATE TABLE CRIPTOMONEDAS (
        id_crypto INT PRIMARY KEY IDENTITY(1,1),
        nombre VARCHAR(100) NOT NULL,
        slug VARCHAR(100) UNIQUE,
        simbolo CHAR(5) UNIQUE NOT NULL,
        fundacion_nombre VARCHAR(100),
        fundacion_ano INT,
        exchange VARCHAR(200),
        capitalizacion_mercado DECIMAL(18,2),
        suministro_total DECIMAL(18,8),
        suministro_circulante DECIMAL(18,8),
        precio_usd_actual DECIMAL(18,8),
        activa BIT DEFAULT 1,
        url_logo VARCHAR(300),
        CONSTRAINT CHK_CRYPTO_CAP_MARKET CHECK (capitalizacion_mercado >= 0),
        CONSTRAINT CHK_CRYPTO_SUMINISTRO_TOTAL CHECK (suministro_total > 0),
        CONSTRAINT CHK_CRYPTO_SUMINISTRO_CIRC CHECK (suministro_circulante >= 0 AND suministro_circulante <= suministro_total),
        CONSTRAINT CHK_CRYPTO_PRECIO CHECK (precio_usd_actual > 0)
    );
END
GO

-- 4. PRECIOS
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'PRECIOS')
BEGIN
    CREATE TABLE PRECIOS (
        id_precio INT PRIMARY KEY IDENTITY(1,1),
        id_crypto INT NOT NULL,
        precio_alto DECIMAL(18,8) NOT NULL,
        precio_bajo DECIMAL(18,8) NOT NULL,
        precio_cierre DECIMAL(18,8) NOT NULL,
        fecha_hora DATETIME2 DEFAULT GETDATE(),
        FOREIGN KEY (id_crypto) REFERENCES CRIPTOMONEDAS(id_crypto),
        CONSTRAINT CHK_PRECIOS_ALTO CHECK (precio_alto > 0),
        CONSTRAINT CHK_PRECIOS_BAJO CHECK (precio_bajo > 0),
        CONSTRAINT CHK_PRECIOS_CIERRE CHECK (precio_cierre > 0)
    );
END
GO

-- 5. PORTFOLIOS
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'PORTFOLIOS')
BEGIN
    CREATE TABLE PORTFOLIOS (
        id_portfolio INT PRIMARY KEY IDENTITY(1,1),
        id_usuario INT NOT NULL,
        nombre_portfolio VARCHAR(100) NOT NULL,
        privacidad BIT DEFAULT 1,
        moneda_base VARCHAR(10) NOT NULL,
        rendimiento DECIMAL(18,8) DEFAULT 0.0,
        valor_total DECIMAL(18,2) DEFAULT 0.0,
        volatilidad_promedio DECIMAL(5,2),
        fecha_creacion DATETIME2 DEFAULT GETDATE(),
        FOREIGN KEY (id_usuario) REFERENCES USUARIOS(id_usuario),
        CONSTRAINT CHK_PORTFOLIOS_RENDIMIENTO CHECK (rendimiento >= 0)
    );
END
GO

-- 6. POSICIONES
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'POSICIONES')
BEGIN
    CREATE TABLE POSICIONES (
        id_posicion INT PRIMARY KEY IDENTITY(1,1),
        id_portfolio INT NOT NULL,
        id_crypto INT NOT NULL,
        cantidad_total DECIMAL(18,8) NOT NULL,
        precio_media_compra DECIMAL(18,8) NOT NULL,
        valor_actual DECIMAL(18,2),
        FOREIGN KEY (id_portfolio) REFERENCES PORTFOLIOS(id_portfolio),
        FOREIGN KEY (id_crypto) REFERENCES CRIPTOMONEDAS(id_crypto),
        CONSTRAINT CHK_POSICIONES_CANTIDAD CHECK (cantidad_total > 0),
        CONSTRAINT CHK_POSICIONES_PRECIO CHECK (precio_media_compra > 0)
    );
END
GO

-- 7. TRANSACCIONES
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TRANSACCIONES')
BEGIN
    CREATE TABLE TRANSACCIONES (
        id_transaccion BIGINT PRIMARY KEY IDENTITY(1,1),
        tipo VARCHAR(20) NOT NULL,
        cantidad DECIMAL(18,8) NOT NULL,
        precio_unitario DECIMAL(18,8) NOT NULL,
        valor_total DECIMAL(18,2) NOT NULL,
        comision DECIMAL(18,8) DEFAULT 0.00000000,
        comision_usd DECIMAL(18,2),
        moneda_destino VARCHAR(10) DEFAULT 'USD',
        fecha_hora DATETIME2 DEFAULT GETDATE(),
        estado VARCHAR(20) NOT NULL,
        hash_blockchain VARCHAR(100),
        datos_origen_banco VARCHAR(100),
        datos_origen_pais VARCHAR(50),
        id_portfolio INT NOT NULL,
        FOREIGN KEY (id_portfolio) REFERENCES PORTFOLIOS(id_portfolio),
        CONSTRAINT CHK_TRANSACCIONES_CANTIDAD CHECK (cantidad > 0),
        CONSTRAINT CHK_TRANSACCIONES_PRECIO CHECK (precio_unitario > 0),
        CONSTRAINT CHK_TRANSACCIONES_VALOR CHECK (valor_total > 0),
        CONSTRAINT CHK_TRANSACCIONES_COMISION CHECK (comision >= 0),
        CONSTRAINT CHK_TRANSACCIONES_TIPO CHECK (tipo IN ('COMPRA', 'VENTA', 'TRANSFERENCIA', 'DEPOSITO', 'RETIRO')),
        CONSTRAINT CHK_TRANSACCIONES_ESTADO CHECK (estado IN ('CONFIRMADA', 'PENDIENTE', 'FALLIDA', 'REVERTIDA'))
    );
END
GO

-- 8. EMPLEADOS
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'EMPLEADOS')
BEGIN
    CREATE TABLE EMPLEADOS (
        id_empleado INT PRIMARY KEY IDENTITY(1,1),
        nombre VARCHAR(100) NOT NULL,
        email_corporativo VARCHAR(120) NOT NULL UNIQUE,
        fecha_contratacion DATE NOT NULL,
        satisfaccion_media DECIMAL(5,3),
        tipo_empleado VARCHAR(20) NOT NULL,
        CONSTRAINT CHK_EMPLEADOS_SATISFACCION CHECK (satisfaccion_media >= 0 AND satisfaccion_media <= 5),
        CONSTRAINT CHK_EMPLEADOS_TIPO CHECK (tipo_empleado IN ('TRADER', 'ANALISTA', 'TECNICO_SOPORTE'))
    );
END
GO

-- 9. TRADERS
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TRADERS')
BEGIN
    CREATE TABLE TRADERS (
        id_empleado INT PRIMARY KEY,
        score DECIMAL(5,2) NOT NULL,
        FOREIGN KEY (id_empleado) REFERENCES EMPLEADOS(id_empleado),
        CONSTRAINT CHK_TRADERS_SCORE CHECK (score >= 0 AND score <= 100)
    );
END
GO

-- 10. ANALISTAS
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ANALISTAS')
BEGIN
    CREATE TABLE ANALISTAS (
        id_empleado INT PRIMARY KEY,
        reporte VARCHAR(500),
        precision DECIMAL(5,3),
        FOREIGN KEY (id_empleado) REFERENCES EMPLEADOS(id_empleado),
        CONSTRAINT CHK_ANALISTAS_PRECISION CHECK (precision >= 0 AND precision <= 100)
    );
END
GO

-- 11. TECNICOS_SOPORTE
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TECNICOS_SOPORTE')
BEGIN
    CREATE TABLE TECNICOS_SOPORTE (
        id_empleado INT PRIMARY KEY,
        tickets_resueltos INT DEFAULT 0,
        incidentes INT DEFAULT 0,
        FOREIGN KEY (id_empleado) REFERENCES EMPLEADOS(id_empleado),
        CONSTRAINT CHK_TECNICO_TICKETS CHECK (tickets_resueltos >= 0),
        CONSTRAINT CHK_TECNICO_INCIDENTES CHECK (incidentes >= 0)
    );
END
GO

-- 12. CRIMP_EMP
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CRIMP_EMP')
BEGIN
    CREATE TABLE CRIMP_EMP (
        id_empleado INT NOT NULL,
        id_crypto INT NOT NULL,
        especializacion VARCHAR(100),
        PRIMARY KEY (id_empleado, id_crypto),
        FOREIGN KEY (id_empleado) REFERENCES EMPLEADOS(id_empleado),
        FOREIGN KEY (id_crypto) REFERENCES CRIPTOMONEDAS(id_crypto)
    );
END
GO

-- 13. TAG_CATEGORIA
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TAG_CATEGORIA')
BEGIN
    CREATE TABLE TAG_CATEGORIA (
        id_crypto INT NOT NULL,
        tag_categoria VARCHAR(100) NOT NULL,
        PRIMARY KEY (id_crypto, tag_categoria),
        FOREIGN KEY (id_crypto) REFERENCES CRIPTOMONEDAS(id_crypto)
    );
END
GO

-- 14. ALERTAS
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ALERTAS')
BEGIN
    CREATE TABLE ALERTAS (
        id_alerta INT PRIMARY KEY IDENTITY(1,1),
        valor_objetivo DECIMAL(18,8) NOT NULL,
        condicion VARCHAR(20) NOT NULL,
        activa BIT DEFAULT 1,
        sensibilidad DECIMAL(5,2),
        horarios_inicio TIME,
        horarios_fin TIME,
        id_crypto INT NOT NULL,
        id_portfolio INT NOT NULL,
        id_usuario INT NOT NULL,
        FOREIGN KEY (id_crypto) REFERENCES CRIPTOMONEDAS(id_crypto),
        FOREIGN KEY (id_portfolio) REFERENCES PORTFOLIOS(id_portfolio),
        FOREIGN KEY (id_usuario) REFERENCES USUARIOS(id_usuario),
        CONSTRAINT CHK_ALERTAS_VALOR CHECK (valor_objetivo > 0),
        CONSTRAINT CHK_ALERTAS_CONDICION CHECK (condicion IN ('MAYOR_QUE', 'MENOR_QUE', 'IGUAL', 'RANGO')),
        CONSTRAINT CHK_ALERTAS_SENSIBILIDAD CHECK (sensibilidad >= 0 AND sensibilidad <= 100)
    );
END
GO

-- 15. PALABRAS_CLAVE
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'PALABRAS_CLAVE')
BEGIN
    CREATE TABLE PALABRAS_CLAVE (
        id_alerta INT NOT NULL,
        palabra_clave VARCHAR(100) NOT NULL,
        PRIMARY KEY (id_alerta, palabra_clave),
        FOREIGN KEY (id_alerta) REFERENCES ALERTAS(id_alerta)
    );
END
GO

-- 16. METRICAS_USUARIOS
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'METRICAS_USUARIOS')
BEGIN
    CREATE TABLE METRICAS_USUARIOS (
        id_metrica INT PRIMARY KEY IDENTITY(1,1),
        id_usuario INT NOT NULL,
        hora DATETIME2 DEFAULT GETDATE(),
        pnl DECIMAL(18,2),
        valor_portfolio DECIMAL(18,2),
        sesiones INT DEFAULT 0,
        FOREIGN KEY (id_usuario) REFERENCES USUARIOS(id_usuario),
        CONSTRAINT CHK_METRICAS_SESIONES CHECK (sesiones >= 0)
    );
END
GO

-- 17. NOTIFICACIONES
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'NOTIFICACIONES')
BEGIN
    CREATE TABLE NOTIFICACIONES (
        id_notificacion INT PRIMARY KEY IDENTITY(1,1),
        id_usuario INT NOT NULL,
        mensaje VARCHAR(500) NOT NULL,
        fecha_hora DATETIME2 DEFAULT GETDATE(),
        leida BIT DEFAULT 0,
        FOREIGN KEY (id_usuario) REFERENCES USUARIOS(id_usuario)
    );
END
GO

-- 18. TICKETS_SOPORTE
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TICKETS_SOPORTE')
BEGIN
    CREATE TABLE TICKETS_SOPORTE (
        id_ticket INT PRIMARY KEY IDENTITY(1,1),
        asunto VARCHAR(200) NOT NULL,
        descripcion VARCHAR(1000) NOT NULL,
        estado VARCHAR(20) DEFAULT 'ABIERTO',
        prioridad VARCHAR(20) NOT NULL,
        tiempo_resolucion INT,
        fecha_creacion DATETIME2 DEFAULT GETDATE(),
        id_empleado INT,
        id_usuario INT NOT NULL,
        FOREIGN KEY (id_empleado) REFERENCES EMPLEADOS(id_empleado),
        FOREIGN KEY (id_usuario) REFERENCES USUARIOS(id_usuario),
        CONSTRAINT CHK_TICKETS_ESTADO CHECK (estado IN ('ABIERTO', 'EN_PROGRESO', 'RESUELTO', 'CERRADO')),
        CONSTRAINT CHK_TICKETS_PRIORIDAD CHECK (prioridad IN ('BAJA', 'MEDIA', 'ALTA', 'CRITICA')),
        CONSTRAINT CHK_TICKETS_TIEMPO CHECK (tiempo_resolucion >= 0)
    );
END
GO

GO

-- TRIGGERS

-- TRIGGER 1: Actualizar METRICAS_USUARIOS
IF OBJECT_ID('TR_ACTUALIZAR_METRICAS_TRANSACCIONES', 'TR') IS NOT NULL
    DROP TRIGGER TR_ACTUALIZAR_METRICAS_TRANSACCIONES;
GO

CREATE TRIGGER TR_ACTUALIZAR_METRICAS_TRANSACCIONES
ON TRANSACCIONES
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @valor_transaccion DECIMAL(18,2);
    DECLARE @tipo_transaccion VARCHAR(20);
    DECLARE @id_portfolio INT;
    DECLARE @id_usuario INT;
    DECLARE @pnl_delta DECIMAL(18,2);
    
    SELECT 
        @valor_transaccion = i.valor_total,
        @tipo_transaccion = i.tipo,
        @id_portfolio = i.id_portfolio
    FROM inserted i;
    
    SELECT @id_usuario = id_usuario FROM PORTFOLIOS WHERE id_portfolio = @id_portfolio;
    
    SET @pnl_delta = 
        CASE 
            WHEN @tipo_transaccion = 'VENTA' THEN @valor_transaccion * 0.02
            WHEN @tipo_transaccion = 'COMPRA' THEN -(@valor_transaccion * 0.015)
            ELSE 0
        END;
    
    IF @id_usuario IS NOT NULL
    BEGIN
        UPDATE METRICAS_USUARIOS
        SET pnl = ISNULL(pnl, 0) + @pnl_delta,
            valor_portfolio = ISNULL(valor_portfolio, 0) + @pnl_delta,
            sesiones = ISNULL(sesiones, 0) + 1
        WHERE id_usuario = @id_usuario
            AND CAST(hora AS DATE) = CAST(GETDATE() AS DATE);
        
        IF @@ROWCOUNT = 0
        BEGIN
            INSERT INTO METRICAS_USUARIOS (id_usuario, hora, pnl, valor_portfolio, sesiones)
            VALUES (@id_usuario, GETDATE(), @pnl_delta, @pnl_delta, 1);
        END;
        
        PRINT 'TRIGGER 1: Métrica actualizada para usuario ' + CAST(@id_usuario AS VARCHAR(10));
    END
    ELSE
    BEGIN
        PRINT 'TRIGGER 1: No se encontró usuario asociado al portfolio ' + CAST(@id_portfolio AS VARCHAR(10));
    END;
END;
GO


-- TRIGGER 2: Actualizar precio en CRIPTOMONEDAS
IF OBJECT_ID('TR_ACTUALIZAR_PRECIO_CRYPTO', 'TR') IS NOT NULL
    DROP TRIGGER TR_ACTUALIZAR_PRECIO_CRYPTO;
GO

CREATE TRIGGER TR_ACTUALIZAR_PRECIO_CRYPTO
ON PRECIOS
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @id_crypto INT;
    DECLARE @precio_nuevo DECIMAL(18,8);
    
    SELECT 
        @id_crypto = i.id_crypto,
        @precio_nuevo = i.precio_cierre
    FROM inserted i;
    
    UPDATE CRIPTOMONEDAS
    SET precio_usd_actual = @precio_nuevo
    WHERE id_crypto = @id_crypto;
    
    PRINT 'TRIGGER 2: Precio sincronizado para crypto ' + CAST(@id_crypto AS VARCHAR(10));
END;
GO

-- TRIGGER 3: Proteger transacciones confirmadas
IF OBJECT_ID('TR_PROTEGER_TRANSACCIONES_CONFIRMADAS', 'TR') IS NOT NULL
    DROP TRIGGER TR_PROTEGER_TRANSACCIONES_CONFIRMADAS;
GO

CREATE TRIGGER TR_PROTEGER_TRANSACCIONES_CONFIRMADAS
ON TRANSACCIONES
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    IF EXISTS (
        SELECT 1
        FROM deleted d
        WHERE d.estado = 'CONFIRMADA'
    )
    BEGIN
        RAISERROR('ERROR: No se pueden modificar transacciones CONFIRMADAS', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END;
    
    PRINT 'TRIGGER 3: Transacción protegida';
END;
GO

-- TRIGGER 4: Sincronizar valores de PORTFOLIOS
IF OBJECT_ID('TR_SINCRONIZAR_PORTFOLIO_VALORES', 'TR') IS NOT NULL
    DROP TRIGGER TR_SINCRONIZAR_PORTFOLIO_VALORES;
GO

CREATE TRIGGER TR_SINCRONIZAR_PORTFOLIO_VALORES
ON POSICIONES
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @id_portfolio INT;
    DECLARE @valor_total DECIMAL(18,2);
    
    SELECT @id_portfolio = ISNULL(i.id_portfolio, d.id_portfolio)
    FROM inserted i
    FULL OUTER JOIN deleted d ON i.id_portfolio = d.id_portfolio;
    
    IF @id_portfolio IS NOT NULL
    BEGIN
        SELECT @valor_total = ISNULL(SUM(valor_actual), 0)
        FROM POSICIONES
        WHERE id_portfolio = @id_portfolio;
        
        UPDATE PORTFOLIOS
        SET valor_total = @valor_total
        WHERE id_portfolio = @id_portfolio;
        
        PRINT 'TRIGGER 4: Portfolio ' + CAST(@id_portfolio AS VARCHAR(10)) + ' sincronizado';
    END;
END;
GO

GO

-- LIMPIAR DATOS ANTERIORES

DELETE FROM PALABRAS_CLAVE;
DELETE FROM TAG_CATEGORIA;
DELETE FROM ALERTAS;
DELETE FROM METRICAS_USUARIOS;
DELETE FROM NOTIFICACIONES;
DELETE FROM POSICIONES;
DELETE FROM TICKETS_SOPORTE;
DELETE FROM TECNICOS_SOPORTE;
DELETE FROM ANALISTAS;
DELETE FROM TRADERS;
DELETE FROM CRIMP_EMP;
DELETE FROM TRANSACCIONES;
DELETE FROM PRECIOS;
DELETE FROM PORTFOLIOS;
DELETE FROM EMPLEADOS;
DELETE FROM CRIPTOMONEDAS;
DELETE FROM USUARIOS;
DELETE FROM PLANES;
GO

-- RESETEAR IDENTIDADES
DBCC CHECKIDENT ('PLANES', RESEED, 0);
DBCC CHECKIDENT ('CRIPTOMONEDAS', RESEED, 0);
DBCC CHECKIDENT ('EMPLEADOS', RESEED, 0);
DBCC CHECKIDENT ('USUARIOS', RESEED, 0);
DBCC CHECKIDENT ('PRECIOS', RESEED, 0);
DBCC CHECKIDENT ('PORTFOLIOS', RESEED, 0);
DBCC CHECKIDENT ('POSICIONES', RESEED, 0);
DBCC CHECKIDENT ('TRANSACCIONES', RESEED, 0);
DBCC CHECKIDENT ('ALERTAS', RESEED, 0);
DBCC CHECKIDENT ('METRICAS_USUARIOS', RESEED, 0);
DBCC CHECKIDENT ('NOTIFICACIONES', RESEED, 0);
DBCC CHECKIDENT ('TICKETS_SOPORTE', RESEED, 0);
GO

-- INSERTAR DATOS

-- 1. PLANES 
INSERT INTO PLANES (nombre_plan, creditos_mensuales, precio_mensual, descripcion, activo)
VALUES 
    ('Plan Basico', 100, 9.99, 'Plan básico para usuarios nuevos', 1),
    ('Plan Profesional', 500, 29.99, 'Plan profesional con más funcionalidades', 1),
    ('Plan Premium', 2000, 99.99, 'Plan premium con acceso total', 1);
GO

-- 2. CRIPTOMONEDAS 
INSERT INTO CRIPTOMONEDAS (nombre, slug, simbolo, fundacion_nombre, fundacion_ano, exchange, capitalizacion_mercado, suministro_total, suministro_circulante, precio_usd_actual, activa, url_logo)
VALUES 
    ('Bitcoin', 'bitcoin', 'BTC', 'Satoshi Nakamoto', 2009, 'Binance', 500000000000.00, 21000000.00000000, 20000000.50000000, 48000.00000000, 1, 'https://example.com/btc.png'),
    ('Ethereum', 'ethereum', 'ETH', 'Vitalik Buterin', 2015, 'Coinbase', 250000000000.00, 120000000.00000000, 115000000.00000000, 2400.00000000, 1, 'https://example.com/eth.png');
GO

-- 3. EMPLEADOS 
INSERT INTO EMPLEADOS (nombre, email_corporativo, fecha_contratacion, satisfaccion_media, tipo_empleado)
VALUES 
    ('Carlos Martínez', 'carlos.martinez@cryptotracker.es', '2023-01-15', 4.5, 'TRADER'),
    ('Ana García', 'ana.garcia@cryptotracker.es', '2023-06-20', 4.8, 'ANALISTA'),
    ('Luis Pérez', 'luis.perez@cryptotracker.es', '2024-01-10', 4.2, 'TECNICO_SOPORTE');
GO

-- 4. USUARIOS 
INSERT INTO USUARIOS (email, nombre_completo, pais, idioma, moneda_preferida, experiencia, datos_email, datos_direccion, datos_telefono, dir_fiscal_pais, dir_fiscal_ciudad, fecha_registro, activo, id_plan)
VALUES 
    ('juan.rodriguez@gmail.com', 'Juan Rodríguez García', 'España', 'es', 'EUR', 'Intermedio', 'juan@personal.com', 'Calle Principal 123', '+34 912 345 678', 'España', 'Madrid', GETDATE(), 1, 1),
    ('maria.lopez@outlook.es', 'María López Martínez', 'México', 'es', 'MXN', 'Principiante', 'maria@personal.com', 'Avenida Central 456', '+52 555 123 456', 'México', 'México DF', GETDATE(), 1, 2),
    ('david.sanchez@hotmail.com', 'David Sánchez Pérez', 'Argentina', 'es', 'ARS', 'Avanzado', 'david@personal.com', 'Carrera Principal 789', '+54 911 234 567', 'Argentina', 'Buenos Aires', GETDATE(), 1, 3);
GO

-- 5. PRECIOS 
INSERT INTO PRECIOS (id_crypto, precio_alto, precio_bajo, precio_cierre, fecha_hora)
VALUES 
    (1, 50000.00000000, 45000.00000000, 48000.00000000, GETDATE()),
    (2, 2500.00000000, 2200.00000000, 2400.00000000, GETDATE());
GO

-- 6. TAG_CATEGORIA
INSERT INTO TAG_CATEGORIA (id_crypto, tag_categoria)
VALUES 
    (1, 'Layer1'),
    (1, 'P2P'),
    (1, 'PoW'),
    (2, 'Layer1'),
    (2, 'SmartContracts'),
    (2, 'PoS');
GO

-- 7. TRADERS 
INSERT INTO TRADERS (id_empleado, score)
VALUES (1, 85.50);
GO

-- 8. ANALISTAS 
INSERT INTO ANALISTAS (id_empleado, reporte, precision)
VALUES (2, 'Análisis técnico especializado en cryptomonedas', 92.30);
GO

-- 9. TECNICOS_SOPORTE (FK a EMPLEADOS ✓ ya existen)
INSERT INTO TECNICOS_SOPORTE (id_empleado, tickets_resueltos, incidentes)
VALUES (3, 125, 8);
PRINT '✓ TECNICOS_SOPORTE insertados (1 fila)';
GO

-- 10. CRIMP_EMP 
INSERT INTO CRIMP_EMP (id_empleado, id_crypto, especializacion)
VALUES 
    (1, 1, 'Trading de Bitcoin'),
    (1, 2, 'Arbitrage'),
    (2, 1, 'Análisis de volatilidad'),
    (2, 2, 'Predictive Analytics');
GO

-- 11. PORTFOLIOS 
INSERT INTO PORTFOLIOS (id_usuario, nombre_portfolio, privacidad, moneda_base, rendimiento, valor_total, volatilidad_promedio, fecha_creacion)
VALUES 
    (1, 'Portfolio Principal', 1, 'EUR', 15.50, 50000.00, 2.30, GETDATE()),
    (2, 'Trading Corto Plazo', 0, 'MXN', 8.25, 25000.00, 5.60, GETDATE()),
    (3, 'Inversión Largo Plazo', 1, 'ARS', 22.75, 75000.00, 1.80, GETDATE());
GO

-- 12. METRICAS_USUARIOS
INSERT INTO METRICAS_USUARIOS (id_usuario, hora, pnl, valor_portfolio, sesiones)
VALUES 
    (1, GETDATE(), 1500.00, 51500.00, 45),
    (1, DATEADD(HOUR, -1, GETDATE()), 1200.00, 51200.00, 44),
    (2, GETDATE(), 800.00, 25800.00, 32),
    (2, DATEADD(HOUR, -1, GETDATE()), 500.00, 25500.00, 31),
    (3, GETDATE(), 3000.00, 78000.00, 65),
    (3, DATEADD(HOUR, -1, GETDATE()), 2500.00, 77500.00, 64);
GO

-- 13. NOTIFICACIONES 
INSERT INTO NOTIFICACIONES (id_usuario, mensaje, fecha_hora, leida)
VALUES 
    (1, 'Tu alerta de Bitcoin ha sido activada', GETDATE(), 0),
    (1, 'Transacción confirmada: Compra de 0.5 BTC', DATEADD(HOUR, -2, GETDATE()), 1),
    (2, 'Nuevo reporte técnico disponible', DATEADD(HOUR, -3, GETDATE()), 1),
    (3, 'Tu portafolio alcanzó valor máximo', DATEADD(HOUR, -4, GETDATE()), 0),
    (3, 'Oportunidad de arbitrage detectada', GETDATE(), 0);
GO

-- 14. POSICIONES 
INSERT INTO POSICIONES (id_portfolio, id_crypto, cantidad_total, precio_media_compra, valor_actual)
VALUES 
    (1, 1, 0.50000000, 40000.00000000, 24000.00),
    (1, 2, 5.00000000, 2000.00000000, 12000.00),
    (2, 1, 0.25000000, 45000.00000000, 12000.00),
    (2, 2, 10.00000000, 2200.00000000, 24000.00),
    (3, 1, 1.00000000, 42000.00000000, 48000.00),
    (3, 2, 20.00000000, 2100.00000000, 48000.00);
GO

-- 15. TRANSACCIONES
INSERT INTO TRANSACCIONES (tipo, cantidad, precio_unitario, valor_total, comision, comision_usd, moneda_destino, fecha_hora, estado, hash_blockchain, datos_origen_banco, datos_origen_pais, id_portfolio)
VALUES 
    ('COMPRA', 0.50000000, 48000.00000000, 24000.00, 0.00500000, 120.00, 'EUR', GETDATE(), 'CONFIRMADA', '0x1a2b3c4d', 'Banco Santander', 'España', 1),
    ('COMPRA', 5.00000000, 2400.00000000, 12000.00, 0.00250000, 60.00, 'EUR', DATEADD(HOUR, -1, GETDATE()), 'CONFIRMADA', '0x1a2b3c4e', 'Banco Santander', 'España', 1),
    ('VENTA', 0.25000000, 48000.00000000, 12000.00, 0.00400000, 80.00, 'MXN', DATEADD(HOUR, -2, GETDATE()), 'CONFIRMADA', '0x1a2b3c4f', 'BBVA México', 'México', 2),
    ('DEPOSITO', 10.00000000, 2200.00000000, 22000.00, 0.00200000, 40.00, 'ARS', DATEADD(HOUR, -3, GETDATE()), 'PENDIENTE', '0x1a2b3c50', 'Banco Galicia', 'Argentina', 3);
GO

-- 16. ALERTAS 
INSERT INTO ALERTAS (valor_objetivo, condicion, activa, sensibilidad, horarios_inicio, horarios_fin, id_crypto, id_portfolio, id_usuario)
VALUES 
    (50000.00000000, 'MAYOR_QUE', 1, 2.50, '08:00:00', '22:00:00', 1, 1, 1),
    (2500.00000000, 'MENOR_QUE', 1, 1.50, '09:00:00', '21:00:00', 2, 1, 1),
    (45000.00000000, 'RANGO', 1, 3.00, '06:00:00', '23:59:00', 1, 2, 2);
GO

-- 17. PALABRAS_CLAVE 
INSERT INTO PALABRAS_CLAVE (id_alerta, palabra_clave)
VALUES 
    (1, 'Bitcoin'),
    (1, 'Tendencia'),
    (1, 'Resistencia'),
    (2, 'Ethereum'),
    (2, 'Soporte'),
    (3, 'Bitcoin'),
    (3, 'Volatilidad');
GO

-- 18. TICKETS_SOPORTE 
INSERT INTO TICKETS_SOPORTE (asunto, descripcion, estado, prioridad, tiempo_resolucion, fecha_creacion, id_empleado, id_usuario)
VALUES 
    ('Problema con depósito', 'El depósito de $1000 no aparece en mi cuenta', 'RESUELTO', 'ALTA', 120, DATEADD(HOUR, -4, GETDATE()), 3, 1),
    ('Duda sobre fees de trading', 'Me gustaría entender mejor cómo se calculan las comisiones', 'EN_PROGRESO', 'BAJA', NULL, DATEADD(HOUR, -2, GETDATE()), 3, 2),
    ('Acceso denegado', 'No puedo acceder a mi cuenta desde esta IP', 'ABIERTO', 'CRITICA', NULL, GETDATE(), NULL, 3);
GO

-- VERIFICACIÓN FINAL

SELECT 
    'PLANES' as Tabla, COUNT(*) as Filas FROM PLANES
UNION ALL SELECT 'USUARIOS', COUNT(*) FROM USUARIOS
UNION ALL SELECT 'CRIPTOMONEDAS', COUNT(*) FROM CRIPTOMONEDAS
UNION ALL SELECT 'PRECIOS', COUNT(*) FROM PRECIOS
UNION ALL SELECT 'TAG_CATEGORIA', COUNT(*) FROM TAG_CATEGORIA
UNION ALL SELECT 'PORTFOLIOS', COUNT(*) FROM PORTFOLIOS
UNION ALL SELECT 'POSICIONES', COUNT(*) FROM POSICIONES
UNION ALL SELECT 'TRANSACCIONES', COUNT(*) FROM TRANSACCIONES
UNION ALL SELECT 'EMPLEADOS', COUNT(*) FROM EMPLEADOS
UNION ALL SELECT 'TRADERS', COUNT(*) FROM TRADERS
UNION ALL SELECT 'ANALISTAS', COUNT(*) FROM ANALISTAS
UNION ALL SELECT 'TECNICOS_SOPORTE', COUNT(*) FROM TECNICOS_SOPORTE
UNION ALL SELECT 'CRIMP_EMP', COUNT(*) FROM CRIMP_EMP
UNION ALL SELECT 'ALERTAS', COUNT(*) FROM ALERTAS
UNION ALL SELECT 'PALABRAS_CLAVE', COUNT(*) FROM PALABRAS_CLAVE
UNION ALL SELECT 'METRICAS_USUARIOS', COUNT(*) FROM METRICAS_USUARIOS
UNION ALL SELECT 'NOTIFICACIONES', COUNT(*) FROM NOTIFICACIONES
UNION ALL SELECT 'TICKETS_SOPORTE', COUNT(*) FROM TICKETS_SOPORTE
ORDER BY Tabla;
GO

SELECT * FROM USUARIOS
SELECT * FROM CRIPTOMONEDAS
SELECT * FROM TRANSACCIONES