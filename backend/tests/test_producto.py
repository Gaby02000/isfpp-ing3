import pytest
from models import Producto, Seccion, Plato, Postre, Bebida
from tests.utils.test_helpers import assert_response_success, assert_response_error, assert_pagination_structure

class TestProductoModel:
    """Tests unitarios para el modelo Producto"""
    
    def test_crear_producto(self, test_db_session, created_seccion, sample_producto_data):
        """Test: Crear un producto válido"""
        producto_data = sample_producto_data.copy()
        producto_data['id_seccion'] = created_seccion.id_seccion
        
        producto = Producto(**producto_data)
        test_db_session.add(producto)
        test_db_session.commit()
        
        assert producto.id_producto is not None
        assert producto.codigo == sample_producto_data['codigo']
        assert producto.nombre == sample_producto_data['nombre']
        assert float(producto.precio) == sample_producto_data['precio']
        assert producto.id_seccion == created_seccion.id_seccion
        assert producto.baja == False
    
    def test_producto_json(self, test_db_session, created_seccion, sample_producto_data):
        """Test: Método json() del modelo"""
        producto_data = sample_producto_data.copy()
        producto_data['id_seccion'] = created_seccion.id_seccion
        
        producto = Producto(**producto_data)
        test_db_session.add(producto)
        test_db_session.commit()
        
        json_data = producto.json()
        assert json_data['id_producto'] == producto.id_producto
        assert json_data['codigo'] == producto.codigo
        assert json_data['nombre'] == producto.nombre
        assert json_data['precio'] == float(producto.precio)
        assert json_data['id_seccion'] == producto.id_seccion
        assert json_data['baja'] == False
    
    def test_producto_codigo_unico(self, test_db_session, created_seccion, sample_producto_data):
        """Test: Validar que el código de producto sea único"""
        producto_data = sample_producto_data.copy()
        producto_data['id_seccion'] = created_seccion.id_seccion
        
        producto1 = Producto(**producto_data)
        test_db_session.add(producto1)
        test_db_session.commit()
        
        # Intentar crear otro con el mismo código
        producto2 = Producto(**producto_data)
        test_db_session.add(producto2)
        
        with pytest.raises(Exception):
            test_db_session.commit()

