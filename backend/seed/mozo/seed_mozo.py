"""
Seeder para mozos
"""
from random import choice, randint
from models import Mozo

def seed_mozos(session, sectores):
    """Crea mozos de prueba"""
    print("👨‍🍳 Creando mozos...")
    
    mozos = []
    
    nombres_apellidos = [
        "Juan Pérez", "María González", "Carlos Rodríguez", "Ana Martínez",
        "Luis Sánchez", "Laura Fernández", "Pedro López", "Sofía García",
        "Diego Gómez", "Carmen Martín", "Miguel Jiménez", "Elena Ruiz",
        "José Hernández", "Patricia Díaz", "Fernando Moreno", "Lucía Álvarez",
        "Roberto Muñoz", "Isabel Romero", "Andrés Alonso", "Marta Gutiérrez"
    ]
    
    calles = [
        "Av. San Martín", "Calle Mitre", "Av. Roca", "Calle Belgrano",
        "Av. 9 de Julio", "Calle Sarmiento", "Av. Libertador", "Calle Rivadavia",
        "Av. Alem", "Calle Urquiza", "Av. Perón", "Calle Güemes"
    ]
    
    for i, nombre_apellido in enumerate(nombres_apellidos):
        documento = str(randint(20000000, 50000000))
        direccion = f"{choice(calles)} {randint(100, 9999)}"
        telefono = f"{randint(2900, 2999)}-{randint(100000, 999999)}"
        
        # Asignar un sector aleatorio (puede ser None)
        id_sector = choice(sectores).id_sector if sectores and i % 3 != 0 else None
        
        mozo = Mozo(
            documento=documento,
            nombre_apellido=nombre_apellido,
            direccion=direccion,
            telefono=telefono,
            id_sector=id_sector,
            baja=False
        )
        mozos.append(mozo)
    
    session.add_all(mozos)
    session.commit()
    print(f"✅ {len(mozos)} mozos creados")
    return mozos

