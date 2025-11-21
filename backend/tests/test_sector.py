import pytest
from models import Sector, Mesa
from tests.utils.test_helpers import assert_response_success, assert_response_error, assert_pagination_structure

class TestSectorModel:
    """Tests unitarios para el modelo Sector"""
    
    def test_crear_sector(self, test_db_session, sample_sector_data):
        """Test: Crear un sector válido"""
        sector = Sector(**sample_sector_data)
        test_db_session.add(sector)
        test_db_session.commit()
        
        assert sector.id_sector is not None
        assert sector.numero == sample_sector_data['numero']
        assert sector.baja == False
    
    def test_sector_json(self, test_db_session, sample_sector_data):
        """Test: Método json() del modelo"""
        sector = Sector(**sample_sector_data)
        test_db_session.add(sector)
        test_db_session.commit()
        
        json_data = sector.json()
        assert json_data['id_sector'] == sector.id_sector
        assert json_data['numero'] == sector.numero
        assert json_data['baja'] == False
    
    def test_sector_numero_unico(self, test_db_session, sample_sector_data):
        """Test: Validar que el número de sector sea único"""
        sector1 = Sector(**sample_sector_data)
        test_db_session.add(sector1)
        test_db_session.commit()
        
        # Intentar crear otro con el mismo número
        sector2 = Sector(**sample_sector_data)
        test_db_session.add(sector2)
        
        with pytest.raises(Exception):
            test_db_session.commit()

