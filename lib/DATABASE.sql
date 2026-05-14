-- ==========================================
-- CryptoLearning - DATABASE CORREGIDA MySQL 8
-- ==========================================

DROP DATABASE IF EXISTS CryptoLearning;
CREATE DATABASE CryptoLearning CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE CryptoLearning;

-- 1. USUARIOS
CREATE TABLE IF NOT EXISTS USUARIOS (
    id_usuario   INT AUTO_INCREMENT PRIMARY KEY,
    dni          VARCHAR(15)  NOT NULL UNIQUE,
    nombre       VARCHAR(100) NOT NULL,
    apellidos    VARCHAR(150) NOT NULL,
    email        VARCHAR(120) NOT NULL UNIQUE,
    password     VARCHAR(255) NOT NULL,
    rol          ENUM('ADMIN','ANALISTA','TRADER') NOT NULL,
    avatar_url   VARCHAR(255),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    activo       BOOLEAN DEFAULT TRUE
);

-- 2. ACTIVOS
CREATE TABLE IF NOT EXISTS ACTIVOS (
    id_activo           INT AUTO_INCREMENT PRIMARY KEY,
    nombre              VARCHAR(50)    NOT NULL,
    simbolo             VARCHAR(10)    NOT NULL UNIQUE,
    slug                VARCHAR(50)    UNIQUE,
    precio_actual       DECIMAL(18,8)  NOT NULL,
    descripcion_especial TEXT,
    es_cripto           BOOLEAN DEFAULT TRUE
);

-- 3. CARTERAS
CREATE TABLE IF NOT EXISTS CARTERAS (
    id_cartera          INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario          INT NOT NULL UNIQUE,
    saldo_fiat          DECIMAL(18,2) DEFAULT 10000.00,
    ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES USUARIOS(id_usuario) ON DELETE CASCADE
);

-- 4. POSICIONES
CREATE TABLE IF NOT EXISTS POSICIONES (
    id_posicion         INT AUTO_INCREMENT PRIMARY KEY,
    id_cartera          INT NOT NULL,
    id_activo           INT NOT NULL,
    cantidad            DECIMAL(18,8) DEFAULT 0.00000000,
    precio_medio_compra DECIMAL(18,8) DEFAULT 0.00000000,
    FOREIGN KEY (id_cartera) REFERENCES CARTERAS(id_cartera) ON DELETE CASCADE,
    FOREIGN KEY (id_activo)  REFERENCES ACTIVOS(id_activo)   ON DELETE CASCADE,
    UNIQUE(id_cartera, id_activo)
);

-- 5. HISTORIAL_PRECIOS
CREATE TABLE IF NOT EXISTS HISTORIAL_PRECIOS (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_activo    INT NOT NULL,
    precio       DECIMAL(18,8) NOT NULL,
    fecha_hora   DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_activo) REFERENCES ACTIVOS(id_activo) ON DELETE CASCADE
);

-- 6. OPERACIONES
CREATE TABLE IF NOT EXISTS OPERACIONES (
    id_operacion    INT AUTO_INCREMENT PRIMARY KEY,
    id_cartera      INT NOT NULL,
    id_activo       INT NOT NULL,
    tipo            ENUM('COMPRA','VENTA') NOT NULL,
    cantidad        DECIMAL(18,8) NOT NULL,
    precio_ejecucion DECIMAL(18,8) NOT NULL,
    total_fiat      DECIMAL(18,2) NOT NULL,
    fecha_hora      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cartera) REFERENCES CARTERAS(id_cartera) ON DELETE CASCADE,
    FOREIGN KEY (id_activo)  REFERENCES ACTIVOS(id_activo)   ON DELETE CASCADE
);

-- 7. EVENTOS_MERCADO
CREATE TABLE IF NOT EXISTS EVENTOS_MERCADO (
    id_evento              INT AUTO_INCREMENT PRIMARY KEY,
    id_admin               INT NOT NULL,
    es_aviso               BIT DEFAULT 1,
    nombre_evento          VARCHAR(100) NOT NULL,
    multiplicador_aplicado FLOAT NOT NULL DEFAULT 1.0,
    descripcion            TEXT,
    fecha_ejecucion        DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_admin) REFERENCES USUARIOS(id_usuario) ON DELETE CASCADE
);

