import pytest
from models import Mozo, Sector
from tests.utils.test_helpers import assert_response_success, assert_response_error, assert_pagination_structure

class TestMozoModel:
    """Tests unitarios para el modelo Mozo"""
    
    def test_crear_mozo(self, test_db_session, sample_mozo_data):
        """Test: Crear un mozo válido"""
        mozo = Mozo(**sample_mozo_data)
        test_db_session.add(mozo)
        test_db_session.commit()
        
        assert mozo.id is not None
        assert mozo.documento == sample_mozo_data['documento']
        assert mozo.nombre_apellido == sample_mozo_data['nombre_apellido']
        assert mozo.baja == False
    
    def test_crear_mozo_con_sector(self, test_db_session, created_sector, sample_mozo_data):
        """Test: Crear un mozo con sector"""
        mozo_data = sample_mozo_data.copy()
        mozo_data['id_sector'] = created_sector.id_sector
        
        mozo = Mozo(**mozo_data)
        test_db_session.add(mozo)
        test_db_session.commit()
        
        assert mozo.id_sector == created_sector.id_sector
        assert mozo.sector is not None
    
    def test_mozo_json(self, test_db_session, sample_mozo_data):
        """Test: Método json() del modelo"""
        mozo = Mozo(**sample_mozo_data)
        test_db_session.add(mozo)
        test_db_session.commit()
        
        json_data = mozo.json()
        assert json_data['id'] == mozo.id
        assert json_data['documento'] == mozo.documento
        assert json_data['nombre_apellido'] == mozo.nombre_apellido
        assert json_data['baja'] == False
    
    def test_mozo_documento_unico(self, test_db_session, sample_mozo_data):
        """Test: Validar que el documento sea único"""
        mozo1 = Mozo(**sample_mozo_data)
        test_db_session.add(mozo1)
        test_db_session.commit()
        
        # Intentar crear otro con el mismo documento
        mozo2 = Mozo(**sample_mozo_data)
        test_db_session.add(mozo2)
        
        with pytest.raises(Exception):
            test_db_session.commit()

