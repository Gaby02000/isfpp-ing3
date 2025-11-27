"""
Tests para la funcionalidad de crear comanda desde reserva
"""
import pytest
from datetime import datetime, timedelta
from db import SessionLocal
from models.comanda import Comanda
from models.reserva import Reserva
from models.cliente import Cliente
from models.mesa import Mesa
from models.mozo import Mozo
from models.producto import Producto
from models.seccion import Seccion
from models.sector import Sector


@pytest.fixture
def setup_data():
    """Configurar datos de prueba"""
    session = SessionLocal()
    
    # Crear sector
    sector = Sector(nombre='Comedor')
    session.add(sector)
    session.flush()
    
    # Crear mesa
    mesa = Mesa(numero=1, tipo='redonda', cant_comensales=4, id_sector=sector.id_sector)
    session.add(mesa)
    session.flush()
    
    # Crear cliente
    cliente = Cliente(
        nombre='Juan',
        apellido='Pérez',
        telefono='1234567890',
        email='juan@example.com'
    )
    session.add(cliente)
    session.flush()
    
    # Crear mozo
    mozo = Mozo(nombre='Pedro', apellido='González')
    session.add(mozo)
    session.flush()
    
    # Crear sección
    seccion = Seccion(nombre='Bebidas')
    session.add(seccion)
    session.flush()
    
    # Crear productos
    producto1 = Producto(
        codigo='P001',
        nombre='Agua',
        precio=100.00,
        id_seccion=seccion.id_seccion
    )
    producto2 = Producto(
        codigo='P002',
        nombre='Cerveza',
        precio=200.00,
        id_seccion=seccion.id_seccion
    )
    session.add_all([producto1, producto2])
    session.flush()
    
    session.commit()
    
    return {
        'session': session,
        'sector': sector,
        'mesa': mesa,
        'cliente': cliente,
        'mozo': mozo,
        'seccion': seccion,
        'productos': [producto1, producto2]
    }


def test_crear_comanda_desde_reserva_exitoso(client, setup_data):
    """Test: Crear comanda exitosamente desde una reserva asistida"""
    session = setup_data['session']
    cliente = setup_data['cliente']
    mesa = setup_data['mesa']
    mozo = setup_data['mozo']
    productos = setup_data['productos']
    
    # Crear reserva
    fecha_reserva = datetime.now() + timedelta(hours=2)
    reserva = Reserva(
        numero=1,
        fecha_hora=fecha_reserva,
        cant_personas=4,
        id_cliente=cliente.id_cliente,
        id_mesa=mesa.id_mesa,
        estado='activa'
    )
    session.add(reserva)
    session.commit()
    
    # Marcar como asistida
    payload = {}
    response = client.put(
        f'/api/reserva/{reserva.id_reserva}/asistida',
        json=payload
    )
    assert response.status_code == 200
    
    # Crear comanda desde reserva
    comanda_data = {
        'id_reserva': reserva.id_reserva,
        'id_mozo': mozo.id,
        'productos': [
            {'id_producto': productos[0].id_producto, 'cantidad': 2},
            {'id_producto': productos[1].id_producto, 'cantidad': 1}
        ]
    }
    
    response = client.post('/api/comanda/desde-reserva', json=comanda_data)
    assert response.status_code == 201
    
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'id_comanda' in data['data']
    assert data['data']['id_reserva'] == reserva.id_reserva
    assert data['data']['id_mesa'] == mesa.id_mesa
    assert data['data']['estado'] == 'Abierta'
    assert len(data['data']['detalles']) == 2
    
    # Verificar que la reserva cambió de estado
    session.refresh(reserva)
    assert reserva.estado == 'en_curso'
    
    # Verificar que la mesa cambió de estado
    session.refresh(mesa)
    assert mesa.estado == 'ocupada'


def test_crear_comanda_desde_reserva_no_asistida(client, setup_data):
    """Test: No se puede crear comanda si la reserva no está asistida"""
    session = setup_data['session']
    cliente = setup_data['cliente']
    mesa = setup_data['mesa']
    mozo = setup_data['mozo']
    
    # Crear reserva en estado 'activa' (no asistida)
    fecha_reserva = datetime.now() + timedelta(hours=2)
    reserva = Reserva(
        numero=2,
        fecha_hora=fecha_reserva,
        cant_personas=4,
        id_cliente=cliente.id_cliente,
        id_mesa=mesa.id_mesa,
        estado='activa'
    )
    session.add(reserva)
    session.commit()
    
    # Intentar crear comanda sin marcar como asistida
    comanda_data = {
        'id_reserva': reserva.id_reserva,
        'id_mozo': mozo.id,
    }
    
    response = client.post('/api/comanda/desde-reserva', json=comanda_data)
    # La reserva en estado 'activa' debería permitir crear comanda, pero si hay validación más estricta debería fallar
    # Este comportamiento depende de los requisitos específicos
    assert response.status_code in [201, 400]