-- 8. NOTICIAS
CREATE TABLE IF NOT EXISTS NOTICIAS (
    id_noticia       INT AUTO_INCREMENT PRIMARY KEY,
    id_analista      INT NOT NULL,
    titulo           VARCHAR(200) NOT NULL,
    cuerpo           TEXT NOT NULL,
    es_aviso         BOOLEAN DEFAULT FALSE,
    fecha_publicacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_analista) REFERENCES USUARIOS(id_usuario) ON DELETE CASCADE
);

-- ==========================================
-- TRIGGER: Crear cartera automáticamente
-- ==========================================
DELIMITER //
CREATE TRIGGER trg_crear_cartera_trader
AFTER INSERT ON USUARIOS
FOR EACH ROW
BEGIN
    IF NEW.rol = 'TRADER' THEN
        INSERT INTO CARTERAS (id_usuario, saldo_fiat)
        VALUES (NEW.id_usuario, 10000.00);
    END IF;
END; //
DELIMITER ;

-- ==========================================
-- STORED PROCEDURE: Realizar operación
-- ==========================================
DELIMITER //
CREATE PROCEDURE sp_realizar_operacion(
    IN p_id_usuario INT,
    IN p_id_activo  INT,
    IN p_tipo       ENUM('COMPRA','VENTA'),
    IN p_cantidad   DECIMAL(18,8)
)  -- <-- ) que faltaba en el original
BEGIN
    DECLARE v_id_cartera         INT;
    DECLARE v_precio_actual      DECIMAL(18,8);
    DECLARE v_total_fiat         DECIMAL(18,2);
    DECLARE v_saldo_fiat         DECIMAL(18,2);
    DECLARE v_cantidad_poseida   DECIMAL(18,8) DEFAULT 0;
    DECLARE v_precio_medio_antiguo DECIMAL(18,8) DEFAULT 0;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT id_cartera, saldo_fiat INTO v_id_cartera, v_saldo_fiat
    FROM CARTERAS WHERE id_usuario = p_id_usuario FOR UPDATE;

    SELECT precio_actual INTO v_precio_actual
    FROM ACTIVOS WHERE id_activo = p_id_activo;

    SET v_total_fiat = p_cantidad * v_precio_actual;

    SELECT cantidad, precio_medio_compra INTO v_cantidad_poseida, v_precio_medio_antiguo
    FROM POSICIONES
    WHERE id_cartera = v_id_cartera AND id_activo = p_id_activo;

    IF p_tipo = 'COMPRA' THEN
        IF v_saldo_fiat < v_total_fiat THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Saldo fiat insuficiente para realizar la compra';
        END IF;
        UPDATE CARTERAS SET saldo_fiat = saldo_fiat - v_total_fiat WHERE id_cartera = v_id_cartera;
        IF v_cantidad_poseida > 0 THEN
            UPDATE POSICIONES
            SET precio_medio_compra = ((v_cantidad_poseida * v_precio_medio_antiguo) + v_total_fiat) / (v_cantidad_poseida + p_cantidad),
                cantidad = cantidad + p_cantidad
            WHERE id_cartera = v_id_cartera AND id_activo = p_id_activo;
        ELSE
            INSERT INTO POSICIONES (id_cartera, id_activo, cantidad, precio_medio_compra)
            VALUES (v_id_cartera, p_id_activo, p_cantidad, v_precio_actual);
        END IF;

    ELSEIF p_tipo = 'VENTA' THEN
        IF v_cantidad_poseida < p_cantidad THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cantidad de activo insuficiente para realizar la venta';
        END IF;
        UPDATE CARTERAS SET saldo_fiat = saldo_fiat + v_total_fiat WHERE id_cartera = v_id_cartera;
        UPDATE POSICIONES SET cantidad = cantidad - p_cantidad
        WHERE id_cartera = v_id_cartera AND id_activo = p_id_activo;
    END IF;

    INSERT INTO OPERACIONES (id_cartera, id_activo, tipo, cantidad, precio_ejecucion, total_fiat)
    VALUES (v_id_cartera, p_id_activo, p_tipo, p_cantidad, v_precio_actual, v_total_fiat);

    COMMIT;
