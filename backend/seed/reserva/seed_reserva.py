"""
Seeder para Reservas
Genera reservas de prueba para hoy y días futuros
"""
from datetime import datetime, timedelta
from random import choice, randint, sample
from models import Reserva


def seed_reservas(session, clientes, mesas, cantidad=25):
    """Crea reservas de prueba para hoy y días futuros"""
    print("📅 Creando reservas...")
    
    reservas = []
    numero_reserva = 1000
    
    # Obtener fecha/hora actual en horario argentino (UTC-3)
    # Para simular horario argentino, trabajamos con UTC y ajustamos
    ahora_utc = datetime.utcnow()
    # Argentina está en UTC-3, así que restamos 3 horas para obtener hora local argentina
    ahora_arg = ahora_utc - timedelta(hours=3)
    
    # Horarios típicos de restaurante (en horario argentino)
    horarios = [
        (12, 0),   # Almuerzo
        (12, 30),
        (13, 0),
        (13, 30),
        (14, 0),
        (20, 0),   # Cena
        (20, 30),
        (21, 0),
        (21, 30),
        (22, 0),
        (22, 30),
    ]
    
    # Crear reservas para hoy
    hoy = ahora_arg.replace(hour=0, minute=0, second=0, microsecond=0)
    reservas_hoy = 0
    
    # Si aún no es muy tarde, crear reservas para hoy
    if ahora_arg.hour < 23:
        # Crear 5-8 reservas para hoy
        cant_hoy = randint(5, 8)
        horarios_hoy = sample(horarios, min(cant_hoy, len(horarios)))
        
        for hora, minuto in horarios_hoy:
            # Solo crear si la hora aún no pasó
            fecha_reserva = hoy.replace(hour=hora, minute=minuto)
            if fecha_reserva > ahora_arg:
                cliente = choice(clientes)
                mesa = choice([m for m in mesas if m.cant_comensales >= 2])
                
                # Convertir a UTC para guardar en BD (sumar 3 horas para volver a UTC desde local)
                # Si fecha_reserva es local (Arg), UTC es Local + 3 horas
                fecha_reserva_utc = fecha_reserva + timedelta(hours=3)
                
                reserva = Reserva(
                    numero=numero_reserva,
                    fecha_hora=fecha_reserva_utc,
                    cant_personas=randint(2, min(mesa.cant_comensales, 6)),
                    id_cliente=cliente.id_cliente,
                    id_mesa=mesa.id_mesa,
                    cancelado=False
                )
                reservas.append(reserva)
                numero_reserva += 1
                reservas_hoy += 1
    
    # Crear reservas para mañana
    manana = hoy + timedelta(days=1)
    cant_manana = randint(6, 10)
    horarios_manana = sample(horarios, min(cant_manana, len(horarios)))
    
    for hora, minuto in horarios_manana:
        cliente = choice(clientes)
        mesa = choice([m for m in mesas if m.cant_comensales >= 2])
        
        fecha_reserva = manana.replace(hour=hora, minute=minuto)
        fecha_reserva_utc = fecha_reserva - timedelta(hours=3)
        
        reserva = Reserva(
            numero=numero_reserva,
            fecha_hora=fecha_reserva_utc,
            cant_personas=randint(2, min(mesa.cant_comensales, 6)),
            id_cliente=cliente.id_cliente,
            id_mesa=mesa.id_mesa,
            cancelado=False
        )
        reservas.append(reserva)
        numero_reserva += 1
    
    # Crear reservas para los próximos 7 días
    for dia_offset in range(2, 8):
        fecha_dia = hoy + timedelta(days=dia_offset)
        cant_dia = randint(3, 7)
        horarios_dia = sample(horarios, min(cant_dia, len(horarios)))
        
        for hora, minuto in horarios_dia:
            cliente = choice(clientes)
            mesa = choice([m for m in mesas if m.cant_comensales >= 2])
            
            fecha_reserva = fecha_dia.replace(hour=hora, minute=minuto)
            fecha_reserva_utc = fecha_reserva + timedelta(hours=3)
            
            # Algunas reservas canceladas (10% aproximadamente)
            cancelada = randint(1, 10) == 1
            motivo = None
            if cancelada:
                motivos = ['Cliente canceló', 'Cambio de planes', 'Problema de agenda']
                motivo = choice(motivos)
            
            reserva = Reserva(
                numero=numero_reserva,
                fecha_hora=fecha_reserva_utc,
                cant_personas=randint(2, min(mesa.cant_comensales, 6)),
                id_cliente=cliente.id_cliente,
                id_mesa=mesa.id_mesa,
                cancelado=cancelada,
                motivo_cancelacion=motivo,
                senia_devuelta=cancelada and randint(1, 2) == 1
            )
            reservas.append(reserva)
            numero_reserva += 1
    
    session.add_all(reservas)
    session.commit()
    
    reservas_activas = len([r for r in reservas if not r.cancelado])
    print(f"✅ {len(reservas)} reservas creadas ({reservas_activas} activas, {len(reservas) - reservas_activas} canceladas)")
    print(f"   - Reservas para hoy: {reservas_hoy}")
    print(f"   - Reservas para mañana: {cant_manana}")
    print(f"   - Reservas para próximos días: {len(reservas) - reservas_hoy - cant_manana}")
    
    return reservas

