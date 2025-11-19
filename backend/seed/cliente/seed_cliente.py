"""
Seeder para clientes
"""
from random import choice, randint
from models import Cliente

def seed_clientes(session):
    """Crea clientes de prueba"""
    print("📦 Creando clientes...")
    
    clientes = []
    
    nombres = [
        "Juan", "María", "Carlos", "Ana", "Luis", "Laura", "Pedro", "Sofía",
        "Diego", "Carmen", "Miguel", "Elena", "José", "Patricia", "Fernando",
        "Lucía", "Roberto", "Isabel", "Andrés", "Marta", "Javier", "Cristina",
        "Alejandro", "Paula", "Ricardo", "Andrea", "Francisco", "Natalia"
    ]
    
    apellidos = [
        "García", "Rodríguez", "González", "Fernández", "López", "Martínez",
        "Sánchez", "Pérez", "Gómez", "Martín", "Jiménez", "Ruiz", "Hernández",
        "Díaz", "Moreno", "Álvarez", "Muñoz", "Romero", "Alonso", "Gutiérrez",
        "Navarro", "Torres", "Domínguez", "Vázquez", "Ramos", "Gil", "Ramírez",
        "Serrano", "Blanco", "Suárez", "Molina", "Morales", "Ortega", "Delgado"
    ]
    
    dominios_email = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "unpsjb.edu.ar"]
    
    for i in range(20):
        nombre = choice(nombres)
        apellido = choice(apellidos)
        documento = str(randint(20000000, 50000000))
        num_telefono = f"{randint(2900, 2999)}-{randint(100000, 999999)}"
        email = f"{nombre.lower()}.{apellido.lower()}{i}@{choice(dominios_email)}"
        
        cliente = Cliente(
            documento=documento,
            nombre=nombre,
            apellido=apellido,
            num_telefono=num_telefono,
            email=email,
            baja=False
        )
        clientes.append(cliente)
    
    session.add_all(clientes)
    session.commit()
    print(f"✅ {len(clientes)} clientes creados")
    return clientes

