from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Producto(Base):
    __tablename__ = 'producto'
    id_producto = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(255), nullable=False)
    precio = Column(DECIMAL(10, 2), nullable=False)
    id_seccion = Column(Integer, ForeignKey('seccion.id_seccion'), nullable=False)
    descripcion = Column(Text)
    baja = Column(Boolean, default=False)
    seccion = relationship("Seccion", back_populates="productos")
    plato = relationship("Plato", uselist=False, back_populates="producto")
    postre = relationship("Postre", uselist=False, back_populates="producto")
    bebida = relationship("Bebida", uselist=False, back_populates="producto")

    def __init__(self, codigo, nombre, precio, id_seccion, descripcion=None, baja=False):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.id_seccion = id_seccion
        self.descripcion = descripcion
        self.baja = baja

    def json(self):
        return {
            'id_producto': self.id_producto,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'precio': float(self.precio),
            'id_seccion': self.id_seccion,
            'descripcion': self.descripcion,
            'baja': self.baja,
        }

class Plato(Base):
    __tablename__ = 'plato'
    id_plato = Column(Integer, ForeignKey('producto.id_producto'), primary_key=True)
    producto = relationship("Producto", back_populates="plato")
    
    def __init__(self, id_plato):
        self.id_plato = id_plato

    def json(self):
        return {
            'id_plato': self.id_plato,
            'producto': self.producto.json() if self.producto else None,
        }

class Postre(Base):
    __tablename__ = 'postre'
    id_postre = Column(Integer, ForeignKey('producto.id_producto'), primary_key=True)
    producto = relationship("Producto", back_populates="postre")

    def __init__(self, id_postre):
        self.id_postre = id_postre

    def json(self):
        return {
            'id_postre': self.id_postre,
            'producto': self.producto.json() if self.producto else None,
        }

class Bebida(Base):
    __tablename__ = 'bebida'
    id_bebida = Column(Integer, ForeignKey('producto.id_producto'), primary_key=True)
    cm3 = Column(Integer, nullable=False)
    producto = relationship("Producto", back_populates="bebida")

    def __init__(self, id_bebida, cm3):
        self.id_bebida = id_bebida
        self.cm3 = cm3

    def json(self):
        return {
            'id_bebida': self.id_bebida,
            'cm3': self.cm3,
            'producto': self.producto.json() if self.producto else None,
        }

