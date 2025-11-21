import pytest
from models import Comanda, Mesa, Mozo, Sector
from tests.utils.test_helpers import assert_response_success, assert_response_error, assert_pagination_structure

class TestComandaModel:
    """Tests unitarios para el modelo Comanda"""
    
    def test_crear_comanda(self, test_db_session, created_mozo, created_mesa, sample_comanda_data):
        """Test: Crear una comanda válida"""
        comanda_data = sample_comanda_data.copy()
        comanda_data['id_mozo'] = created_mozo.id
        comanda_data['id_mesa'] = created_mesa.id_mesa
        
        comanda = Comanda(**comanda_data)
        test_db_session.add(comanda)
        test_db_session.commit()
        
        assert comanda.id_comanda is not None
        assert comanda.fecha == sample_comanda_data['fecha']
        assert comanda.id_mozo == created_mozo.id
        assert comanda.id_mesa == created_mesa.id_mesa
        assert comanda.baja == False
    
    def test_comanda_json(self, test_db_session, created_mozo, created_mesa, sample_comanda_data):
        """Test: Método json() del modelo"""
        comanda_data = sample_comanda_data.copy()
        comanda_data['id_mozo'] = created_mozo.id
        comanda_data['id_mesa'] = created_mesa.id_mesa
        
        comanda = Comanda(**comanda_data)
        test_db_session.add(comanda)
        test_db_session.commit()
        
        json_data = comanda.json()
        assert json_data['id_comanda'] == comanda.id_comanda
        assert json_data['fecha'] == comanda.fecha
        assert json_data['id_mozo'] == comanda.id_mozo
        assert json_data['id_mesa'] == comanda.id_mesa
        assert json_data['baja'] == False
    
    def test_comanda_relaciones(self, test_db_session, created_mozo, created_mesa, sample_comanda_data):
        """Test: Verificar relaciones con Mesa y Mozo"""
        comanda_data = sample_comanda_data.copy()
        comanda_data['id_mozo'] = created_mozo.id
        comanda_data['id_mesa'] = created_mesa.id_mesa
        
        comanda = Comanda(**comanda_data)
        test_db_session.add(comanda)
        test_db_session.commit()
        test_db_session.refresh(comanda)
        
        assert comanda.mozo is not None
        assert comanda.mozo.id == created_mozo.id
        assert comanda.mesa is not None
        assert comanda.mesa.id_mesa == created_mesa.id_mesa