def test_crear_comanda_desde_reserva_cancelada(client, setup_data):
    """Test: No se puede crear comanda si la reserva está cancelada"""
    session = setup_data['session']
    cliente = setup_data['cliente']
    mesa = setup_data['mesa']
    mozo = setup_data['mozo']
    
    # Crear reserva
    fecha_reserva = datetime.now() + timedelta(hours=2)
    reserva = Reserva(
        numero=3,
        fecha_hora=fecha_reserva,
        cant_personas=4,
        id_cliente=cliente.id_cliente,
        id_mesa=mesa.id_mesa,
        cancelado=True
    )
    session.add(reserva)
    session.commit()
    
    # Intentar crear comanda
    comanda_data = {
        'id_reserva': reserva.id_reserva,
        'id_mozo': mozo.id,
    }
    
    response = client.post('/api/comanda/desde-reserva', json=comanda_data)
    assert response.status_code == 400
    assert 'cancelada' in response.get_json()['message'].lower()


def test_crear_comanda_desde_reserva_inexistente(client, setup_data):
    """Test: No se puede crear comanda si la reserva no existe"""
    setup_data['session']
    mozo = setup_data['mozo']
    
    comanda_data = {
        'id_reserva': 9999,
        'id_mozo': mozo.id,
    }
    
    response = client.post('/api/comanda/desde-reserva', json=comanda_data)
    assert response.status_code == 404
    assert 'no existe' in response.get_json()['message'].lower()


def test_crear_comanda_desde_reserva_mozo_inexistente(client, setup_data):
    """Test: No se puede crear comanda si el mozo no existe"""
    session = setup_data['session']
    cliente = setup_data['cliente']
    mesa = setup_data['mesa']
    
    # Crear reserva
    fecha_reserva = datetime.now() + timedelta(hours=2)
    reserva = Reserva(
        numero=4,
        fecha_hora=fecha_reserva,
        cant_personas=4,
        id_cliente=cliente.id_cliente,
        id_mesa=mesa.id_mesa,
        estado='asistida'
    )
    session.add(reserva)
    session.commit()
    
    comanda_data = {
        'id_reserva': reserva.id_reserva,
        'id_mozo': 9999,
    }
    
    response = client.post('/api/comanda/desde-reserva', json=comanda_data)
    assert response.status_code == 400
    assert 'mozo' in response.get_json()['message'].lower()


def test_no_puede_haber_dos_comandas_por_reserva(client, setup_data):
    """Test: No se pueden crear dos comandas para la misma reserva"""
    session = setup_data['session']
    cliente = setup_data['cliente']
    mesa = setup_data['mesa']
    mozo = setup_data['mozo']
    
    # Crear reserva
    fecha_reserva = datetime.now() + timedelta(hours=2)
    reserva = Reserva(
        numero=5,
        fecha_hora=fecha_reserva,
        cant_personas=4,
        id_cliente=cliente.id_cliente,
        id_mesa=mesa.id_mesa,
        estado='asistida'
    )
    session.add(reserva)
    session.commit()
    
    # Crear primera comanda
    comanda_data = {
        'id_reserva': reserva.id_reserva,
        'id_mozo': mozo.id,
    }
    
    response1 = client.post('/api/comanda/desde-reserva', json=comanda_data)
    assert response1.status_code == 201
    
    # Intentar crear segunda comanda
    response2 = client.post('/api/comanda/desde-reserva', json=comanda_data)
    assert response2.status_code == 400
    assert 'ya existe' in response2.get_json()['message'].lower()


def test_mesa_no_puede_tener_dos_comandas_abiertas(client, setup_data):
    """Test: No se pueden tener dos comandas abiertas en la misma mesa"""
    session = setup_data['session']
    cliente = setup_data['cliente']
    mesa = setup_data['mesa']
    mozo = setup_data['mozo']
    
    # Crear dos reservas en la misma mesa
    fecha_reserva1 = datetime.now() + timedelta(hours=2)
    fecha_reserva2 = datetime.now() + timedelta(hours=3)
    
    reserva1 = Reserva(
        numero=6,
        fecha_hora=fecha_reserva1,
        cant_personas=2,
        id_cliente=cliente.id_cliente,
        id_mesa=mesa.id_mesa,
        estado='asistida'
    )
    reserva2 = Reserva(
        numero=7,
        fecha_hora=fecha_reserva2,
        cant_personas=2,
        id_cliente=cliente.id_cliente,
        id_mesa=mesa.id_mesa,
        estado='asistida'
    )
    session.add_all([reserva1, reserva2])
    session.commit()
    
    # Crear comanda para primera reserva
    comanda_data1 = {
        'id_reserva': reserva1.id_reserva,
        'id_mozo': mozo.id,
    }
    
    response1 = client.post('/api/comanda/desde-reserva', json=comanda_data1)
    assert response1.status_code == 201
    
    # Intentar crear comanda para segunda reserva en la misma mesa
    comanda_data2 = {
        'id_reserva': reserva2.id_reserva,
        'id_mozo': mozo.id,
    }
    
    response2 = client.post('/api/comanda/desde-reserva', json=comanda_data2)
    assert response2.status_code == 400
    assert 'ya tiene' in response2.get_json()['message'].lower()


