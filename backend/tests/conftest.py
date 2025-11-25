import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import app, db
from db import Base, engine, SessionLocal
from models import (
    Cliente, Comanda, Mesa, Mozo, Producto, Seccion, 
    Sector, MedioPago, Plato, Postre, Bebida, DetalleComanda, Reserva
)

# Base de datos de test en memoria
TEST_DATABASE_URL = "sqlite:///:memory:"

# Crear engine de test
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)
TestSessionLocal = sessionmaker(bind=test_engine)

@pytest.fixture(scope='session', autouse=True)
def setup_test_db():
    """Configura la base de datos de test antes de todos los tests"""
    # Crear todas las tablas
    Base.metadata.create_all(bind=test_engine)
    yield
    # Limpiar después de todos los tests
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope='function', autouse=True)
def setup_test_db_for_routes(monkeypatch):
    """Reemplaza SessionLocal en db.py para cada test"""
    import db as db_module
    # Usar monkeypatch para reemplazar SessionLocal en todos los módulos que lo usan
    monkeypatch.setattr(db_module, 'engine', test_engine)
    monkeypatch.setattr(db_module, 'SessionLocal', TestSessionLocal)
    
    # También reemplazar en los módulos de rutas que ya lo importaron
    import routes.cliente_routes as cr
    import routes.comanda_routes as comr
    import routes.mesa_routes as mr
    import routes.mozo_routes as mor
    import routes.producto_routes as pr
    import routes.seccion_routes as sr
    import routes.sector_routes as secr
    import routes.medio_pagos_routes as mpr
    import routes.reserva_routes as resr
    
    monkeypatch.setattr(cr, 'SessionLocal', TestSessionLocal)
    monkeypatch.setattr(comr, 'SessionLocal', TestSessionLocal)
    monkeypatch.setattr(mr, 'SessionLocal', TestSessionLocal)
    monkeypatch.setattr(mor, 'SessionLocal', TestSessionLocal)
    monkeypatch.setattr(pr, 'SessionLocal', TestSessionLocal)
    monkeypatch.setattr(sr, 'SessionLocal', TestSessionLocal)
    monkeypatch.setattr(secr, 'SessionLocal', TestSessionLocal)
    monkeypatch.setattr(mpr, 'SessionLocal', TestSessionLocal)
    monkeypatch.setattr(resr, 'SessionLocal', TestSessionLocal)

