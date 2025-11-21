import pytest
from sqlalchemy.exc import IntegrityError
from models import Cliente
from tests.utils.test_helpers import assert_response_success, assert_response_error, assert_pagination_structure

class TestClienteModel:
    """Tests unitarios para el modelo Cliente"""
    
    def test_crear_cliente(self, test_db_session, sample_cliente_data):
        """Test: Crear un cliente válido"""
        cliente = Cliente(**sample_cliente_data)
        test_db_session.add(cliente)
        test_db_session.commit()
        
        assert cliente.id_cliente is not None
        assert cliente.documento == sample_cliente_data['documento']
        assert cliente.nombre == sample_cliente_data['nombre']
        assert cliente.apellido == sample_cliente_data['apellido']
        assert cliente.num_telefono == sample_cliente_data['num_telefono']
        assert cliente.email == sample_cliente_data['email']
        assert cliente.baja == False
    
    def test_cliente_json(self, test_db_session, sample_cliente_data):
        """Test: Método json() del modelo"""
        cliente = Cliente(**sample_cliente_data)
        test_db_session.add(cliente)
        test_db_session.commit()
        
        json_data = cliente.json()
        assert json_data['id_cliente'] == cliente.id_cliente
        assert json_data['documento'] == cliente.documento
        assert json_data['nombre'] == cliente.nombre
        assert json_data['apellido'] == cliente.apellido
        assert json_data['num_telefono'] == cliente.num_telefono
        assert json_data['email'] == cliente.email
        assert json_data['baja'] == False
    
    def test_cliente_documento_unico(self, test_db_session, sample_cliente_data):
        """Test: Validar que el documento sea único"""
        cliente1 = Cliente(**sample_cliente_data)
        test_db_session.add(cliente1)
        test_db_session.commit()
        
        # Intentar crear otro con el mismo documento
        cliente2 = Cliente(**sample_cliente_data)
        test_db_session.add(cliente2)
        
        with pytest.raises(IntegrityError):
            test_db_session.commit()
    
    def test_cliente_baja_default(self, test_db_session, sample_cliente_data):
        """Test: Verificar que baja sea False por defecto"""
        cliente = Cliente(**sample_cliente_data)
        assert cliente.baja == False

