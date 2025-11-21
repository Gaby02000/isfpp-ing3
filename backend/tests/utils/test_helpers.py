"""Funciones auxiliares para los tests"""

def assert_response_success(response, expected_status=200):
    """Verifica que una respuesta sea exitosa"""
    assert response.status_code == expected_status
    data = response.get_json()
    assert data['status'] == 'success'
    return data

def assert_response_error(response, expected_status=400):
    """Verifica que una respuesta sea un error"""
    assert response.status_code == expected_status
    data = response.get_json()
    assert data['status'] == 'error'
    return data

def assert_pagination_structure(data):
    """Verifica que la estructura de paginación sea correcta"""
    assert 'pagination' in data
    pagination = data['pagination']
    assert 'page' in pagination
    assert 'per_page' in pagination
    assert 'total' in pagination
    assert 'total_pages' in pagination
    assert 'has_next' in pagination
    assert 'has_prev' in pagination

