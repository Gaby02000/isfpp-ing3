import pytest
from models import Mesa, Sector
from tests.utils.test_helpers import assert_response_success, assert_response_error, assert_pagination_structure

class TestMesaModel:
    """Tests unitarios para el modelo Mesa"""
    
    def test_crear_mesa(self, test_db_session, created_sector, sample_mesa_data):
        """Test: Crear una mesa válida"""
        mesa_data = sample_mesa_data.copy()
        mesa_data['id_sector'] = created_sector.id_sector
        
        mesa = Mesa(**mesa_data)
        test_db_session.add(mesa)
        test_db_session.commit()
        
        assert mesa.id_mesa is not None
        assert mesa.numero == sample_mesa_data['numero']
        assert mesa.tipo == sample_mesa_data['tipo']
        assert mesa.cant_comensales == sample_mesa_data['cant_comensales']
        assert mesa.id_sector == created_sector.id_sector
        assert mesa.baja == False
    
    def test_mesa_json(self, test_db_session, created_sector, sample_mesa_data):
        """Test: Método json() del modelo"""
        mesa_data = sample_mesa_data.copy()
        mesa_data['id_sector'] = created_sector.id_sector
        
        mesa = Mesa(**mesa_data)
        test_db_session.add(mesa)
        test_db_session.commit()
        
        json_data = mesa.json()
        assert json_data['id_mesa'] == mesa.id_mesa
        assert json_data['numero'] == mesa.numero
        assert json_data['tipo'] == mesa.tipo
        assert json_data['cant_comensales'] == mesa.cant_comensales
        assert json_data['id_sector'] == mesa.id_sector
        assert json_data['baja'] == False
    
    def test_mesa_numero_unico(self, test_db_session, created_sector, sample_mesa_data):
        """Test: Validar que el número de mesa sea único"""
        mesa_data = sample_mesa_data.copy()
        mesa_data['id_sector'] = created_sector.id_sector
        
        mesa1 = Mesa(**mesa_data)
        test_db_session.add(mesa1)
        test_db_session.commit()
        
        # Intentar crear otra con el mismo número
        mesa2 = Mesa(**mesa_data)
        test_db_session.add(mesa2)
        
        with pytest.raises(Exception):
            test_db_session.commit()

