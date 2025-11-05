"""
Seeder para Productos
Genera productos (platos, postres, bebidas) de prueba
"""
from models import Producto, Plato, Postre, Bebida


def seed_productos(session, secciones):
    """Crea productos de prueba"""
    print("📦 Creando productos...")
    
    productos_data = [
        # Entradas
        {"codigo": "ENT001", "nombre": "Provoleta", "precio": 1200.00, "seccion": "Entradas", "tipo": "plato"},
        {"codigo": "ENT002", "nombre": "Empanadas (3 unidades)", "precio": 800.00, "seccion": "Entradas", "tipo": "plato"},
        {"codigo": "ENT003", "nombre": "Bruschettas", "precio": 950.00, "seccion": "Entradas", "tipo": "plato"},
        
        # Platos Principales
        {"codigo": "PLA001", "nombre": "Milanesa Napolitana con Papas", "precio": 1800.00, "seccion": "Platos Principales", "tipo": "plato"},
        {"codigo": "PLA002", "nombre": "Asado de Tira", "precio": 2500.00, "seccion": "Platos Principales", "tipo": "plato"},
        {"codigo": "PLA003", "nombre": "Pescado a la Plancha", "precio": 2200.00, "seccion": "Platos Principales", "tipo": "plato"},
        {"codigo": "PLA004", "nombre": "Risotto de Hongos", "precio": 1900.00, "seccion": "Platos Principales", "tipo": "plato"},
        {"codigo": "PLA005", "nombre": "Pollo al Curry", "precio": 1750.00, "seccion": "Platos Principales", "tipo": "plato"},
        
        # Postres
        {"codigo": "POS001", "nombre": "Flan Casero con Dulce de Leche", "precio": 650.00, "seccion": "Postres", "tipo": "postre"},
        {"codigo": "POS002", "nombre": "Tiramisú", "precio": 850.00, "seccion": "Postres", "tipo": "postre"},
        {"codigo": "POS003", "nombre": "Brownie con Helado", "precio": 900.00, "seccion": "Postres", "tipo": "postre"},
        {"codigo": "POS004", "nombre": "Mousse de Chocolate", "precio": 750.00, "seccion": "Postres", "tipo": "postre"},
        
        # Bebidas
        {"codigo": "BEB001", "nombre": "Coca-Cola 500ml", "precio": 350.00, "seccion": "Bebidas", "tipo": "bebida", "cm3": 500},
        {"codigo": "BEB002", "nombre": "Agua Mineral 500ml", "precio": 200.00, "seccion": "Bebidas", "tipo": "bebida", "cm3": 500},
        {"codigo": "BEB003", "nombre": "Cerveza Artesanal 500ml", "precio": 600.00, "seccion": "Bebidas", "tipo": "bebida", "cm3": 500},
        {"codigo": "BEB004", "nombre": "Vino Tinto (Copa)", "precio": 450.00, "seccion": "Bebidas", "tipo": "bebida", "cm3": 150},
        {"codigo": "BEB005", "nombre": "Jugo de Naranja Natural", "precio": 300.00, "seccion": "Bebidas", "tipo": "bebida", "cm3": 300},
        
        # Menú del Día
        {"codigo": "MEN001", "nombre": "Menú del Día Completo", "precio": 1500.00, "seccion": "Menú del Día", "tipo": "plato"},
    ]
    
    productos_creados = []
    platos_creados = []
    postres_creados = []
    bebidas_creadas = []
    
    secciones_dict = {s.nombre: s for s in secciones}
    
    for prod_data in productos_data:
        seccion = secciones_dict[prod_data["seccion"]]
        producto = Producto(
            codigo=prod_data["codigo"],
            nombre=prod_data["nombre"],
            precio=prod_data["precio"],
            id_seccion=seccion.id_seccion,
            descripcion=f"Delicioso {prod_data['nombre'].lower()}",
            baja=False
        )
        session.add(producto)
        session.flush()  # Para obtener el id_producto
        
        if prod_data["tipo"] == "plato":
            plato = Plato(id_plato=producto.id_producto)
            platos_creados.append(plato)
            session.add(plato)
        elif prod_data["tipo"] == "postre":
            postre = Postre(id_postre=producto.id_producto)
            postres_creados.append(postre)
            session.add(postre)
        elif prod_data["tipo"] == "bebida":
            bebida = Bebida(id_bebida=producto.id_producto, cm3=prod_data["cm3"])
            bebidas_creadas.append(bebida)
            session.add(bebida)
        
        productos_creados.append(producto)
    
    session.commit()
    print(f"✅ {len(productos_creados)} productos creados")
    print(f"   - {len(platos_creados)} platos")
    print(f"   - {len(postres_creados)} postres")
    print(f"   - {len(bebidas_creadas)} bebidas")
    return productos_creados

