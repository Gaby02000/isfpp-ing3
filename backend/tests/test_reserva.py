import pytest
from datetime import datetime, timedelta
from models import Reserva, Cliente, Mesa, Sector
from tests.utils.test_helpers import assert_response_success, assert_response_error


@pytest.fixture
def sample_reserva_data(created_cliente, created_mesa):
    """Datos de ejemplo para crear una reserva"""
    fecha_futura = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
    return {
        'numero': 1001,
        'fecha_hora': fecha_futura,
        'cant_personas': 2,
        'id_cliente': created_cliente.id_cliente,
        'id_mesa': created_mesa.id_mesa
    }


def test_crear_reserva_exitosamente(test_client, sample_reserva_data):
    """Prueba crear una reserva correctamente"""
    response = test_client.post('/api/reservas/', json=sample_reserva_data)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['numero'] == 1001
    assert data['data']['cant_personas'] == 2
    assert data['data']['cancelado'] is False


def test_listar_reservas(test_client, sample_reserva_data):
    """Prueba listar todas las reservas"""
    # Crear una reserva primero
    test_client.post('/api/reservas/', json=sample_reserva_data)
    
    # Listar reservas
    response = test_client.get('/api/reservas/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert isinstance(data['data'], list)
    assert 'pagination' in data


def test_obtener_reserva_por_id(test_client, sample_reserva_data):
    """Prueba obtener una reserva específica por ID"""
    # Crear reserva
    create_response = test_client.post('/api/reservas/', json=sample_reserva_data)
    reserva_id = create_response.get_json()['data']['id_reserva']
    
    # Obtener por ID
    response = test_client.get(f'/api/reservas/{reserva_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['id_reserva'] == reserva_id
    assert data['data']['numero'] == 1001


def test_crear_reserva_fecha_pasada(test_client, created_cliente, created_mesa):
    """Prueba que no se pueda reservar en fecha pasada"""
    fecha_pasada = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
    data = {
        'numero': 9999,
        'fecha_hora': fecha_pasada,
        'cant_personas': 2,
        'id_cliente': created_cliente.id_cliente,
        'id_mesa': created_mesa.id_mesa
    }
    
    response = test_client.post('/api/reservas/', json=data)
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'futura' in data['message'].lower()


def test_crear_reserva_numero_duplicado(test_client, sample_reserva_data):
    """Prueba que no se pueda crear una reserva con número duplicado"""
    # Crear primera reserva
    test_client.post('/api/reservas/', json=sample_reserva_data)
    
    # Intentar crear otra con el mismo número
    fecha_futura = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%S')
    data_duplicada = sample_reserva_data.copy()
    data_duplicada['fecha_hora'] = fecha_futura
    
    response = test_client.post('/api/reservas/', json=data_duplicada)
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'número' in data['message'].lower() or 'numero' in data['message'].lower()


def test_crear_reserva_mesa_insuficiente(test_client, created_cliente, created_mesa):
    """Prueba que no se pueda reservar más personas de las que caben en la mesa"""
    fecha_futura = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
    data = {
        'numero': 2001,
        'fecha_hora': fecha_futura,
        'cant_personas': 999,  # Más de lo que cabe en la mesa
        'id_cliente': created_cliente.id_cliente,
        'id_mesa': created_mesa.id_mesa
    }
    
    response = test_client.post('/api/reservas/', json=data)
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'capacidad' in data['message'].lower() or 'insuficiente' in data['message'].lower()


def test_cancelar_reserva(test_client, sample_reserva_data):
    """Prueba cancelar una reserva existente"""
    # Crear reserva
    create_response = test_client.post('/api/reservas/', json=sample_reserva_data)
    reserva_id = create_response.get_json()['data']['id_reserva']
    
    # Cancelar reserva
    cancel_data = {'motivo': 'Cliente solicitó cancelación'}
    response = test_client.put(f'/api/reservas/{reserva_id}/cancelar', json=cancel_data)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['cancelado'] is True
    assert data['data']['motivo_cancelacion'] == 'Cliente solicitó cancelación'


def test_actualizar_reserva(test_client, sample_reserva_data):
    """Prueba actualizar una reserva existente"""
    # Crear reserva
    create_response = test_client.post('/api/reservas/', json=sample_reserva_data)
    reserva_id = create_response.get_json()['data']['id_reserva']
    
    # Actualizar reserva
    nueva_fecha = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%dT%H:%M:%S')
    update_data = {
        'fecha_hora': nueva_fecha,
        'cant_personas': 3
    }
    response = test_client.put(f'/api/reservas/{reserva_id}', json=update_data)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['cant_personas'] == 3


def test_filtrar_reservas_por_cliente(test_client, created_cliente, created_mesa):
    """Prueba filtrar reservas por cliente"""
    # Crear dos reservas para el mismo cliente
    fecha1 = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
    fecha2 = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%S')
    
    data1 = {
        'numero': 3001,
        'fecha_hora': fecha1,
        'cant_personas': 2,
        'id_cliente': created_cliente.id_cliente,
        'id_mesa': created_mesa.id_mesa
    }
    data2 = {
        'numero': 3002,
        'fecha_hora': fecha2,
        'cant_personas': 2,
        'id_cliente': created_cliente.id_cliente,
        'id_mesa': created_mesa.id_mesa
    }
    
    test_client.post('/api/reservas/', json=data1)
    test_client.post('/api/reservas/', json=data2)
    
    # Filtrar por cliente
    response = test_client.get(f'/api/reservas/?cliente_id={created_cliente.id_cliente}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert len(data['data']) >= 2


def test_filtrar_reservas_activas(test_client, sample_reserva_data):
    """Prueba filtrar solo reservas activas (no canceladas)"""
    # Crear reserva activa
    test_client.post('/api/reservas/', json=sample_reserva_data)
    
    # Filtrar por activas
    response = test_client.get('/api/reservas/?cancelado=activo')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    # Todas las reservas retornadas deben estar activas
    for reserva in data['data']:
        assert reserva['cancelado'] is False


def test_reserva_no_encontrada(test_client):
    """Prueba obtener una reserva que no existe"""
    response = test_client.get('/api/reservas/99999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['status'] == 'error'


def test_campos_requeridos(test_client):
    """Prueba que se validen los campos requeridos"""
    # Intentar crear reserva sin campos requeridos
    response = test_client.post('/api/reservas/', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'
    # El mensaje puede ser "no input data provided" o mencionar campos requeridos
    assert 'requerido' in data['message'].lower() or 'no input data' in data['message'].lower()