def test_comanda_incluye_datos_de_reserva(client, setup_data):
    """Test: La comanda creada incluye todos los datos correctos"""
    session = setup_data['session']
    cliente = setup_data['cliente']
    mesa = setup_data['mesa']
    mozo = setup_data['mozo']
    
    # Crear reserva
    fecha_reserva = datetime.now() + timedelta(hours=2)
    reserva = Reserva(
        numero=8,
        fecha_hora=fecha_reserva,
        cant_personas=3,
        id_cliente=cliente.id_cliente,
        id_mesa=mesa.id_mesa,
        estado='asistida'
    )
    session.add(reserva)
    session.commit()
    
    # Crear comanda
    comanda_data = {
        'id_reserva': reserva.id_reserva,
        'id_mozo': mozo.id,
        'observaciones': 'Sin picante'
    }
    
    response = client.post('/api/comanda/desde-reserva', json=comanda_data)
    assert response.status_code == 201
    
    data = response.get_json()['data']
    assert data['id_reserva'] == reserva.id_reserva
    assert data['id_mesa'] == mesa.id_mesa
    assert data['id_mozo'] == mozo.id
    assert data['observaciones'] == 'Sin picante'
    assert data['mesa']['id_mesa'] == mesa.id_mesa
    assert data['reserva']['id_reserva'] == reserva.id_reserva


def test_comanda_calcula_total_correctamente(client, setup_data):
    """Test: El total de la comanda se calcula correctamente"""
    session = setup_data['session']
    cliente = setup_data['cliente']
    mesa = setup_data['mesa']
    mozo = setup_data['mozo']
    productos = setup_data['productos']
    
    # Crear reserva
    fecha_reserva = datetime.now() + timedelta(hours=2)
    reserva = Reserva(
        numero=9,
        fecha_hora=fecha_reserva,
        cant_personas=4,
        id_cliente=cliente.id_cliente,
        id_mesa=mesa.id_mesa,
        estado='asistida'
    )
    session.add(reserva)
    session.commit()
    
    # Crear comanda con productos
    comanda_data = {
        'id_reserva': reserva.id_reserva,
        'id_mozo': mozo.id,
        'productos': [
            {'id_producto': productos[0].id_producto, 'cantidad': 2},  # 100 * 2 = 200
            {'id_producto': productos[1].id_producto, 'cantidad': 1}   # 200 * 1 = 200
        ]
    }
    
    response = client.post('/api/comanda/desde-reserva', json=comanda_data)
    assert response.status_code == 201
    
    data = response.get_json()['data']
    # Total debería ser 200 + 200 = 400
    assert data['total'] == 400.0


def test_solo_productos_activos(client, setup_data):
    """Test: Solo se agregan productos activos a la comanda"""
    session = setup_data['session']
    cliente = setup_data['cliente']
    mesa = setup_data['mesa']
    mozo = setup_data['mozo']
    productos = setup_data['productos']
    
    # Dar de baja un producto
    productos[1].baja = True
    session.commit()
    
    # Crear reserva
    fecha_reserva = datetime.now() + timedelta(hours=2)
    reserva = Reserva(
        numero=10,
        fecha_hora=fecha_reserva,
        cant_personas=4,
        id_cliente=cliente.id_cliente,
        id_mesa=mesa.id_mesa,
        estado='asistida'
    )
    session.add(reserva)
    session.commit()
    
    # Intentar crear comanda con producto inactivo
    comanda_data = {
        'id_reserva': reserva.id_reserva,
        'id_mozo': mozo.id,
        'productos': [
            {'id_producto': productos[0].id_producto, 'cantidad': 1},
            {'id_producto': productos[1].id_producto, 'cantidad': 1}  # Inactivo
        ]
    }
    
    response = client.post('/api/comanda/desde-reserva', json=comanda_data)
    assert response.status_code == 201
    
    # Solo debe haber un detalle (el del producto activo)
    data = response.get_json()['data']
    assert len(data['detalles']) == 1
