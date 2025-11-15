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
        REFERENCES sector(id)
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
        REFERENCES sector(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- Inserciones
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