class TestSectorRoutes:
    """Tests de integración para las rutas de Sector"""
    
    def test_listar_sectores_vacio(self, test_client):
        """Test: Listar sectores cuando no hay ninguno"""
        response = test_client.get('/api/sectores/')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data'] == []
        assert_pagination_structure(data)
    
    def test_crear_sector_exitoso(self, test_client, sample_sector_data):
        """Test: Crear un sector exitosamente"""
        response = test_client.post('/api/sectores/', json=sample_sector_data)
        assert response.status_code == 201
        data = assert_response_success(response, 201)
        assert data['data']['numero'] == sample_sector_data['numero']
        assert data['data']['baja'] == False
    
    def test_crear_sector_sin_datos(self, test_client):
        """Test: Intentar crear sector sin datos"""
        response = test_client.post('/api/sectores/', json={})
        assert response.status_code == 400
        assert_response_error(response, 400)
    
    def test_crear_sector_numero_duplicado(self, test_client, sample_sector_data):
        """Test: Intentar crear sector con número duplicado"""
        # Crear primer sector
        test_client.post('/api/sectores/', json=sample_sector_data)
        
        # Intentar crear otro con el mismo número
        response = test_client.post('/api/sectores/', json=sample_sector_data)
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'Ya existe' in data['message'] or 'número' in data['message'].lower()
    
    def test_obtener_sector_existente(self, test_client, created_sector):
        """Test: Obtener un sector por ID"""
        response = test_client.get(f'/api/sectores/{created_sector.id_sector}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['id_sector'] == created_sector.id_sector
        assert 'cantidad_mesas' in data['data']
    
    def test_obtener_sector_inexistente(self, test_client):
        """Test: Obtener un sector que no existe"""
        response = test_client.get('/api/sectores/99999')
        assert response.status_code == 404
        assert_response_error(response, 404)
    
    def test_listar_todos_sectores(self, test_client, created_sector):
        """Test: Listar todos los sectores sin paginación"""
        response = test_client.get('/api/sectores/todos')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
        assert all('cantidad_mesas' in s for s in data['data'])
    
    def test_modificar_sector(self, test_client, created_sector):
        """Test: Modificar un sector existente"""
        nuevos_datos = {'numero': 99}
        response = test_client.put(
            f'/api/sectores/{created_sector.id_sector}',
            json=nuevos_datos
        )
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['numero'] == 99
    
    def test_modificar_sector_numero_duplicado(self, test_client, sample_sector_data):
        """Test: Intentar modificar número de sector a uno que ya existe"""
        # Crear dos sectores
        sector1 = sample_sector_data.copy()
        test_client.post('/api/sectores/', json=sector1)
        
        sector2 = sample_sector_data.copy()
        sector2['numero'] = 2
        create_response = test_client.post('/api/sectores/', json=sector2)
        sector2_id = create_response.get_json()['data']['id_sector']
        
        # Intentar cambiar número del sector2 al del sector1
        response = test_client.put(
            f'/api/sectores/{sector2_id}',
            json={'numero': sector1['numero']}
        )
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'Ya existe' in data['message'] or 'número' in data['message'].lower()
    
    def test_modificar_sector_dado_baja(self, test_client, created_sector):
        """Test: Intentar modificar un sector dado de baja"""
        # Dar de baja
        test_client.delete(f'/api/sectores/{created_sector.id_sector}')
        
        # Intentar modificar
        response = test_client.put(
            f'/api/sectores/{created_sector.id_sector}',
            json={'numero': 99}
        )
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'baja' in data['message'].lower()
    
    def test_eliminar_sector(self, test_client, test_db_session, sample_sector_data):
        """Test: Dar de baja un sector sin mesas"""
        # Crear sector sin mesas
        sector_data = sample_sector_data.copy()
        sector_data['numero'] = 99
        create_response = test_client.post('/api/sectores/', json=sector_data)
        sector_id = create_response.get_json()['data']['id_sector']
        
        response = test_client.delete(f'/api/sectores/{sector_id}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['baja'] == True
    
    def test_eliminar_sector_con_mesas(self, test_client, created_sector, created_mesa):
        """Test: Intentar dar de baja un sector con mesas activas"""
        response = test_client.delete(f'/api/sectores/{created_sector.id_sector}')
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'mesa' in data['message'].lower() or 'activa' in data['message'].lower()
    
    def test_eliminar_sector_inexistente(self, test_client):
        """Test: Intentar dar de baja un sector que no existe"""
        response = test_client.delete('/api/sectores/99999')
        assert response.status_code == 404
        assert_response_error(response, 404)
    
    def test_eliminar_sector_ya_dado_baja(self, test_client, test_db_session, sample_sector_data):
        """Test: Intentar dar de baja un sector ya dado de baja"""
        # Crear sector sin mesas
        sector_data = sample_sector_data.copy()
        sector_data['numero'] = 98
        create_response = test_client.post('/api/sectores/', json=sector_data)
        sector_id = create_response.get_json()['data']['id_sector']
        
        # Dar de baja primera vez
        test_client.delete(f'/api/sectores/{sector_id}')
        
        # Intentar dar de baja segunda vez
        response = test_client.delete(f'/api/sectores/{sector_id}')
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'ya está dado de baja' in data['message'].lower()
    
    def test_listar_sectores_filtros(self, test_client, created_sector):
        """Test: Listar sectores con filtros"""
        # Filtrar solo activos
        response = test_client.get('/api/sectores/?estado=activo')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(s['baja'] == False for s in data['data'])
        
        # Dar de baja el sector
        test_client.delete(f'/api/sectores/{created_sector.id_sector}')
        
        # Filtrar solo dados de baja
        response = test_client.get('/api/sectores/?estado=baja')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(s['baja'] == True for s in data['data'])
    
    def test_listar_sectores_paginacion(self, test_client, sample_sector_data):
        """Test: Listar sectores con paginación"""
        # Crear varios sectores
        for i in range(15):
            sector_data = sample_sector_data.copy()
            sector_data['numero'] = i + 10
            test_client.post('/api/sectores/', json=sector_data)
        
        # Obtener primera página
        response = test_client.get('/api/sectores/?page=1&per_page=10')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) == 10
        assert data['pagination']['has_next'] == True
    
    def test_sector_cantidad_mesas(self, test_client, created_sector, created_mesa):
        """Test: Verificar que se muestre la cantidad de mesas en el sector"""
        response = test_client.get(f'/api/sectores/{created_sector.id_sector}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert 'cantidad_mesas' in data['data']
        assert data['data']['cantidad_mesas'] >= 1

