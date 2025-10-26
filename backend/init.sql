CREATE TABLE IF NOT EXISTS seccion (
    id_seccion SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    baja BOOLEAN DEFAULT FALSE
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