class TestComandaRoutes:
    """Tests de integración para las rutas de Comanda"""
    
    def test_listar_comandas_vacio(self, test_client):
        """Test: Listar comandas cuando no hay ninguna"""
        response = test_client.get('/api/comandas/')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data'] == []
        assert_pagination_structure(data)
    
    def test_crear_comanda_exitoso(self, test_client, created_mozo, created_mesa, sample_comanda_data):
        """Test: Crear una comanda exitosamente"""
        comanda_data = sample_comanda_data.copy()
        comanda_data['id_mozo'] = created_mozo.id
        comanda_data['id_mesa'] = created_mesa.id_mesa
        
        response = test_client.post('/api/comandas/', json=comanda_data)
        assert response.status_code == 201
        data = assert_response_success(response, 201)
        assert data['data']['fecha'] == sample_comanda_data['fecha']
        assert data['data']['id_mozo'] == created_mozo.id
        assert data['data']['id_mesa'] == created_mesa.id_mesa
    
    def test_crear_comanda_sin_datos(self, test_client):
        """Test: Intentar crear comanda sin datos"""
        response = test_client.post('/api/comandas/', json={})
        assert response.status_code == 400
        assert_response_error(response, 400)
    
    def test_crear_comanda_campos_faltantes(self, test_client, created_mozo, created_mesa):
        """Test: Intentar crear comanda con campos faltantes"""
        # Sin fecha
        response = test_client.post('/api/comandas/', json={
            'id_mozo': created_mozo.id,
            'id_mesa': created_mesa.id_mesa
        })
        assert response.status_code == 400
        
        # Sin id_mozo
        response = test_client.post('/api/comandas/', json={
            'fecha': '2024-01-15',
            'id_mesa': created_mesa.id_mesa
        })
        assert response.status_code == 400
        
        # Sin id_mesa
        response = test_client.post('/api/comandas/', json={
            'fecha': '2024-01-15',
            'id_mozo': created_mozo.id
        })
        assert response.status_code == 400
    
    def test_crear_comanda_mozo_inexistente(self, test_client, created_mesa, sample_comanda_data):
        """Test: Intentar crear comanda con mozo inexistente"""
        comanda_data = sample_comanda_data.copy()
        comanda_data['id_mozo'] = 99999
        comanda_data['id_mesa'] = created_mesa.id_mesa
        
        response = test_client.post('/api/comandas/', json=comanda_data)
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'mozo' in data['message'].lower()
    
    def test_crear_comanda_mozo_dado_baja(self, test_client, test_db_session, created_mesa, sample_comanda_data):
        """Test: Intentar crear comanda con mozo dado de baja"""
        # Crear mozo y darlo de baja
        sector = Sector(numero=99)
        test_db_session.add(sector)
        test_db_session.commit()
        
        mozo = Mozo(documento='99999999', nombre_apellido='Mozo Baja', id_sector=sector.id_sector)
        test_db_session.add(mozo)
        test_db_session.commit()
        mozo.baja = True
        test_db_session.commit()
        
        comanda_data = sample_comanda_data.copy()
        comanda_data['id_mozo'] = mozo.id
        comanda_data['id_mesa'] = created_mesa.id_mesa
        
        response = test_client.post('/api/comandas/', json=comanda_data)
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'baja' in data['message'].lower()
    
    def test_crear_comanda_mesa_inexistente(self, test_client, created_mozo, sample_comanda_data):
        """Test: Intentar crear comanda con mesa inexistente"""
        comanda_data = sample_comanda_data.copy()
        comanda_data['id_mozo'] = created_mozo.id
        comanda_data['id_mesa'] = 99999
        
        response = test_client.post('/api/comandas/', json=comanda_data)
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'mesa' in data['message'].lower()
    
    def test_crear_comanda_mesa_dada_baja(self, test_client, test_db_session, created_mozo, sample_comanda_data):
        """Test: Intentar crear comanda con mesa dada de baja"""
        # Crear mesa y darla de baja
        sector = Sector(numero=99)
        test_db_session.add(sector)
        test_db_session.commit()
        
        mesa = Mesa(numero=99, tipo='Interior', cant_comensales=4, id_sector=sector.id_sector)
        test_db_session.add(mesa)
        test_db_session.commit()
        mesa.baja = True
        test_db_session.commit()
        
        comanda_data = sample_comanda_data.copy()
        comanda_data['id_mozo'] = created_mozo.id
        comanda_data['id_mesa'] = mesa.id_mesa
        
        response = test_client.post('/api/comandas/', json=comanda_data)
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'baja' in data['message'].lower()
    
    def test_obtener_comanda_existente(self, test_client, created_comanda):
        """Test: Obtener una comanda por ID"""
        response = test_client.get(f'/api/comandas/{created_comanda.id_comanda}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['id_comanda'] == created_comanda.id_comanda
    
    def test_obtener_comanda_inexistente(self, test_client):
        """Test: Obtener una comanda que no existe"""
        response = test_client.get('/api/comandas/99999')
        assert response.status_code == 404
        assert_response_error(response, 404)
    
    def test_modificar_comanda(self, test_client, created_comanda):
        """Test: Modificar una comanda existente"""
        nuevos_datos = {'fecha': '2024-01-20'}
        response = test_client.put(
            f'/api/comandas/{created_comanda.id_comanda}',
            json=nuevos_datos
        )
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['fecha'] == '2024-01-20'
    
    def test_modificar_comanda_mozo(self, test_client, test_db_session, created_comanda, created_sector):
        """Test: Modificar el mozo de una comanda"""
        # Crear nuevo mozo
        nuevo_mozo = Mozo(
            documento='88888888',
            nombre_apellido='Nuevo Mozo',
            id_sector=created_sector.id_sector
        )
        test_db_session.add(nuevo_mozo)
        test_db_session.commit()
        
        response = test_client.put(
            f'/api/comandas/{created_comanda.id_comanda}',
            json={'id_mozo': nuevo_mozo.id}
        )
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['id_mozo'] == nuevo_mozo.id
    
    def test_modificar_comanda_mozo_inexistente(self, test_client, created_comanda):
        """Test: Intentar modificar comanda con mozo inexistente"""
        response = test_client.put(
            f'/api/comandas/{created_comanda.id_comanda}',
            json={'id_mozo': 99999}
        )
        assert response.status_code == 400
        assert_response_error(response, 400)
    
    def test_modificar_comanda_mesa(self, test_client, test_db_session, created_comanda, created_sector):
        """Test: Modificar la mesa de una comanda"""
        # Crear nueva mesa
        nueva_mesa = Mesa(
            numero=99,
            tipo='Exterior',
            cant_comensales=6,
            id_sector=created_sector.id_sector
        )
        test_db_session.add(nueva_mesa)
        test_db_session.commit()
        
        response = test_client.put(
            f'/api/comandas/{created_comanda.id_comanda}',
            json={'id_mesa': nueva_mesa.id_mesa}
        )
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['id_mesa'] == nueva_mesa.id_mesa
    
    def test_modificar_comanda_inexistente(self, test_client):
        """Test: Modificar una comanda que no existe"""
        response = test_client.put(
            '/api/comandas/99999',
            json={'fecha': '2024-01-20'}
        )
        assert response.status_code == 404
        assert_response_error(response, 404)
    
    def test_eliminar_comanda(self, test_client, created_comanda):
        """Test: Dar de baja una comanda"""
        response = test_client.delete(f'/api/comandas/{created_comanda.id_comanda}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['baja'] == True
    
    def test_eliminar_comanda_inexistente(self, test_client):
        """Test: Intentar dar de baja una comanda que no existe"""
        response = test_client.delete('/api/comandas/99999')
        assert response.status_code == 404
        assert_response_error(response, 404)
    
    def test_eliminar_comanda_ya_dada_baja(self, test_client, created_comanda):
        """Test: Intentar dar de baja una comanda ya dada de baja"""
        # Dar de baja primera vez
        test_client.delete(f'/api/comandas/{created_comanda.id_comanda}')
        
        # Intentar dar de baja segunda vez
        response = test_client.delete(f'/api/comandas/{created_comanda.id_comanda}')
        assert response.status_code == 400
        data = assert_response_error(response, 400)
        assert 'ya está dada de baja' in data['message'].lower()
    
    def test_listar_comandas_filtros(self, test_client, created_comanda, created_mozo, created_mesa):
        """Test: Listar comandas con filtros"""
        # Filtrar por mozo
        response = test_client.get(f'/api/comandas/?id_mozo={created_mozo.id}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
        assert all(c['id_mozo'] == created_mozo.id for c in data['data'])
        
        # Filtrar por mesa
        response = test_client.get(f'/api/comandas/?id_mesa={created_mesa.id_mesa}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
        assert all(c['id_mesa'] == created_mesa.id_mesa for c in data['data'])
        
        # Filtrar por fecha
        response = test_client.get(f'/api/comandas/?fecha={created_comanda.fecha}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
    
    def test_listar_comandas_filtro_estado(self, test_client, created_comanda):
        """Test: Listar comandas filtradas por estado"""
        # Filtrar solo activas
        response = test_client.get('/api/comandas/?estado=activa')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(c['baja'] == False for c in data['data'])
        
        # Dar de baja la comanda
        test_client.delete(f'/api/comandas/{created_comanda.id_comanda}')
        
        # Filtrar solo dadas de baja
        response = test_client.get('/api/comandas/?estado=baja')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(c['baja'] == True for c in data['data'])
    
    def test_listar_comandas_paginacion(self, test_client, created_mozo, created_mesa, sample_comanda_data):
        """Test: Listar comandas con paginación"""
        # Crear varias comandas
        for i in range(15):
            comanda_data = sample_comanda_data.copy()
            comanda_data['fecha'] = f'2024-01-{15+i:02d}'
            comanda_data['id_mozo'] = created_mozo.id
            comanda_data['id_mesa'] = created_mesa.id_mesa
            test_client.post('/api/comandas/', json=comanda_data)
        
        # Obtener primera página
        response = test_client.get('/api/comandas/?page=1&per_page=10')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) == 10
        assert data['pagination']['has_next'] == True