class TestClienteRoutes:
    """Tests de integración para las rutas de Cliente"""
    
    def test_listar_clientes_vacio(self, test_client):
        """Test: Listar clientes cuando no hay ninguno"""
        response = test_client.get('/api/clientes/')
        assert response.status_code == 200
        
        data = assert_response_success(response)
        assert data['data'] == []
        assert_pagination_structure(data)
        assert data['pagination']['total'] == 0
    
    def test_crear_cliente_exitoso(self, test_client, sample_cliente_data):
        """Test: Crear un cliente exitosamente"""
        response = test_client.post(
            '/api/clientes/',
            json=sample_cliente_data
        )
        
        assert response.status_code == 201
        data = assert_response_success(response, 201)
        assert data['data']['documento'] == sample_cliente_data['documento']
        assert data['data']['nombre'] == sample_cliente_data['nombre']
        assert data['data']['baja'] == False
    
    def test_crear_cliente_sin_datos(self, test_client):
        """Test: Intentar crear cliente sin datos"""
        response = test_client.post('/api/clientes/', json={})
        assert response.status_code == 400
        assert_response_error(response, 400)
    
    def test_crear_cliente_campo_faltante(self, test_client, sample_cliente_data):
        """Test: Intentar crear cliente con campos faltantes"""
        datos_incompletos = sample_cliente_data.copy()
        del datos_incompletos['nombre']
        
        response = test_client.post('/api/clientes/', json=datos_incompletos)
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'nombre' in data['message'].lower()
    
    def test_crear_cliente_documento_duplicado(self, test_client, sample_cliente_data):
        """Test: Intentar crear cliente con documento duplicado"""
        # Crear primer cliente
        test_client.post('/api/clientes/', json=sample_cliente_data)
        
        # Intentar crear otro con el mismo documento
        response = test_client.post(
            '/api/clientes/',
            json=sample_cliente_data
        )
        
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'Ya existe' in data['message'] or 'documento' in data['message'].lower()
    
    def test_obtener_cliente_existente(self, test_client, sample_cliente_data):
        """Test: Obtener un cliente por ID"""
        # Crear cliente
        create_response = test_client.post(
            '/api/clientes/',
            json=sample_cliente_data
        )
        cliente_id = create_response.get_json()['data']['id_cliente']
        
        # Obtener cliente
        response = test_client.get(f'/api/clientes/{cliente_id}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['id_cliente'] == cliente_id
        assert data['data']['documento'] == sample_cliente_data['documento']
    
    def test_obtener_cliente_inexistente(self, test_client):
        """Test: Obtener un cliente que no existe"""
        response = test_client.get('/api/clientes/99999')
        assert response.status_code == 404
        assert_response_error(response, 404)
    
    def test_modificar_cliente(self, test_client, sample_cliente_data):
        """Test: Modificar un cliente existente"""
        # Crear cliente
        create_response = test_client.post(
            '/api/clientes/',
            json=sample_cliente_data
        )
        cliente_id = create_response.get_json()['data']['id_cliente']
        
        # Modificar cliente
        nuevos_datos = {'nombre': 'Pedro', 'apellido': 'González'}
        response = test_client.put(
            f'/api/clientes/{cliente_id}',
            json=nuevos_datos
        )
        
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['nombre'] == 'Pedro'
        assert data['data']['apellido'] == 'González'
        # Verificar que otros campos no cambiaron
        assert data['data']['documento'] == sample_cliente_data['documento']
    
    def test_modificar_cliente_inexistente(self, test_client):
        """Test: Modificar un cliente que no existe"""
        response = test_client.put(
            '/api/clientes/99999',
            json={'nombre': 'Nuevo'}
        )
        assert response.status_code == 404
        assert_response_error(response, 404)
    
    def test_modificar_cliente_dado_baja(self, test_client, sample_cliente_data):
        """Test: Intentar modificar un cliente dado de baja"""
        # Crear cliente
        create_response = test_client.post(
            '/api/clientes/',
            json=sample_cliente_data
        )
        cliente_id = create_response.get_json()['data']['id_cliente']
        
        # Dar de baja
        test_client.delete(f'/api/clientes/{cliente_id}')
        
        # Intentar modificar
        response = test_client.put(
            f'/api/clientes/{cliente_id}',
            json={'nombre': 'Nuevo'}
        )
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'baja' in data['message'].lower()
    
    def test_modificar_cliente_documento_duplicado(self, test_client, sample_cliente_data):
        """Test: Intentar modificar documento a uno que ya existe"""
        # Crear dos clientes
        cliente1 = sample_cliente_data.copy()
        test_client.post('/api/clientes/', json=cliente1)
        
        cliente2 = sample_cliente_data.copy()
        cliente2['documento'] = '87654321'
        create_response = test_client.post('/api/clientes/', json=cliente2)
        cliente2_id = create_response.get_json()['data']['id_cliente']
        
        # Intentar cambiar documento del cliente2 al del cliente1
        response = test_client.put(
            f'/api/clientes/{cliente2_id}',
            json={'documento': cliente1['documento']}
        )
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'Ya existe' in data['message'] or 'documento' in data['message'].lower()
    
    def test_eliminar_cliente(self, test_client, sample_cliente_data):
        """Test: Dar de baja un cliente"""
        # Crear cliente
        create_response = test_client.post(
            '/api/clientes/',
            json=sample_cliente_data
        )
        cliente_id = create_response.get_json()['data']['id_cliente']
        
        # Dar de baja
        response = test_client.delete(f'/api/clientes/{cliente_id}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['baja'] == True
    
    def test_eliminar_cliente_inexistente(self, test_client):
        """Test: Intentar dar de baja un cliente que no existe"""
        response = test_client.delete('/api/clientes/99999')
        assert response.status_code == 404
        assert_response_error(response, 404)
    
    def test_eliminar_cliente_ya_dado_baja(self, test_client, sample_cliente_data):
        """Test: Intentar dar de baja un cliente ya dado de baja"""
        # Crear cliente
        create_response = test_client.post(
            '/api/clientes/',
            json=sample_cliente_data
        )
        cliente_id = create_response.get_json()['data']['id_cliente']
        
        # Dar de baja primera vez
        test_client.delete(f'/api/clientes/{cliente_id}')
        
        # Intentar dar de baja segunda vez
        response = test_client.delete(f'/api/clientes/{cliente_id}')
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'ya está dado de baja' in data['message'].lower()
    
    def test_listar_clientes_con_filtros(self, test_client, sample_cliente_data):
        """Test: Listar clientes con filtros"""
        # Crear varios clientes
        cliente1 = sample_cliente_data.copy()
        cliente1['documento'] = '11111111'
        cliente1['nombre'] = 'Juan'
        cliente1['apellido'] = 'Pérez'
        test_client.post('/api/clientes/', json=cliente1)
        
        cliente2 = sample_cliente_data.copy()
        cliente2['documento'] = '22222222'
        cliente2['nombre'] = 'Pedro'
        cliente2['apellido'] = 'García'
        test_client.post('/api/clientes/', json=cliente2)
        
        # Filtrar por nombre
        response = test_client.get('/api/clientes/?nombre=Juan')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
        assert all('Juan' in c['nombre'] for c in data['data'])
        
        # Filtrar por apellido
        response = test_client.get('/api/clientes/?apellido=García')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
        assert all('García' in c['apellido'] for c in data['data'])
        
        # Filtrar por documento
        response = test_client.get('/api/clientes/?documento=11111111')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
        assert data['data'][0]['documento'] == '11111111'
    
    def test_listar_clientes_filtro_estado(self, test_client, sample_cliente_data):
        """Test: Listar clientes filtrados por estado"""
        # Crear cliente activo
        cliente1 = sample_cliente_data.copy()
        cliente1['documento'] = '11111111'
        test_client.post('/api/clientes/', json=cliente1)
        
        # Crear y dar de baja otro cliente
        cliente2 = sample_cliente_data.copy()
        cliente2['documento'] = '22222222'
        create_response = test_client.post('/api/clientes/', json=cliente2)
        cliente2_id = create_response.get_json()['data']['id_cliente']
        test_client.delete(f'/api/clientes/{cliente2_id}')
        
        # Filtrar solo activos
        response = test_client.get('/api/clientes/?estado=activa')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(c['baja'] == False for c in data['data'])
        
        # Filtrar solo dados de baja
        response = test_client.get('/api/clientes/?estado=baja')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(c['baja'] == True for c in data['data'])
    
    def test_listar_clientes_paginacion(self, test_client, sample_cliente_data):
        """Test: Listar clientes con paginación"""
        # Crear varios clientes
        for i in range(15):
            datos = sample_cliente_data.copy()
            datos['documento'] = f'1234567{i:02d}'
            datos['nombre'] = f'Cliente{i}'
            test_client.post('/api/clientes/', json=datos)
        
        # Obtener primera página
        response = test_client.get('/api/clientes/?page=1&per_page=10')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) == 10
        assert data['pagination']['page'] == 1
        assert data['pagination']['per_page'] == 10
        assert data['pagination']['total'] == 15
        assert data['pagination']['has_next'] == True
        assert data['pagination']['has_prev'] == False
        
        # Obtener segunda página
        response = test_client.get('/api/clientes/?page=2&per_page=10')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) == 5
        assert data['pagination']['page'] == 2
        assert data['pagination']['has_next'] == False
        assert data['pagination']['has_prev'] == True
    
    def test_listar_clientes_ordenamiento(self, test_client, sample_cliente_data):
        """Test: Listar clientes con diferentes ordenamientos"""
        # Crear clientes con diferentes apellidos
        clientes = [
            {'apellido': 'Zapata', 'nombre': 'Ana'},
            {'apellido': 'Alvarez', 'nombre': 'Carlos'},
            {'apellido': 'Benítez', 'nombre': 'Beatriz'}
        ]
        
        for cliente_data in clientes:
            datos = sample_cliente_data.copy()
            datos.update(cliente_data)
            datos['documento'] = f'DOC{cliente_data["apellido"]}'
            test_client.post('/api/clientes/', json=datos)
        
        # Ordenar por apellido (default)
        response = test_client.get('/api/clientes/?ordenar_por=apellido')
        assert response.status_code == 200
        data = assert_response_success(response)
        apellidos = [c['apellido'] for c in data['data'] if c['apellido'] in ['Alvarez', 'Benítez', 'Zapata']]
        assert apellidos == sorted(apellidos)
        
        # Ordenar por nombre
        response = test_client.get('/api/clientes/?ordenar_por=nombre')
        assert response.status_code == 200
        data = assert_response_success(response)
        nombres = [c['nombre'] for c in data['data'] if c['nombre'] in ['Ana', 'Beatriz', 'Carlos']]
        assert nombres == sorted(nombres)
    
    def test_listar_clientes_paginacion_invalida(self, test_client):
        """Test: Validar paginación con valores inválidos"""
        # Página negativa
        response = test_client.get('/api/clientes/?page=-1')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['pagination']['page'] == 1
        
        # per_page muy grande
        response = test_client.get('/api/clientes/?per_page=200')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['pagination']['per_page'] == 10
        
        # per_page cero
        response = test_client.get('/api/clientes/?per_page=0')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['pagination']['per_page'] == 10