@pytest.fixture(scope='session')
def test_app():
    """Crea una aplicación Flask para testing"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def test_client(test_app):
    """Cliente de test para hacer requests"""
    return test_app.test_client()

@pytest.fixture(scope='function', autouse=True)
def clean_test_db():
    """Limpia la base de datos antes de cada test"""
    # Limpiar todas las tablas antes de cada test
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    # Limpiar después del test
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope='function')
def test_db_session(test_app):
    """Sesión de base de datos para cada test"""
    connection = test_engine.connect()
    transaction = connection.begin()
    
    # Crear una sesión vinculada a esta conexión
    session = sessionmaker(bind=connection)()
    
    yield session
    
    # Rollback y limpiar
    transaction.rollback()
    connection.close()
    session.close()

# Fixtures para datos de ejemplo
@pytest.fixture
def sample_cliente_data():
    """Datos de ejemplo para crear un cliente"""
    return {
        'documento': '12345678',
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'num_telefono': '1234567890',
        'email': 'juan@example.com'
    }

@pytest.fixture
def sample_sector_data():
    """Datos de ejemplo para crear un sector"""
    return {
        'numero': 1
    }

@pytest.fixture
def sample_seccion_data():
    """Datos de ejemplo para crear una sección"""
    return {
        'nombre': 'Platos Principales'
    }

@pytest.fixture
def sample_medio_pago_data():
    """Datos de ejemplo para crear un medio de pago"""
    return {
        'nombre': 'Efectivo',
        'descripcion': 'Pago en efectivo'
    }

@pytest.fixture
def sample_mozo_data():
    """Datos de ejemplo para crear un mozo"""
    return {
        'documento': '87654321',
        'nombre_apellido': 'Carlos García',
        'direccion': 'Calle Falsa 123',
        'telefono': '9876543210'
    }

@pytest.fixture
def sample_mesa_data():
    """Datos de ejemplo para crear una mesa"""
    return {
        'numero': 1,
        'tipo': 'Interior',
        'cant_comensales': 4
    }

@pytest.fixture
def sample_producto_data():
    """Datos de ejemplo para crear un producto"""
    return {
        'codigo': 'PROD001',
        'nombre': 'Milanesa',
        'precio': 1500.00,
        'descripcion': 'Milanesa napolitana'
    }

@pytest.fixture
def sample_comanda_data():
    """Datos de ejemplo para crear una comanda"""
    return {
        'fecha': '2024-01-15'
    }

# Fixtures que crean objetos en la BD para tests que requieren relaciones
@pytest.fixture
def created_sector(test_db_session, sample_sector_data):
    """Crea un sector en la BD y lo retorna"""
    sector = Sector(**sample_sector_data)
    test_db_session.add(sector)
    test_db_session.commit()
    test_db_session.refresh(sector)
    return sector

@pytest.fixture
def created_seccion(test_db_session, sample_seccion_data):
    """Crea una sección en la BD y la retorna"""
    seccion = Seccion(**sample_seccion_data)
    test_db_session.add(seccion)
    test_db_session.commit()
    test_db_session.refresh(seccion)
    return seccion

@pytest.fixture
def created_mozo(test_db_session, sample_mozo_data, created_sector):
    """Crea un mozo en la BD y lo retorna"""
    mozo_data = sample_mozo_data.copy()
    mozo_data['id_sector'] = created_sector.id_sector
    mozo = Mozo(**mozo_data)
    test_db_session.add(mozo)
    test_db_session.commit()
    test_db_session.refresh(mozo)
    return mozo

@pytest.fixture
def created_mesa(test_db_session, sample_mesa_data, created_sector):
    """Crea una mesa en la BD y la retorna"""
    mesa_data = sample_mesa_data.copy()
    mesa_data['id_sector'] = created_sector.id_sector
    mesa = Mesa(**mesa_data)
    test_db_session.add(mesa)
    test_db_session.commit()
    test_db_session.refresh(mesa)
    return mesa

@pytest.fixture
def created_producto(test_db_session, sample_producto_data, created_seccion):
    """Crea un producto en la BD y lo retorna"""
    producto_data = sample_producto_data.copy()
    producto_data['id_seccion'] = created_seccion.id_seccion
    producto = Producto(**producto_data)
    test_db_session.add(producto)
    test_db_session.commit()
    test_db_session.refresh(producto)
    return producto

@pytest.fixture
def created_cliente(test_db_session, sample_cliente_data):
    """Crea un cliente en la BD y lo retorna"""
    cliente = Cliente(**sample_cliente_data)
    test_db_session.add(cliente)
    test_db_session.commit()
    test_db_session.refresh(cliente)
    return cliente

@pytest.fixture
def created_medio_pago(test_db_session, sample_medio_pago_data):
    """Crea un medio de pago en la BD y lo retorna"""
    medio_pago = MedioPago(**sample_medio_pago_data)
    test_db_session.add(medio_pago)
    test_db_session.commit()
    test_db_session.refresh(medio_pago)
    return medio_pago

@pytest.fixture
def created_comanda(test_db_session, sample_comanda_data, created_mozo, created_mesa):
    """Crea una comanda en la BD y la retorna"""
    comanda_data = sample_comanda_data.copy()
    comanda_data['id_mozo'] = created_mozo.id
    comanda_data['id_mesa'] = created_mesa.id_mesa
    comanda = Comanda(**comanda_data)
    test_db_session.add(comanda)
    test_db_session.commit()
    test_db_session.refresh(comanda)
    return comanda