class TestMozoRoutes:
    """Tests de integración para las rutas de Mozo"""
    
    def test_listar_mozos_vacio(self, test_client):
        """Test: Listar mozos cuando no hay ninguno"""
        response = test_client.get('/api/mozos/')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data'] == []
        assert_pagination_structure(data)
    
    def test_crear_mozo_exitoso(self, test_client, sample_mozo_data):
        """Test: Crear un mozo exitosamente"""
        response = test_client.post('/api/mozos/', json=sample_mozo_data)
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['documento'] == sample_mozo_data['documento']
        assert data['data']['nombre_apellido'] == sample_mozo_data['nombre_apellido']
        assert data['data']['baja'] == False
    
    def test_crear_mozo_con_sector(self, test_client, created_sector, sample_mozo_data):
        """Test: Crear un mozo con sector"""
        mozo_data = sample_mozo_data.copy()
        mozo_data['id_sector'] = created_sector.id_sector
        
        response = test_client.post('/api/mozos/', json=mozo_data)
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['id_sector'] == created_sector.id_sector
    
    def test_crear_mozo_sin_datos(self, test_client):
        """Test: Intentar crear mozo sin datos"""
        response = test_client.post('/api/mozos/', json={})
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'requerido' in data['message'].lower()
    
    def test_crear_mozo_campos_faltantes(self, test_client, sample_mozo_data):
        """Test: Intentar crear mozo con campos faltantes"""
        # Sin documento
        datos_incompletos = sample_mozo_data.copy()
        del datos_incompletos['documento']
        response = test_client.post('/api/mozos/', json=datos_incompletos)
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'documento' in data['message'].lower()
        
        # Sin nombre_apellido
        datos_incompletos = sample_mozo_data.copy()
        del datos_incompletos['nombre_apellido']
        response = test_client.post('/api/mozos/', json=datos_incompletos)
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'nombre_apellido' in data['message'].lower()
    
    def test_crear_mozo_sector_inexistente(self, test_client, sample_mozo_data):
        """Test: Intentar crear mozo con sector inexistente"""
        mozo_data = sample_mozo_data.copy()
        mozo_data['id_sector'] = 99999
        
        response = test_client.post('/api/mozos/', json=mozo_data)
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'sector' in data['message'].lower()
    
    def test_crear_mozo_documento_duplicado(self, test_client, sample_mozo_data):
        """Test: Intentar crear mozo con documento duplicado"""
        # Crear primer mozo
        test_client.post('/api/mozos/', json=sample_mozo_data)
        
        # Intentar crear otro con el mismo documento
        response = test_client.post('/api/mozos/', json=sample_mozo_data)
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'Ya existe' in data['message'] or 'documento' in data['message'].lower()
    
    def test_obtener_mozo_existente(self, test_client, created_mozo):
        """Test: Obtener un mozo por ID"""
        response = test_client.get(f'/api/mozos/{created_mozo.id}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['id'] == created_mozo.id
    
    def test_obtener_mozo_inexistente(self, test_client):
        """Test: Obtener un mozo que no existe"""
        response = test_client.get('/api/mozos/99999')
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'no encontrado' in data['message'].lower()
    
    def test_obtener_mozo_dado_baja(self, test_client, test_db_session, sample_mozo_data):
        """Test: Intentar obtener un mozo dado de baja"""
        mozo = Mozo(**sample_mozo_data)
        test_db_session.add(mozo)
        test_db_session.commit()
        mozo.baja = True
        test_db_session.commit()
        
        response = test_client.get(f'/api/mozos/{mozo.id}')
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'no encontrado' in data['message'].lower()
    
    def test_modificar_mozo(self, test_client, created_mozo):
        """Test: Modificar un mozo existente"""
        nuevos_datos = {'nombre_apellido': 'Pedro González', 'telefono': '1111111111'}
        response = test_client.put(
            f'/api/mozos/{created_mozo.id}',
            json=nuevos_datos
        )
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['nombre_apellido'] == 'Pedro González'
        assert data['data']['telefono'] == '1111111111'
    
    def test_modificar_mozo_documento_duplicado(self, test_client, sample_mozo_data):
        """Test: Intentar modificar documento a uno que ya existe"""
        # Crear dos mozos
        mozo1 = sample_mozo_data.copy()
        test_client.post('/api/mozos/', json=mozo1)
        
        mozo2 = sample_mozo_data.copy()
        mozo2['documento'] = '88888888'
        create_response = test_client.post('/api/mozos/', json=mozo2)
        mozo2_id = create_response.get_json()['data']['id']
        
        # Intentar cambiar documento del mozo2 al del mozo1
        response = test_client.put(
            f'/api/mozos/{mozo2_id}',
            json={'documento': mozo1['documento']}
        )
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'Ya existe' in data['message'] or 'documento' in data['message'].lower()
    
    def test_modificar_mozo_sector(self, test_client, test_db_session, created_mozo, created_sector):
        """Test: Modificar el sector de un mozo"""
        # Crear nuevo sector
        nuevo_sector = Sector(numero=99)
        test_db_session.add(nuevo_sector)
        test_db_session.commit()
        
        response = test_client.put(
            f'/api/mozos/{created_mozo.id}',
            json={'id_sector': nuevo_sector.id_sector}
        )
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['id_sector'] == nuevo_sector.id_sector
    
    def test_modificar_mozo_quitar_sector(self, test_client, created_mozo):
        """Test: Quitar el sector de un mozo (asignar None)"""
        response = test_client.put(
            f'/api/mozos/{created_mozo.id}',
            json={'id_sector': None}
        )
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['id_sector'] is None
    
    def test_modificar_mozo_inexistente(self, test_client):
        """Test: Modificar un mozo que no existe"""
        response = test_client.put(
            '/api/mozos/99999',
            json={'nombre_apellido': 'Nuevo'}
        )
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'no encontrado' in data['message'].lower()
    
    def test_eliminar_mozo(self, test_client, created_mozo):
        """Test: Dar de baja un mozo"""
        response = test_client.delete(f'/api/mozos/{created_mozo.id}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['baja'] == True
    
    def test_eliminar_mozo_inexistente(self, test_client):
        """Test: Intentar dar de baja un mozo que no existe"""
        response = test_client.delete('/api/mozos/99999')
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'no encontrado' in data['message'].lower()
    
    def test_eliminar_mozo_ya_dado_baja(self, test_client, created_mozo):
        """Test: Intentar dar de baja un mozo ya dado de baja"""
        # Dar de baja primera vez
        test_client.delete(f'/api/mozos/{created_mozo.id}')
        
        # Intentar dar de baja segunda vez
        response = test_client.delete(f'/api/mozos/{created_mozo.id}')
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'ya dado de baja' in data['message'].lower()
    
    def test_listar_mozos_filtros(self, test_client, created_mozo, created_sector):
        """Test: Listar mozos con filtros"""
        # Filtrar por sector
        response = test_client.get(f'/api/mozos/?sector_id={created_sector.id_sector}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
        assert all(m['id_sector'] == created_sector.id_sector for m in data['data'])
        
        # Filtrar solo activos
        response = test_client.get('/api/mozos/?activos=true')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(m['baja'] == False for m in data['data'])
        
        # Filtrar solo dados de baja
        test_client.delete(f'/api/mozos/{created_mozo.id}')
        response = test_client.get('/api/mozos/?activos=false')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(m['baja'] == True for m in data['data'])
    
    def test_listar_mozos_paginacion(self, test_client, sample_mozo_data):
        """Test: Listar mozos con paginación"""
        # Crear varios mozos
        for i in range(15):
            mozo_data = sample_mozo_data.copy()
            mozo_data['documento'] = f'1234567{i:02d}'
            mozo_data['nombre_apellido'] = f'Mozo {i}'
            test_client.post('/api/mozos/', json=mozo_data)
        
        # Obtener primera página
        response = test_client.get('/api/mozos/?page=1&per_page=10')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) == 10
        assert data['pagination']['has_next'] == True