END; //
DELIMITER ;

-- ==========================================
-- STORED PROCEDURE: Ejecutar evento de mercado
-- ==========================================
DELIMITER //
CREATE PROCEDURE sp_ejecutar_evento_mercado(
    IN p_id_admin      INT,
    IN p_nombre_evento VARCHAR(100),
    IN p_descripcion   TEXT
)  -- <-- ) que faltaba en el original
BEGIN
    DECLARE done        INT DEFAULT FALSE;
    DECLARE v_id_activo INT;
    DECLARE v_simbolo   VARCHAR(10);
    DECLARE v_precio_actual  DECIMAL(18,8);
    DECLARE v_min_mult  DECIMAL(5,2);
    DECLARE v_max_mult  DECIMAL(5,2);
    DECLARE v_mult_aplicado DECIMAL(18,8);
    DECLARE v_nuevo_precio  DECIMAL(18,8);

    DECLARE cur_activos CURSOR FOR
        SELECT id_activo, simbolo, precio_actual FROM ACTIVOS;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; RESIGNAL; END;

    START TRANSACTION;

    INSERT INTO EVENTOS_MERCADO (id_admin, nombre_evento, descripcion, multiplicador_aplicado)
    VALUES (p_id_admin, p_nombre_evento, p_descripcion, 1.0);

    OPEN cur_activos;
    read_loop: LOOP
        FETCH cur_activos INTO v_id_activo, v_simbolo, v_precio_actual;
        IF done THEN LEAVE read_loop; END IF;

        -- Rangos por evento y símbolo
        IF p_nombre_evento = 'Bull Market' THEN
            IF v_simbolo = 'BTC'  THEN SET v_min_mult=0.95; SET v_max_mult=1.40;
            ELSEIF v_simbolo = 'GOLD' THEN SET v_min_mult=0.98; SET v_max_mult=1.10;
            ELSE SET v_min_mult=0.90; SET v_max_mult=1.45; END IF;
        ELSEIF p_nombre_evento = 'Bear Market' THEN
            IF v_simbolo = 'BTC'  THEN SET v_min_mult=0.60; SET v_max_mult=1.05;
            ELSEIF v_simbolo = 'GOLD' THEN SET v_min_mult=0.98; SET v_max_mult=1.08;
            ELSE SET v_min_mult=0.55; SET v_max_mult=1.10; END IF;
        ELSEIF p_nombre_evento = 'Crisis Fiat' THEN
            IF v_simbolo = 'BTC'  THEN SET v_min_mult=0.90; SET v_max_mult=1.40;
            ELSEIF v_simbolo = 'GOLD' THEN SET v_min_mult=0.98; SET v_max_mult=1.50;
            ELSE SET v_min_mult=0.45; SET v_max_mult=0.85; END IF;
        ELSEIF p_nombre_evento = 'Guerra Mundial' THEN
            IF v_simbolo = 'GOLD' THEN SET v_min_mult=1.10; SET v_max_mult=1.60;
            ELSEIF v_simbolo = 'BTC' THEN SET v_min_mult=0.50; SET v_max_mult=0.90;
            ELSE SET v_min_mult=0.40; SET v_max_mult=0.80; END IF;
        ELSEIF p_nombre_evento = 'Halving Bitcoin' THEN
            IF v_simbolo = 'BTC'  THEN SET v_min_mult=1.20; SET v_max_mult=2.00;
            ELSEIF v_simbolo = 'GOLD' THEN SET v_min_mult=0.98; SET v_max_mult=1.05;
            ELSE SET v_min_mult=1.05; SET v_max_mult=1.30; END IF;
        ELSEIF p_nombre_evento = 'Hack Exchange' THEN
            IF v_simbolo = 'GOLD' THEN SET v_min_mult=1.02; SET v_max_mult=1.15;
            ELSE SET v_min_mult=0.50; SET v_max_mult=0.85; END IF;
        ELSE
            SET v_min_mult=0.99; SET v_max_mult=1.01;
        END IF;

        SET v_mult_aplicado = v_min_mult + (RAND() * (v_max_mult - v_min_mult));
        SET v_nuevo_precio  = v_precio_actual * v_mult_aplicado;

        UPDATE ACTIVOS SET precio_actual = v_nuevo_precio WHERE id_activo = v_id_activo;
        INSERT INTO HISTORIAL_PRECIOS (id_activo, precio) VALUES (v_id_activo, v_nuevo_precio);
    END LOOP;
    CLOSE cur_activos;
    COMMIT;
