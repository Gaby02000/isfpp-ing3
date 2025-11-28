from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Factura(Base):
    __tablename__ = 'factura'
    
    id_factura = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False, unique=True)
    fecha = Column(String(50), nullable=False)
    total = Column(Numeric(10,2), nullable=False)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=False)
    id_comanda = Column(Integer, ForeignKey('comanda.id_comanda'), nullable=True)
    baja = Column(Boolean, default=False)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="factura")
    comanda = relationship("Comanda", back_populates="factura")
    detalles = relationship("DetalleFactura", back_populates="factura", cascade="all, delete-orphan")
    pagos = relationship("Pago", back_populates="factura")
    
    def __init__(self, codigo, fecha, total, id_cliente, id_comanda):
        self.codigo = codigo
        self.fecha = fecha
        self.total = total
        self.id_cliente = id_cliente
        self.id_comanda = id_comanda
        self.baja = False

    def calcular_total_pagado(self):
        """Calcula el total pagado de la factura sumando todos los pagos"""
        if not self.pagos:
            return 0.0
        return sum(float(pago.monto) for pago in self.pagos)

    def calcular_saldo_pendiente(self):
        """Calcula el saldo pendiente de la factura (total - pagado)"""
        total_pagado = self.calcular_total_pagado()
        return float(self.total) - total_pagado

    def esta_pagada(self):
        """Retorna True si la factura está completamente pagada"""
        return self.calcular_saldo_pendiente() <= 0

    def json(self):
        total_pagado = self.calcular_total_pagado()
        saldo_pendiente = self.calcular_saldo_pendiente()
        return {
            'id_factura': self.id_factura,
            'codigo': self.codigo,
            'fecha': self.fecha,
            'total': float(self.total),
            'id_cliente': self.id_cliente,
            'cliente': self.cliente.json() if self.cliente else None,
            'id_comanda': self.id_comanda,
            'comanda': self.comanda.json() if self.comanda else None,
            'detalles': [d.json() for d in self.detalles] if self.detalles else [],
            'baja': self.baja,
            'total_pagado': total_pagado,
            'saldo_pendiente': saldo_pendiente,
            'esta_pagada': self.esta_pagada()
        }