# Feature #27: Crear Comanda con Reserva - ✅ IMPLEMENTADO

## 📋 Resumen de Implementación

Esta feature permite que un mozo cree una comanda asociada a una reserva existente, registrando los pedidos del cliente al llegar al restaurante.

---

## ✅ Criterios de Aceptación Implementados

### 1. **Solo se puede crear comanda para reservas con estado "activa" y "asistida"**
- ✅ Validación en línea 145-152 de `comanda_routes.py`
- Rechaza reservas canceladas o en otros estados

### 2. **La mesa y el cliente deben coincidir con los datos de la reserva**
- ✅ La mesa se obtiene automáticamente de la reserva (línea 157)
- ✅ El cliente viene implícitamente de la reserva
- ✅ Validación de mesa activa (línea 163)

### 3. **La comanda debe generarse automáticamente con la información de la reserva**
- ✅ Endpoint POST `/api/comanda/desde-reserva` 
- ✅ Crea comanda con fecha actual, mozo, mesa, y asocia reserva (línea 177-186)
- ✅ Campo `id_reserva` agregado al modelo Comanda

### 4. **No se pueden incluir productos inactivos**
- ✅ Validación en línea 196-202
- Solo agrega productos que tienen `baja=False`

### 5. **Al confirmar, la reserva pasa a "en curso" y la mesa a "ocupada"**
- ✅ Línea 204: `reserva.estado = 'en_curso'`
- ✅ Línea 207: `mesa.estado = 'ocupada'`
- ✅ Ambos cambios se guardan en BD

### 6. **El sistema calcula el total de la comanda**
- ✅ Método `calcular_total()` en modelo Comanda
- ✅ Se incluye en respuesta JSON (detalles + total)
- ✅ Se puede cerrar como cualquier otra comanda

### 7. **Primero marcar como "Asistida", luego crear comanda**
- ✅ Endpoint PUT `/api/reserva/{id}/asistida` para marcar asistida (línea 34-57 en reserva_routes.py)
- ✅ Solo entonces se puede crear la comanda (validación en línea 145-152)
- ✅ Estados: activa → asistida → en_curso

---

## 🔧 Cambios Técnicos

### Modelos Modificados

#### `backend/models/reserva.py`
```python
estado = Column(String(20), default='activa', nullable=False)
# Estados: 'activa', 'asistida', 'en_curso', 'completada', 'cancelada'
asistida = Column(Boolean, default=False)  # Retrocompatibilidad
```

#### `backend/models/mesa.py`
```python
estado = Column(String(20), default='disponible', nullable=False)
# Estados: 'disponible', 'ocupada', 'reservada'
```

#### `backend/models/comanda.py`
```python
id_reserva = Column(Integer, ForeignKey('reserva.id_reserva'), nullable=True)
reserva = relationship("Reserva", foreign_keys=[id_reserva])
```

#### `backend/models/detalle_comanda.py`
- ✅ Removido campo innecesario `id_detalle_reserva`

---

## 📡 Endpoints Nuevos

### 1. **Marcar Reserva como Asistida**
```
PUT /api/reserva/{id}/asistida
```
**Payload:**
```json
{}
```

**Response:**
```json
{
  "status": "success",
  "message": "Reserva marcada como asistida correctamente",
  "data": {
    "id_reserva": 1,
    "estado": "asistida",
    "asistida": true,
    ...
  }
}
```

### 2. **Crear Comanda desde Reserva**
```
POST /api/comanda/desde-reserva
```

