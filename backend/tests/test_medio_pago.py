import pytest
from models import MedioPago
from tests.utils.test_helpers import assert_response_success, assert_response_error, assert_pagination_structure

class TestMedioPagoModel:
    """Tests unitarios para el modelo MedioPago"""
    
    def test_crear_medio_pago(self, test_db_session, sample_medio_pago_data):
        """Test: Crear un medio de pago válido"""
        medio_pago = MedioPago(**sample_medio_pago_data)
        test_db_session.add(medio_pago)
        test_db_session.commit()
        
        assert medio_pago.id_medio_pago is not None
        assert medio_pago.nombre == sample_medio_pago_data['nombre']
        assert medio_pago.descripcion == sample_medio_pago_data['descripcion']
        assert medio_pago.baja == False
    
    def test_medio_pago_json(self, test_db_session, sample_medio_pago_data):
        """Test: Método json() del modelo"""
        medio_pago = MedioPago(**sample_medio_pago_data)
        test_db_session.add(medio_pago)
        test_db_session.commit()
        
        json_data = medio_pago.json()
        assert json_data['id_medio_pago'] == medio_pago.id_medio_pago
        assert json_data['nombre'] == medio_pago.nombre
        assert json_data['descripcion'] == medio_pago.descripcion
        assert json_data['baja'] == False
    
    def test_medio_pago_nombre_unico(self, test_db_session, sample_medio_pago_data):
        """Test: Validar que el nombre de medio de pago sea único"""
        medio_pago1 = MedioPago(**sample_medio_pago_data)
        test_db_session.add(medio_pago1)
        test_db_session.commit()
        
        # Intentar crear otro con el mismo nombre
        medio_pago2 = MedioPago(**sample_medio_pago_data)
        test_db_session.add(medio_pago2)
        
        with pytest.raises(Exception):
            test_db_session.commit()
    
    def test_medio_pago_sin_descripcion(self, test_db_session):
        """Test: Crear medio de pago sin descripción (opcional)"""
        medio_pago = MedioPago(nombre='Tarjeta')
        test_db_session.add(medio_pago)
        test_db_session.commit()
        
        assert medio_pago.descripcion is None