class TestMesaRoutes:
    """Tests de integración para las rutas de Mesa"""
    
    def test_listar_mesas_vacio(self, test_client):
        """Test: Listar mesas cuando no hay ninguna"""
        response = test_client.get('/api/mesas/')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data'] == []
        assert_pagination_structure(data)
    
    def test_crear_mesa_exitosa(self, test_client, created_sector, sample_mesa_data):
        """Test: Crear una mesa exitosamente"""
        mesa_data = sample_mesa_data.copy()
        mesa_data['id_sector'] = created_sector.id_sector
        
        response = test_client.post('/api/mesas/', json=mesa_data)
        assert response.status_code == 201
        data = assert_response_success(response, 201)
        assert data['data']['numero'] == sample_mesa_data['numero']
        assert data['data']['tipo'] == sample_mesa_data['tipo']
        assert data['data']['cant_comensales'] == sample_mesa_data['cant_comensales']
    
    def test_crear_mesa_sin_datos(self, test_client):
        """Test: Intentar crear mesa sin datos"""
        response = test_client.post('/api/mesas/', json={})
        assert response.status_code == 400
        assert_response_error(response, 400)
    
    def test_crear_mesa_campos_faltantes(self, test_client, created_sector):
        """Test: Intentar crear mesa con campos faltantes"""
        # Sin número
        response = test_client.post('/api/mesas/', json={
            'tipo': 'Interior',
            'cant_comensales': 4,
            'id_sector': created_sector.id_sector
        })
        assert response.status_code == 400
        
        # Sin tipo
        response = test_client.post('/api/mesas/', json={
            'numero': 1,
            'cant_comensales': 4,
            'id_sector': created_sector.id_sector
        })
        assert response.status_code == 400
        
        # Sin cant_comensales
        response = test_client.post('/api/mesas/', json={
            'numero': 1,
            'tipo': 'Interior',
            'id_sector': created_sector.id_sector
        })
        assert response.status_code == 400
    
    def test_crear_mesa_sector_inexistente(self, test_client, sample_mesa_data):
        """Test: Intentar crear mesa con sector inexistente"""
        mesa_data = sample_mesa_data.copy()
        mesa_data['id_sector'] = 99999
        
        response = test_client.post('/api/mesas/', json=mesa_data)
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'sector' in data['message'].lower()
    
    def test_crear_mesa_sector_dado_baja(self, test_client, test_db_session, sample_mesa_data):
        """Test: Intentar crear mesa con sector dado de baja"""
        sector = Sector(numero=99)
        test_db_session.add(sector)
        test_db_session.commit()
        sector.baja = True
        test_db_session.commit()
        
        mesa_data = sample_mesa_data.copy()
        mesa_data['id_sector'] = sector.id_sector
        
        response = test_client.post('/api/mesas/', json=mesa_data)
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'baja' in data['message'].lower()
    
    def test_crear_mesa_numero_duplicado(self, test_client, created_sector, sample_mesa_data):
        """Test: Intentar crear mesa con número duplicado"""
        mesa_data = sample_mesa_data.copy()
        mesa_data['id_sector'] = created_sector.id_sector
        
        # Crear primera mesa
        test_client.post('/api/mesas/', json=mesa_data)
        
        # Intentar crear otra con el mismo número
        response = test_client.post('/api/mesas/', json=mesa_data)
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'Ya existe' in data['message'] or 'número' in data['message'].lower()
    
    def test_crear_mesa_cant_comensales_invalida(self, test_client, created_sector, sample_mesa_data):
        """Test: Intentar crear mesa con cantidad de comensales inválida"""
        mesa_data = sample_mesa_data.copy()
        mesa_data['id_sector'] = created_sector.id_sector
        mesa_data['cant_comensales'] = 0
        
        response = test_client.post('/api/mesas/', json=mesa_data)
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'comensales' in data['message'].lower() or 'positivo' in data['message'].lower()
    
    def test_obtener_mesa_existente(self, test_client, created_mesa):
        """Test: Obtener una mesa por ID"""
        response = test_client.get(f'/api/mesas/{created_mesa.id_mesa}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['id_mesa'] == created_mesa.id_mesa
    
    def test_obtener_mesa_inexistente(self, test_client):
        """Test: Obtener una mesa que no existe"""
        response = test_client.get('/api/mesas/99999')
        assert response.status_code == 404
        assert_response_error(response, 404)
    
    def test_listar_mesas_disponibles(self, test_client, created_mesa):
        """Test: Listar mesas disponibles"""
        response = test_client.get('/api/mesas/disponibles')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
        assert all(m['baja'] == False for m in data['data'])
    
    def test_listar_mesas_disponibles_filtro_comensales(self, test_client, created_mesa):
        """Test: Listar mesas disponibles filtradas por cantidad de comensales"""
        response = test_client.get('/api/mesas/disponibles?cant_comensales=4')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(m['cant_comensales'] >= 4 for m in data['data'])
    
    def test_listar_tipos_mesas(self, test_client, created_mesa):
        """Test: Listar tipos únicos de mesas"""
        response = test_client.get('/api/mesas/tipos')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert isinstance(data['data'], list)
        assert created_mesa.tipo in data['data']
    
    def test_modificar_mesa(self, test_client, created_mesa):
        """Test: Modificar una mesa existente"""
        nuevos_datos = {'tipo': 'Exterior', 'cant_comensales': 6}
        response = test_client.put(
            f'/api/mesas/{created_mesa.id_mesa}',
            json=nuevos_datos
        )
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['tipo'] == 'Exterior'
        assert data['data']['cant_comensales'] == 6
    
    def test_modificar_mesa_numero_duplicado(self, test_client, created_sector, created_mesa):
        """Test: Intentar modificar número de mesa a uno que ya existe"""
        # Crear otra mesa
        mesa2_data = {
            'numero': 2,
            'tipo': 'Interior',
            'cant_comensales': 4,
            'id_sector': created_sector.id_sector
        }
        test_client.post('/api/mesas/', json=mesa2_data)
        
        # Intentar cambiar número de mesa1 al de mesa2
        response = test_client.put(
            f'/api/mesas/{created_mesa.id_mesa}',
            json={'numero': 2}
        )
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'Ya existe' in data['message'] or 'número' in data['message'].lower()
    
    def test_modificar_mesa_dada_baja(self, test_client, created_mesa):
        """Test: Intentar modificar una mesa dada de baja"""
        # Dar de baja
        test_client.delete(f'/api/mesas/{created_mesa.id_mesa}')
        
        # Intentar modificar
        response = test_client.put(
            f'/api/mesas/{created_mesa.id_mesa}',
            json={'tipo': 'Nuevo'}
        )
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'baja' in data['message'].lower()
    
    def test_modificar_mesa_sector_invalido(self, test_client, created_mesa):
        """Test: Intentar modificar mesa con sector inexistente"""
        response = test_client.put(
            f'/api/mesas/{created_mesa.id_mesa}',
            json={'id_sector': 99999}
        )
        assert response.status_code == 400
        assert_response_error(response, 400)
    
    def test_eliminar_mesa(self, test_client, created_mesa):
        """Test: Dar de baja una mesa"""
        response = test_client.delete(f'/api/mesas/{created_mesa.id_mesa}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['baja'] == True
    
    def test_eliminar_mesa_inexistente(self, test_client):
        """Test: Intentar dar de baja una mesa que no existe"""
        response = test_client.delete('/api/mesas/99999')
        assert response.status_code == 404
        assert_response_error(response, 404)
    
    def test_eliminar_mesa_ya_dada_baja(self, test_client, created_mesa):
        """Test: Intentar dar de baja una mesa ya dada de baja"""
        # Dar de baja primera vez
        test_client.delete(f'/api/mesas/{created_mesa.id_mesa}')
        
        # Intentar dar de baja segunda vez
        response = test_client.delete(f'/api/mesas/{created_mesa.id_mesa}')
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'ya está dada de baja' in data['message'].lower()
    
    def test_listar_mesas_filtros(self, test_client, created_mesa, created_sector):
        """Test: Listar mesas con filtros"""
        # Filtrar por sector
        response = test_client.get(f'/api/mesas/?sector_id={created_sector.id_sector}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
        assert all(m['id_sector'] == created_sector.id_sector for m in data['data'])
        
        # Filtrar por tipo
        response = test_client.get(f'/api/mesas/?tipo={created_mesa.tipo}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
        assert all(m['tipo'] == created_mesa.tipo for m in data['data'])
    
    def test_listar_mesas_filtro_estado(self, test_client, created_mesa):
        """Test: Listar mesas filtradas por estado"""
        # Filtrar solo activas
        response = test_client.get('/api/mesas/?estado=activa')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(m['baja'] == False for m in data['data'])
        
        # Dar de baja la mesa
        test_client.delete(f'/api/mesas/{created_mesa.id_mesa}')
        
        # Filtrar solo dadas de baja
        response = test_client.get('/api/mesas/?estado=baja')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(m['baja'] == True for m in data['data'])
    
    def test_listar_mesas_paginacion(self, test_client, created_sector, sample_mesa_data):
        """Test: Listar mesas con paginación"""
        # Crear varias mesas
        for i in range(15):
            mesa_data = sample_mesa_data.copy()
            mesa_data['numero'] = i + 1
            mesa_data['id_sector'] = created_sector.id_sector
            test_client.post('/api/mesas/', json=mesa_data)
        
        # Obtener primera página
        response = test_client.get('/api/mesas/?page=1&per_page=10')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) == 10
        assert data['pagination']['has_next'] == True