END; //
DELIMITER ;

-- ==========================================
-- VISTAS
-- ==========================================
CREATE OR REPLACE VIEW vw_estado_cartera AS
SELECT c.id_cartera, u.id_usuario, u.nombre AS nombre_trader,
       c.saldo_fiat AS liquidez_disponible,
       IFNULL(SUM(p.cantidad * a.precio_actual), 0) AS valor_activos,
       c.saldo_fiat + IFNULL(SUM(p.cantidad * a.precio_actual), 0) AS patrimonio_total
FROM CARTERAS c
JOIN USUARIOS u ON c.id_usuario = u.id_usuario
LEFT JOIN POSICIONES p ON c.id_cartera = p.id_cartera
LEFT JOIN ACTIVOS a ON p.id_activo = a.id_activo
GROUP BY c.id_cartera, u.id_usuario, u.nombre, c.saldo_fiat;

CREATE OR REPLACE VIEW vw_rendimiento_posiciones AS
SELECT p.id_cartera, a.simbolo, a.nombre AS activo, p.cantidad,
       p.precio_medio_compra, a.precio_actual,
       (a.precio_actual - p.precio_medio_compra) * p.cantidad AS pnl_ganancia_perdida_fiat,
       CASE WHEN p.precio_medio_compra = 0 THEN 0
            ELSE ROUND(((a.precio_actual - p.precio_medio_compra) / p.precio_medio_compra) * 100, 2)
       END AS roi_porcentaje
FROM POSICIONES p
JOIN ACTIVOS a ON p.id_activo = a.id_activo
WHERE p.cantidad > 0;

CREATE OR REPLACE VIEW vw_historial_operaciones AS
SELECT o.id_operacion, o.id_cartera, o.fecha_hora, o.tipo AS operacion,
       a.simbolo, o.cantidad, o.precio_ejecucion, o.total_fiat
FROM OPERACIONES o
JOIN ACTIVOS a ON o.id_activo = a.id_activo
ORDER BY o.fecha_hora DESC;

-- ==========================================
-- SEED DATA
-- ==========================================
INSERT INTO USUARIOS (dni, nombre, apellidos, email, password, rol) VALUES
('00000000A', 'Profesor', 'Administrador', 'admin@unileon.es',
    SHA2('admin123', 256), 'ADMIN'),
('11111111B', 'Profesor', 'Analista', 'analista@unileon.es',
    SHA2('analista123', 256), 'ANALISTA');

INSERT INTO ACTIVOS (nombre, simbolo, slug, precio_actual, descripcion_especial, es_cripto) VALUES
('Bitcoin',     'BTC',  'bitcoin',      65000.00, 'Store Value - volatilidad media, REY',       TRUE),
('Ethereum',    'ETH',  'ethereum',     3500.00,  'Smart contracts - gas fees',                 TRUE),
('Oro digital', 'GOLD', 'oro-digital',  2300.00,  'Refugio - Estabilidad frente a crisis',      FALSE),
('Binance Coin','BNB',  'binance-coin', 580.00,   'Exchange - Volumen Trading',                 TRUE),
('Ripple',      'XRP',  'ripple',       0.60,     'Pagos - Transacciones Rápidas',              TRUE),
('Solana',      'SOL',  'solana',       145.00,   'High Speed - Competidor ETH',                TRUE),
('Cardano',     'ADA',  'cardano',      0.45,     'Research - Desarrollo académico',            TRUE),
('Dogecoin',    'DOGE', 'dogecoin',     0.15,     'Meme - Volatilidad extrema',                 TRUE),
('Chainlink',   'LINK', 'chainlink',    18.00,    'Oráculos - Datos externos',                  TRUE),
('Tether',      'USDT', 'tether',       1.00,     'Stablecoin - 100% estabilidad ($1.00)',      TRUE);

INSERT INTO HISTORIAL_PRECIOS (id_activo, precio)
SELECT id_activo, precio_actual FROM ACTIVOS;
