CREATE TABLE IF NOT EXISTS cliente (
    id_cliente SERIAL PRIMARY KEY,
    documento VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    num_telefono VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL, 
    baja BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS seccion (
    id_seccion SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    baja BOOLEAN DEFAULT FALSE
);


--  Nueva tabla SECTOR
CREATE TABLE IF NOT EXISTS sector (
    id_sector SERIAL PRIMARY KEY,
    numero INTEGER UNIQUE NOT NULL,
    baja BOOLEAN DEFAULT false
);

-- Modificación de la tabla MESA para incluir referencia a SECTOR

CREATE TABLE IF NOT EXISTS mesa (
    id_mesa SERIAL PRIMARY KEY,
    numero INT NOT NULL UNIQUE,
    tipo VARCHAR(50) NOT NULL,
    cant_comensales INT NOT NULL CHECK (cant_comensales > 0),
    id_sector INT NOT NULL,
    baja BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_mesa_sector FOREIGN KEY (id_sector)
        REFERENCES sector(id_sector)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
    
CREATE TABLE IF NOT EXISTS producto (
    id_producto SERIAL PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    id_seccion INT NOT NULL,
    descripcion TEXT,
    baja BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_producto_seccion FOREIGN KEY (id_seccion)
        REFERENCES seccion(id_seccion)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS plato (
    id_plato INT PRIMARY KEY,
    CONSTRAINT fk_plato_producto FOREIGN KEY (id_plato)
        REFERENCES producto(id_producto)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS postre (
    id_postre INT PRIMARY KEY,
    CONSTRAINT fk_postre_producto FOREIGN KEY (id_postre)
        REFERENCES producto(id_producto)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS bebida (
    id_bebida INT PRIMARY KEY,
    cm3 INT NOT NULL CHECK (cm3 > 0),
    CONSTRAINT fk_bebida_producto FOREIGN KEY (id_bebida)
        REFERENCES producto(id_producto)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Nueva tabla MEDIO PAGO
CREATE TABLE IF NOT EXISTS medio_pago (
    id_medio_pago SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    baja BOOLEAN DEFAULT false
);


-- Nueva tabla MOZO
CREATE TABLE IF NOT EXISTS mozo (
    id SERIAL PRIMARY KEY,
    documento VARCHAR(20) UNIQUE NOT NULL,
    nombre_apellido VARCHAR(100) NOT NULL,
    direccion VARCHAR(150),
    telefono VARCHAR(50),
    id_sector INTEGER,
    baja BOOLEAN DEFAULT false,
    CONSTRAINT fk_mozo_sector FOREIGN KEY (id_sector)
        REFERENCES sector(id_sector)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS reserva (
    id_reserva SERIAL PRIMARY KEY,
    numero INT NOT NULL UNIQUE, -- número de reserva
    fecha_hora TIMESTAMP NOT NULL, -- fecha y hora de la reserva
    cant_personas INT NOT NULL CHECK (cant_personas > 0), -- cantidad de comensales
    id_cliente INT NOT NULL, -- FK al cliente
    id_mesa INT NOT NULL, -- FK a la mesa
    cancelado BOOLEAN DEFAULT FALSE, -- inicializa en "No" (FALSE)
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- fecha de creación
    fecha_modificacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    motivo_cancelacion VARCHAR(255),
    senia_devuelta BOOLEAN DEFAULT FALSE,
    senia_recuperada BOOLEAN DEFAULT FALSE,
    asistida BOOLEAN DEFAULT FALSE,

    -- Relaciones
    CONSTRAINT fk_reserva_cliente FOREIGN KEY (id_cliente)
        REFERENCES cliente(id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_reserva_mesa FOREIGN KEY (id_mesa)
        REFERENCES mesa(id_mesa)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Inserciones

INSERT INTO cliente (documento, nombre, apellido, num_telefono, email, baja)
VALUES
('30111222', 'Juan', 'Pérez', '2974456789', 'juan.perez@example.com', FALSE),
('30222333', 'María', 'González', '2974123456', 'maria.gonzalez@example.com', FALSE),
('30333444', 'Carlos', 'Ramírez', '2974987654', 'carlos.ramirez@example.com', FALSE),
('30444555', 'Ana', 'López', '2974765432', 'ana.lopez@example.com', FALSE),
('30555666', 'Pedro', 'Martínez', '2974234567', 'pedro.martinez@example.com', FALSE);

INSERT INTO seccion (nombre, baja) VALUES
('xd', FALSE),
('xd2', FALSE),
('xd3', FALSE);

INSERT INTO producto (codigo, nombre, precio, id_seccion, descripcion, baja) VALUES
('PL001', 'Milanesa con papas', 1200.00, 1, 'Milanesa de ternera acompañada de papas fritas', FALSE),
('PL002', 'Ensalada César', 900.00, 1, 'Lechuga, pollo, queso y aderezo César', FALSE),
('PO001', 'Flan casero', 450.00, 2, 'Flan con dulce de leche y crema', FALSE),
('PO002', 'Helado de chocolate', 400.00, 2, 'Helado artesanal de chocolate', FALSE),
('BE001', 'Coca-Cola 500ml', 250.00, 3, 'Bebida gaseosa de 500 cm3', FALSE),
('BE002', 'Agua mineral 500ml', 150.00, 3, 'Agua mineral sin gas', FALSE);

INSERT INTO plato (id_plato) VALUES (1),(2);
INSERT INTO postre (id_postre) VALUES (3),(4);
INSERT INTO bebida (id_bebida, cm3) VALUES (5, 500),(6, 500);


-- Inserts de ejemplo para SECTOR (idempotente)
INSERT INTO sector (numero, baja) VALUES
(1, FALSE),
(2, FALSE),
(3, FALSE);

-- Inserts de ejemplo para MOZO (idempotente)
INSERT INTO mozo (documento, nombre_apellido, direccion, telefono, id_sector, baja) VALUES
('20123456', 'Juan Perez', 'Calle Falsa 123', '111222333', 1, FALSE),
('20333444', 'María Gómez', 'Avenida Siempre Viva 742', '222333444', 2, FALSE);

-- Inserts de ejemplo para CLIENTE (idempotente)
INSERT INTO cliente (documento, nombre, apellido, num_telefono, email, baja) VALUES
('17555444', 'Marcelo', 'Santander', '2804000456', 'santander@gmail.com', FALSE);

-- Mesas del sector 1
INSERT INTO mesa (numero, tipo, cant_comensales, id_sector, baja)
VALUES (1, 'Interior', 4, 1, FALSE);

INSERT INTO mesa (numero, tipo, cant_comensales, id_sector, baja)
VALUES (2, 'Interior', 2, 1, FALSE);

-- Mesas del sector 2
INSERT INTO mesa (numero, tipo, cant_comensales, id_sector, baja)
VALUES (3, 'Terraza', 6, 2, FALSE);

INSERT INTO mesa (numero, tipo, cant_comensales, id_sector, baja)
VALUES (4, 'Terraza', 4, 2, FALSE);

-- Mesas del sector 3
INSERT INTO mesa (numero, tipo, cant_comensales, id_sector, baja)
VALUES (5, 'VIP', 8, 3, FALSE);

INSERT INTO mesa (numero, tipo, cant_comensales, id_sector, baja)
VALUES (6, 'VIP', 10, 3, FALSE);


-- Reserva en mesa 1 para cliente 1
-- Reserva en mesa 1 para cliente 1
INSERT INTO reserva (numero, fecha_hora, cant_personas, id_cliente, id_mesa, cancelado, fecha_creacion, fecha_modificacion, motivo_cancelacion, senia_devuelta, senia_recuperada, asistida)
VALUES (1001, '2025-11-25 20:30:00', 4, 1, 1, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, FALSE, FALSE, FALSE);

-- Reserva en mesa 2 para cliente 2
INSERT INTO reserva (numero, fecha_hora, cant_personas, id_cliente, id_mesa, cancelado, fecha_creacion, fecha_modificacion, motivo_cancelacion, senia_devuelta, senia_recuperada, asistida)
VALUES (1002, '2025-11-26 21:00:00', 2, 2, 2, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, FALSE, FALSE, FALSE);

-- Reserva en mesa 3 para cliente 3
INSERT INTO reserva (numero, fecha_hora, cant_personas, id_cliente, id_mesa, cancelado, fecha_creacion, fecha_modificacion, motivo_cancelacion, senia_devuelta, senia_recuperada, asistida)
VALUES (1003, '2025-11-27 19:00:00', 6, 3, 3, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, FALSE, FALSE, FALSE);

-- Reserva marcada como AUSENCIA (fecha pasada)
INSERT INTO reserva (numero, fecha_hora, cant_personas, id_cliente, id_mesa, cancelado, fecha_creacion, fecha_modificacion, motivo_cancelacion, senia_devuelta, senia_recuperada, asistida)
VALUES (1004, '2025-10-15 20:00:00', 4, 1, 1, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'ausencia', FALSE, TRUE, FALSE);