class TestProductoRoutes:
    """Tests de integración para las rutas de Producto"""
    
    def test_listar_productos_vacio(self, test_client):
        """Test: Listar productos cuando no hay ninguno"""
        response = test_client.get('/api/productos/')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data'] == []
        assert_pagination_structure(data)
    
    def test_crear_plato_exitoso(self, test_client, created_seccion, sample_producto_data):
        """Test: Crear un plato exitosamente"""
        producto_data = sample_producto_data.copy()
        producto_data['id_seccion'] = created_seccion.id_seccion
        
        response = test_client.post('/api/productos/platos', json=producto_data)
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['producto']['codigo'] == producto_data['codigo']
        assert data['data']['producto']['nombre'] == producto_data['nombre']
    
    def test_crear_postre_exitoso(self, test_client, created_seccion, sample_producto_data):
        """Test: Crear un postre exitosamente"""
        producto_data = sample_producto_data.copy()
        producto_data['id_seccion'] = created_seccion.id_seccion
        producto_data['codigo'] = 'POST001'
        producto_data['nombre'] = 'Flan'
        
        response = test_client.post('/api/productos/postres', json=producto_data)
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['producto']['codigo'] == producto_data['codigo']
    
    def test_crear_bebida_exitosa(self, test_client, created_seccion, sample_producto_data):
        """Test: Crear una bebida exitosamente"""
        producto_data = sample_producto_data.copy()
        producto_data['id_seccion'] = created_seccion.id_seccion
        producto_data['codigo'] = 'BEB001'
        producto_data['nombre'] = 'Coca Cola'
        producto_data['cm3'] = 500
        
        response = test_client.post('/api/productos/bebidas', json=producto_data)
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['producto']['codigo'] == producto_data['codigo']
        assert data['data']['cm3'] == 500
    
    def test_crear_bebida_sin_cm3(self, test_client, created_seccion, sample_producto_data):
        """Test: Intentar crear bebida sin cm3"""
        producto_data = sample_producto_data.copy()
        producto_data['id_seccion'] = created_seccion.id_seccion
        producto_data['codigo'] = 'BEB002'
        
        response = test_client.post('/api/productos/bebidas', json=producto_data)
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'cm3' in data['message'].lower() or 'requerido' in data['message'].lower()
    
    def test_crear_producto_codigo_duplicado(self, test_client, created_seccion, sample_producto_data):
        """Test: Intentar crear producto con código duplicado"""
        producto_data = sample_producto_data.copy()
        producto_data['id_seccion'] = created_seccion.id_seccion
        
        # Crear primer producto
        test_client.post('/api/productos/platos', json=producto_data)
        
        # Intentar crear otro con el mismo código
        response = test_client.post('/api/productos/platos', json=producto_data)
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'Ya existe' in data['message'] or 'código' in data['message'].lower()
    
    def test_crear_producto_seccion_inexistente(self, test_client, sample_producto_data):
        """Test: Intentar crear producto con sección inexistente"""
        producto_data = sample_producto_data.copy()
        producto_data['id_seccion'] = 99999
        
        response = test_client.post('/api/productos/platos', json=producto_data)
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'sección' in data['message'].lower()
    
    def test_obtener_producto_existente(self, test_client, created_producto):
        """Test: Obtener un producto por ID"""
        response = test_client.get(f'/api/productos/{created_producto.id_producto}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['id_producto'] == created_producto.id_producto
    
    def test_obtener_producto_inexistente(self, test_client):
        """Test: Obtener un producto que no existe"""
        response = test_client.get('/api/productos/99999')
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'no encontrado' in data['message'].lower()
    
    def test_obtener_producto_dado_baja(self, test_client, test_db_session, created_producto):
        """Test: Intentar obtener un producto dado de baja"""
        created_producto.baja = True
        test_db_session.commit()
        
        response = test_client.get(f'/api/productos/{created_producto.id_producto}')
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'no encontrado' in data['message'].lower()
    
    def test_modificar_producto(self, test_client, created_producto):
        """Test: Modificar un producto existente"""
        nuevos_datos = {'nombre': 'Milanesa Especial', 'precio': 2000.00}
        response = test_client.put(
            f'/api/productos/{created_producto.id_producto}',
            json=nuevos_datos
        )
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['nombre'] == 'Milanesa Especial'
        assert data['data']['precio'] == 2000.00
    
    def test_modificar_producto_inexistente(self, test_client):
        """Test: Modificar un producto que no existe"""
        response = test_client.put(
            '/api/productos/99999',
            json={'nombre': 'Nuevo'}
        )
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'no encontrado' in data['message'].lower()
    
    def test_eliminar_producto(self, test_client, created_producto):
        """Test: Dar de baja un producto"""
        response = test_client.delete(f'/api/productos/{created_producto.id_producto}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['baja'] == True
    
    def test_eliminar_producto_inexistente(self, test_client):
        """Test: Intentar dar de baja un producto que no existe"""
        response = test_client.delete('/api/productos/99999')
        assert response.status_code == 200
        data = assert_response_error(response, 200)
        assert 'no encontrado' in data['message'].lower()
    
    def test_listar_platos(self, test_client, created_seccion, sample_producto_data):
        """Test: Listar platos"""
        # Crear un plato
        producto_data = sample_producto_data.copy()
        producto_data['id_seccion'] = created_seccion.id_seccion
        test_client.post('/api/productos/platos', json=producto_data)
        
        response = test_client.get('/api/productos/platos')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
    
    def test_listar_postres(self, test_client, created_seccion, sample_producto_data):
        """Test: Listar postres"""
        # Crear un postre
        producto_data = sample_producto_data.copy()
        producto_data['id_seccion'] = created_seccion.id_seccion
        producto_data['codigo'] = 'POST001'
        producto_data['nombre'] = 'Flan'
        test_client.post('/api/productos/postres', json=producto_data)
        
        response = test_client.get('/api/productos/postres')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
    
    def test_listar_bebidas(self, test_client, created_seccion, sample_producto_data):
        """Test: Listar bebidas"""
        # Crear una bebida
        producto_data = sample_producto_data.copy()
        producto_data['id_seccion'] = created_seccion.id_seccion
        producto_data['codigo'] = 'BEB001'
        producto_data['nombre'] = 'Coca Cola'
        producto_data['cm3'] = 500
        test_client.post('/api/productos/bebidas', json=producto_data)
        
        response = test_client.get('/api/productos/bebidas')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
    
    def test_listar_productos_filtros(self, test_client, created_producto, created_seccion):
        """Test: Listar productos con filtros"""
        # Filtrar por sección
        response = test_client.get(f'/api/productos/?seccion_id={created_seccion.id_seccion}')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) >= 1
        assert all(p['id_seccion'] == created_seccion.id_seccion for p in data['data'])
        
        # Filtrar solo activos
        response = test_client.get('/api/productos/?activos=true')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert all(p['baja'] == False for p in data['data'])
    
    def test_listar_productos_paginacion(self, test_client, created_seccion, sample_producto_data):
        """Test: Listar productos con paginación"""
        # Crear varios productos
        for i in range(15):
            producto_data = sample_producto_data.copy()
            producto_data['codigo'] = f'PROD{i:03d}'
            producto_data['nombre'] = f'Producto {i}'
            producto_data['id_seccion'] = created_seccion.id_seccion
            test_client.post('/api/productos/platos', json=producto_data)
        
        # Obtener primera página
        response = test_client.get('/api/productos/?page=1&per_page=10')
        assert response.status_code == 200
        data = assert_response_success(response)
        assert len(data['data']) == 10
        assert data['pagination']['has_next'] == True
    
    def test_modificar_bebida_cm3(self, test_client, test_db_session, created_seccion, sample_producto_data):
        """Test: Modificar cm3 de una bebida"""
        # Crear bebida
        producto_data = sample_producto_data.copy()
        producto_data['id_seccion'] = created_seccion.id_seccion
        producto_data['codigo'] = 'BEB003'
        producto_data['nombre'] = 'Sprite'
        producto_data['cm3'] = 500
        
        create_response = test_client.post('/api/productos/bebidas', json=producto_data)
        bebida_id = create_response.get_json()['data']['id_bebida']
        
        # Modificar cm3
        response = test_client.put(
            f'/api/productos/bebidas/{bebida_id}',
            json={'cm3': 750}
        )
        assert response.status_code == 200
        data = assert_response_success(response)
        assert data['data']['cm3'] == 750

