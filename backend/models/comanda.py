#Crear comandas para los pedidos de los clientes
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Comanda(Base):
    __tablename__ = 'comanda'
    
    id_comanda = Column(Integer, primary_key=True)
    fecha = Column(String(50), nullable=False)
    id_mozo = Column(Integer, ForeignKey('mozo.id'), nullable=False)
    id_mesa = Column(Integer, ForeignKey('mesa.id_mesa'), nullable=False)
    baja = Column(Boolean, default=False)
    
    # Relaciones
    mesa = relationship("Mesa", back_populates="comandas")
    mozo = relationship("Mozo", back_populates="comandas")

    def __init__(self, fecha, id_mozo, id_mesa, baja=False):
        self.fecha = fecha
        self.id_mozo = id_mozo
        self.id_mesa = id_mesa
        self.baja = baja

    def json(self):
        return {
            'id_comanda': self.id_comanda,
            'fecha': self.fecha,
            'id_mozo': self.id_mozo,
            'mozo': self.mozo.json() if self.mozo else None,
            'id_mesa': self.id_mesa,
            'mesa': self.mesa.json() if self.mesa else None,
            'baja': self.baja,
        }