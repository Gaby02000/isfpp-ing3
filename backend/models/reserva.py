from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,TIMESTAMP, func
from sqlalchemy.orm import relationship
from db import Base

class Reserva(Base):
    __tablename__ = 'reserva'

    id_reserva = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False, unique=True)
    fecha_hora = Column(TIMESTAMP, nullable=False)
    cant_personas = Column(Integer, nullable=False)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=False)
    id_mesa = Column(Integer, ForeignKey('mesa.id_mesa'), nullable=False)
    cancelado = Column(Boolean, default=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    #Relaciones

    cliente =  relationship("Cliente", back_populates="reservas")
    mesa = relationship("Mesa", back_populates="reservas")

    def __init__(self, numero, fecha_hora, cant_personas, id_cliente, id_mesa, cancelado=False):
        self.numero = numero
        self.fecha_hora = fecha_hora
        self.cant_personas = cant_personas
        self.id_cliente = id_cliente
        self.id_mesa = id_mesa
        self.cancelado = cancelado

    def json(self):
        return {
            'id_reserva': self.id_reserva,
            'numero': self.numero,
            'fecha_hora': str(self.fecha_hora),
            'cant_personas': self.cant_personas,
            'id_cliente': self.id_cliente,
            'cliente': self.cliente.json() if self.cliente else None,
            'id_mesa': self.id_mesa,
            'mesa': self.mesa.json() if self.mesa else None,
            'cancelado': self.cancelado,
            'fecha_creacion': str(self.fecha_creacion) if self.fecha_creacion else None
        }