class TestMedioPagoRoutes:
    """Tests de integración para las rutas de MedioPago"""
    
    def test_listar_medio_pagos_vacio(self, test_client):
        """Test: Listar medios de pago cuando no hay ninguno"""
        response = test_client.get('/api/medio-pagos/')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data'] == []
        assert_pagination_structure(data)
    
    def test_crear_medio_pago_exitoso(self, test_client, sample_medio_pago_data):
        """Test: Crear un medio de pago exitosamente"""
        response = test_client.post('/api/medio-pagos/', json=sample_medio_pago_data)
        assert response.status_code == 201
        data = assert_response_success(response, 201)
        assert data['data']['nombre'] == sample_medio_pago_data['nombre']
        assert data['data']['descripcion'] == sample_medio_pago_data['descripcion']
        assert data['data']['baja'] == False
    
    def test_crear_medio_pago_sin_descripcion(self, test_client):
        """Test: Crear medio de pago sin descripción"""
        medio_pago_data = {'nombre': 'Tarjeta de Débito'}
        response = test_client.post('/api/medio-pagos/', json=medio_pago_data)
        assert response.status_code == 201
        data = assert_response_success(response, 201)
        assert data['data']['nombre'] == 'Tarjeta de Débito'
        assert data['data']['descripcion'] is None
    
    def test_crear_medio_pago_sin_datos(self, test_client):
        """Test: Intentar crear medio de pago sin datos"""
        response = test_client.post('/api/medio-pagos/', json={})
        assert response.status_code == 400
        assert_response_error(response, 400)
    
    def test_crear_medio_pago_sin_nombre(self, test_client):
        """Test: Intentar crear medio de pago sin nombre"""
        response = test_client.post('/api/medio-pagos/', json={'descripcion': 'Descripción'})
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'nombre' in data['message'].lower() or 'requerido' in data['message'].lower()
    
    def test_crear_medio_pago_nombre_duplicado(self, test_client, sample_medio_pago_data):
        """Test: Intentar crear medio de pago con nombre duplicado"""
        # Crear primer medio de pago
        test_client.post('/api/medio-pagos/', json=sample_medio_pago_data)
        
        # Intentar crear otro con el mismo nombre
        response = test_client.post('/api/medio-pagos/', json=sample_medio_pago_data)
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'Ya existe' in data['message'] or 'nombre' in data['message'].lower()
    
    def test_obtener_medio_pago_existente(self, test_client, created_medio_pago):
        """Test: Obtener un medio de pago por ID"""
        response = test_client.get(f'/api/medio-pagos/{created_medio_pago.id_medio_pago}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['id_medio_pago'] == created_medio_pago.id_medio_pago
        assert data['data']['nombre'] == created_medio_pago.nombre
    
    def test_obtener_medio_pago_inexistente(self, test_client):
        """Test: Obtener un medio de pago que no existe"""
        response = test_client.get('/api/medio-pagos/99999')
        assert response.status_code == 404
        assert_response_error(response, 404)
    
    def test_modificar_medio_pago(self, test_client, created_medio_pago):
        """Test: Modificar un medio de pago existente"""
        nuevos_datos = {
            'nombre': 'Efectivo Actualizado',
            'descripcion': 'Nueva descripción'
        }
        response = test_client.put(
            f'/api/medio-pagos/{created_medio_pago.id_medio_pago}',
            json=nuevos_datos
        )
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['nombre'] == 'Efectivo Actualizado'
        assert data['data']['descripcion'] == 'Nueva descripción'
    
    def test_modificar_medio_pago_solo_nombre(self, test_client, created_medio_pago):
        """Test: Modificar solo el nombre de un medio de pago"""
        response = test_client.put(
            f'/api/medio-pagos/{created_medio_pago.id_medio_pago}',
            json={'nombre': 'Nuevo Nombre'}
        )
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['nombre'] == 'Nuevo Nombre'
        # Verificar que la descripción no cambió
        assert data['data']['descripcion'] == created_medio_pago.descripcion
    
    def test_modificar_medio_pago_solo_descripcion(self, test_client, created_medio_pago):
        """Test: Modificar solo la descripción de un medio de pago"""
        response = test_client.put(
            f'/api/medio-pagos/{created_medio_pago.id_medio_pago}',
            json={'descripcion': 'Nueva descripción'}
        )
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['descripcion'] == 'Nueva descripción'
        # Verificar que el nombre no cambió
        assert data['data']['nombre'] == created_medio_pago.nombre
    
    def test_modificar_medio_pago_nombre_duplicado(self, test_client, sample_medio_pago_data):
        """Test: Intentar modificar nombre a uno que ya existe"""
        # Crear dos medios de pago
        medio_pago1 = sample_medio_pago_data.copy()
        test_client.post('/api/medio-pagos/', json=medio_pago1)
        
        medio_pago2 = sample_medio_pago_data.copy()
        medio_pago2['nombre'] = 'Tarjeta'
        create_response = test_client.post('/api/medio-pagos/', json=medio_pago2)
        medio_pago2_id = create_response.get_json()['data']['id_medio_pago']
        
        # Intentar cambiar nombre del medio_pago2 al del medio_pago1
        response = test_client.put(
            f'/api/medio-pagos/{medio_pago2_id}',
            json={'nombre': medio_pago1['nombre']}
        )
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'Ya existe' in data['message'] or 'nombre' in data['message'].lower()
    
    def test_modificar_medio_pago_dado_baja(self, test_client, created_medio_pago):
        """Test: Intentar modificar un medio de pago dado de baja"""
        # Dar de baja
        test_client.delete(f'/api/medio-pagos/{created_medio_pago.id_medio_pago}')
        
        # Intentar modificar
        response = test_client.put(
            f'/api/medio-pagos/{created_medio_pago.id_medio_pago}',
            json={'nombre': 'Nuevo'}
        )
        assert response.status_code == 404
        data = assert_response_error(response, 404)
        assert 'baja' in data['message'].lower()
    
    def test_modificar_medio_pago_inexistente(self, test_client):
        """Test: Modificar un medio de pago que no existe"""
        response = test_client.put(
            '/api/medio-pagos/99999',
            json={'nombre': 'Nuevo'}
        )
        assert response.status_code == 400
        assert_response_error(response, 400)
    
    def test_eliminar_medio_pago(self, test_client, created_medio_pago):
        """Test: Dar de baja un medio de pago"""
        response = test_client.delete(f'/api/medio-pagos/{created_medio_pago.id_medio_pago}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['baja'] == True
    
    def test_eliminar_medio_pago_inexistente(self, test_client):
        """Test: Intentar dar de baja un medio de pago que no existe"""
        response = test_client.delete('/api/medio-pagos/99999')
        assert response.status_code == 404
        assert_response_error(response, 404)
    
    def test_eliminar_medio_pago_ya_dado_baja(self, test_client, created_medio_pago):
        """Test: Intentar dar de baja un medio de pago ya dado de baja"""
        # Dar de baja primera vez
        test_client.delete(f'/api/medio-pagos/{created_medio_pago.id_medio_pago}')
        
        # Intentar dar de baja segunda vez
        response = test_client.delete(f'/api/medio-pagos/{created_medio_pago.id_medio_pago}')
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'ya está dado de baja' in data['message'].lower()
    
    def test_listar_medio_pagos_filtros(self, test_client, created_medio_pago):
        """Test: Listar medios de pago con filtros"""
        # Filtrar por nombre
        response = test_client.get(f'/api/medio-pagos/?nombre={created_medio_pago.nombre}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
        assert all(m['nombre'] == created_medio_pago.nombre for m in data['data'])
        
        # Filtrar solo activas
        response = test_client.get('/api/medio-pagos/?estado=activa')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(m['baja'] == False for m in data['data'])
        
        # Dar de baja el medio de pago
        test_client.delete(f'/api/medio-pagos/{created_medio_pago.id_medio_pago}')
        
        # Filtrar solo dadas de baja
        response = test_client.get('/api/medio-pagos/?estado=baja')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(m['baja'] == True for m in data['data'])
    
    def test_listar_medio_pagos_ordenamiento(self, test_client, sample_medio_pago_data):
        """Test: Verificar que los medios de pago se ordenen por nombre"""
        # Crear medios de pago con diferentes nombres
        nombres = ['Zapata', 'Alvarez', 'Benítez']
        for nombre in nombres:
            medio_pago_data = sample_medio_pago_data.copy()
            medio_pago_data['nombre'] = nombre
            test_client.post('/api/medio-pagos/', json=medio_pago_data)
        
        response = test_client.get('/api/medio-pagos/')
        assert response.status_code == 200
        data = assert_response_success(response)
        medios_nombres = [m['nombre'] for m in data['data'] if m['nombre'] in nombres]
        assert medios_nombres == sorted(medios_nombres)
    
    def test_listar_medio_pagos_paginacion(self, test_client, sample_medio_pago_data):
        """Test: Listar medios de pago con paginación"""
        # Crear varios medios de pago
        for i in range(15):
            medio_pago_data = sample_medio_pago_data.copy()
            medio_pago_data['nombre'] = f'Medio {i}'
            test_client.post('/api/medio-pagos/', json=medio_pago_data)
        
        # Obtener primera página
        response = test_client.get('/api/medio-pagos/?page=1&per_page=10')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) == 10
        assert data['pagination']['has_next'] == True

