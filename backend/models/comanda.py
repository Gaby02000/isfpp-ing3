#Crear comandas para los pedidos de los clientes
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from db import Base

class Comanda(Base):
    __tablename__ = 'comanda'
    
    id_comanda = Column(Integer, primary_key=True)
    fecha = Column(String(50), nullable=False)
    fecha_cierre = Column(String(50), nullable=True)
    id_mozo = Column(Integer, ForeignKey('mozo.id'), nullable=False)
    id_mesa = Column(Integer, ForeignKey('mesa.id_mesa'), nullable=False)
    id_reserva = Column(Integer, ForeignKey('reserva.id_reserva'), nullable=True)
    estado = Column(String(20), nullable=False, default='Abierta')
    observaciones = Column(Text, nullable=True)
    baja = Column(Boolean, default=False)
    
    # Relaciones
    mesa = relationship("Mesa", back_populates="comandas")
    mozo = relationship("Mozo", back_populates="comandas")
    detalles = relationship("DetalleComanda", back_populates="comanda", cascade="all, delete-orphan")
    factura = relationship("Factura", back_populates="comanda", uselist=False)
    reserva = relationship("Reserva", foreign_keys=[id_reserva])
    # Nota: el cliente ahora pertenece únicamente a la Factura; se eliminó la relación aquí

    def __init__(self, fecha, id_mozo, id_mesa, fecha_cierre=None, estado='Abierta', observaciones=None, baja=False, id_reserva=None):
        self.fecha = fecha
        self.fecha_cierre = fecha_cierre
        self.id_mozo = id_mozo
        self.id_mesa = id_mesa
        self.id_reserva = id_reserva
        self.estado = estado
        self.observaciones = observaciones
        self.baja = baja

    def calcular_total(self):
        """Calcula el total de la comanda sumando todos los detalles"""
        if not self.detalles:
            return 0.0
        return sum(float(detalle.precio_unitario * detalle.cantidad) for detalle in self.detalles)

    def json(self):
        detalles_json = [detalle.json() for detalle in self.detalles] if self.detalles else []
        return {
            'id_comanda': self.id_comanda,
            'fecha': self.fecha,
            'fecha_cierre': self.fecha_cierre,
            'id_mozo': self.id_mozo,
            'mozo': self.mozo.json() if self.mozo else None,
            'id_mesa': self.id_mesa,
            'mesa': self.mesa.json() if self.mesa else None,
            'id_reserva': self.id_reserva,
            'reserva': self.reserva.json() if self.reserva else None,
            # Cliente se maneja a nivel de Factura, no en la Comanda
            'estado': self.estado,
            'observaciones': self.observaciones,
            'baja': self.baja,
            'detalles': detalles_json,
            'total': self.calcular_total()
        }