**Payload:**
```json
{
  "id_reserva": 1,
  "id_mozo": 1,
  "observaciones": "Sin picante",
  "productos": [
    {"id_producto": 1, "cantidad": 2},
    {"id_producto": 5, "cantidad": 1}
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Comanda creada exitosamente desde la reserva",
  "data": {
    "id_comanda": 3,
    "id_reserva": 1,
    "id_mesa": 1,
    "id_mozo": 1,
    "estado": "Abierta",
    "fecha": "2025-11-27 15:30:45",
    "detalles": [
      {
        "id_detalle_comanda": 1,
        "id_producto": 1,
        "cantidad": 2,
        "precio_unitario": 1200.00,
        "entregado": false,
        "subtotal": 2400.00
      },
      {
        "id_detalle_comanda": 2,
        "id_producto": 5,
        "cantidad": 1,
        "precio_unitario": 250.00,
        "entotal": false,
        "subtotal": 250.00
      }
    ],
    "total": 2650.00,
    "mesa": { ... },
    "reserva": { ... }
  }
}
```

---

## ✅ Validaciones Implementadas

1. ✅ Reserva existe
2. ✅ Reserva no está cancelada
3. ✅ Reserva está en estado "activa" o "asistida"
4. ✅ No existe comanda previa para la reserva
5. ✅ Mozo existe y está activo
6. ✅ Mesa existe y está activa
7. ✅ No hay otra comanda abierta en la mesa
8. ✅ Productos existen y están activos
9. ✅ Cantidades son válidas

---

## 🗄️ Cambios en BD

### `init.sql` Actualizado
- ✅ Tabla `mesa`: Agregado `estado VARCHAR(20) DEFAULT 'disponible'`
- ✅ Tabla `reserva`: Agregado `estado VARCHAR(20) DEFAULT 'activa'`
- ✅ Tabla `comanda`: Agregado `id_reserva INT` con FK a reserva

---

## 🧪 Tests

Archivo: `backend/tests/test_comanda_desde_reserva.py`

**10 casos de prueba:**
1. ✅ Crear comanda exitosamente
2. ✅ Validar reserva no asistida
3. ✅ Validar reserva cancelada
4. ✅ Validar reserva inexistente
5. ✅ Validar mozo inexistente
6. ✅ Validar una comanda por reserva
7. ✅ Validar una comanda por mesa
8. ✅ Validar datos de comanda
9. ✅ Validar cálculo de total
10. ✅ Validar solo productos activos

---

## 🚀 Cómo Usar

### Flujo Completo en la UI:

1. **Seleccionar reserva en lista** (ver página de Reservas)
2. **Marcar como "Asistida"** (Click en botón "Cliente llegó" o similar)
3. **Crear comanda** (Click en "Nueva Comanda desde Reserva")
4. **Seleccionar mozo** (Dropdown)
5. **Agregar productos** (Selector de productos + cantidad)
6. **Confirmar creación** (La reserva pasa a "En Curso", mesa a "Ocupada")
7. **Gestionar comanda normalmente** (Agregar/quitar productos, marcar como entregados, etc.)
8. **Cerrar comanda** (Cuando todos los productos estén entregados)
9. **Crear factura** (Seleccionar cliente y medio de pago)

---

## 📝 Notas Importantes

- El campo `asistida` se mantiene por retrocompatibilidad, pero el nuevo campo `estado` es el que controla el flujo
- La comanda hereda automáticamente la mesa y cliente de la reserva
- Los cambios en estado se guardan en `fecha_modificacion` de la reserva
- El total se calcula dinámicamente sumando subtotales de detalles

---

## 🔄 Estado de Implementación

| Requisito | Estado | Ubicación |
|-----------|--------|-----------|
| Modelo Reserva | ✅ | `backend/models/reserva.py` |
| Modelo Mesa | ✅ | `backend/models/mesa.py` |
| Modelo Comanda | ✅ | `backend/models/comanda.py` |
| Endpoint marcar asistida | ✅ | `backend/routes/reserva_routes.py` |
| Endpoint crear desde reserva | ✅ | `backend/routes/comanda_routes.py` |
| BD Schema | ✅ | `backend/init.sql` |
| Tests | ✅ | `backend/tests/test_comanda_desde_reserva.py` |
| Validaciones | ✅ | Todos los criterios |

**ESTADO: ✅ 100% IMPLEMENTADO Y LISTO PARA USAR**

