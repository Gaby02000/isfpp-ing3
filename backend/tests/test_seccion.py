import pytest
from models import Seccion
from tests.utils.test_helpers import assert_response_success, assert_response_error, assert_pagination_structure

class TestSeccionModel:
    """Tests unitarios para el modelo Seccion"""
    
    def test_crear_seccion(self, test_db_session, sample_seccion_data):
        """Test: Crear una sección válida"""
        seccion = Seccion(**sample_seccion_data)
        test_db_session.add(seccion)
        test_db_session.commit()
        
        assert seccion.id_seccion is not None
        assert seccion.nombre == sample_seccion_data['nombre']
        assert seccion.baja == False
    
    def test_seccion_json(self, test_db_session, sample_seccion_data):
        """Test: Método json() del modelo"""
        seccion = Seccion(**sample_seccion_data)
        test_db_session.add(seccion)
        test_db_session.commit()
        
        json_data = seccion.json()
        assert json_data['id_seccion'] == seccion.id_seccion
        assert json_data['nombre'] == seccion.nombre
        assert json_data['baja'] == False
    
    def test_seccion_nombre_unico(self, test_db_session, sample_seccion_data):
        """Test: Validar que el nombre de sección sea único"""
        seccion1 = Seccion(**sample_seccion_data)
        test_db_session.add(seccion1)
        test_db_session.commit()
        
        # Intentar crear otra con el mismo nombre
        seccion2 = Seccion(**sample_seccion_data)
        test_db_session.add(seccion2)
        
        with pytest.raises(Exception):
            test_db_session.commit()

class TestSeccionRoutes:
    """Tests de integración para las rutas de Seccion"""
    
    def test_listar_secciones_vacio(self, test_client):
        """Test: Listar secciones cuando no hay ninguna"""
        response = test_client.get('/api/secciones/')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data'] == []
        assert_pagination_structure(data)
    
    def test_crear_seccion_exitosa(self, test_client, sample_seccion_data):
        """Test: Crear una sección exitosamente"""
        response = test_client.post('/api/secciones/', json=sample_seccion_data)
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['nombre'] == sample_seccion_data['nombre']
        assert data['data']['baja'] == False
    
    def test_crear_seccion_sin_datos(self, test_client):
        """Test: Intentar crear sección sin datos"""
        response = test_client.post('/api/secciones/', json={})
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'nombre' in data['message'].lower() or 'requerido' in data['message'].lower()
    
    def test_crear_seccion_nombre_duplicado(self, test_client, sample_seccion_data):
        """Test: Intentar crear sección con nombre duplicado"""
        # Crear primera sección
        test_client.post('/api/secciones/', json=sample_seccion_data)
        
        # Intentar crear otra con el mismo nombre
        response = test_client.post('/api/secciones/', json=sample_seccion_data)
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'Ya existe' in data['message'] or 'único' in data['message'].lower()
    
    def test_obtener_seccion_existente(self, test_client, created_seccion):
        """Test: Obtener una sección por ID"""
        response = test_client.get(f'/api/secciones/{created_seccion.id_seccion}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['id_seccion'] == created_seccion.id_seccion
        assert data['data']['nombre'] == created_seccion.nombre
    
    def test_obtener_seccion_inexistente(self, test_client):
        """Test: Obtener una sección que no existe"""
        response = test_client.get('/api/secciones/99999')
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'no encontrada' in data['message'].lower()
    
    def test_obtener_seccion_dada_baja(self, test_client, test_db_session, sample_seccion_data):
        """Test: Intentar obtener una sección dada de baja"""
        seccion = Seccion(**sample_seccion_data)
        test_db_session.add(seccion)
        test_db_session.commit()
        seccion.baja = True
        test_db_session.commit()
        
        response = test_client.get(f'/api/secciones/{seccion.id_seccion}')
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'no encontrada' in data['message'].lower()
    
    def test_eliminar_seccion(self, test_client, created_seccion):
        """Test: Dar de baja una sección"""
        response = test_client.delete(f'/api/secciones/{created_seccion.id_seccion}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['baja'] == True
    
    def test_eliminar_seccion_inexistente(self, test_client):
        """Test: Intentar dar de baja una sección que no existe"""
        response = test_client.delete('/api/secciones/99999')
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'no encontrada' in data['message'].lower()
    
    def test_eliminar_seccion_ya_dada_baja(self, test_client, created_seccion):
        """Test: Intentar dar de baja una sección ya dada de baja"""
        # Dar de baja primera vez
        test_client.delete(f'/api/secciones/{created_seccion.id_seccion}')
        
        # Intentar dar de baja segunda vez
        response = test_client.delete(f'/api/secciones/{created_seccion.id_seccion}')
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'ya dada de baja' in data['message'].lower()
    
    def test_listar_secciones_filtros(self, test_client, created_seccion):
        """Test: Listar secciones con filtros"""
        # Filtrar solo activas
        response = test_client.get('/api/secciones/?activos=true')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(s['baja'] == False for s in data['data'])
        
        # Filtrar solo dadas de baja
        test_client.delete(f'/api/secciones/{created_seccion.id_seccion}')
        response = test_client.get('/api/secciones/?activos=false')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(s['baja'] == True for s in data['data'])
    
    def test_listar_secciones_paginacion(self, test_client, sample_seccion_data):
        """Test: Listar secciones con paginación"""
        # Crear varias secciones
        for i in range(15):
            seccion_data = sample_seccion_data.copy()
            seccion_data['nombre'] = f'Sección {i}'
            test_client.post('/api/secciones/', json=seccion_data)
        
        # Obtener primera página
        response = test_client.get('/api/secciones/?page=1&per_page=10')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) == 10
        assert data['pagination']['has_next'] == True
    
    def test_listar_secciones_ordenamiento(self, test_client, sample_seccion_data):
        """Test: Verificar que las secciones se ordenen por nombre"""
        # Crear secciones con diferentes nombres
        nombres = ['Zapata', 'Alvarez', 'Benítez']
        for nombre in nombres:
            seccion_data = sample_seccion_data.copy()
            seccion_data['nombre'] = nombre
            test_client.post('/api/secciones/', json=seccion_data)
        
        response = test_client.get('/api/secciones/')
        assert response.status_code == 200
        data = assert_response_success(response)
        secciones_nombres = [s['nombre'] for s in data['data'] if s['nombre'] in nombres]
        assert secciones_nombres == sorted(secciones_nombres)

