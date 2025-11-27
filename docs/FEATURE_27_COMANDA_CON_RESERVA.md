# Feature #27: Crear Comanda con Reserva

## 📋 Resumen
Se implementó la funcionalidad de crear una comanda asociada a una reserva existente. Cuando un cliente llega al restaurante, el mozo puede marcar la reserva como "asistida" y luego crear una comanda directamente desde esa reserva, registrando automáticamente los datos del cliente y la mesa.

## 🔄 Flujo de Trabajo

### Paso 1: Marcar Reserva como Asistida
```
PUT /api/reserva/{id_reserva}/asistida
```
Cambiar el estado de la reserva de "activa" a "asistida" cuando el cliente llega.

**Validaciones:**
- La reserva debe estar en estado "activa"
- La reserva no debe estar cancelada

**Respuesta exitosa:**
```json
{
  "status": "success",
  "message": "Reserva marcada como asistida correctamente",
  "data": { ... }
}
```

### Paso 2: Crear Comanda desde Reserva
```
POST /api/comanda/desde-reserva
```
Crear una comanda asociada a la reserva asistida.

**Body:**
```json
{
  "id_reserva": 1,
  "id_mozo": 5,
  "observaciones": "Sin picante",
  "productos": [
    {"id_producto": 10, "cantidad": 2},
    {"id_producto": 15, "cantidad": 1}
  ]
}
```

## ✅ Criterios de Aceptación Implementados

### 1. Estados de Reserva ✓
- Reserva inicia en estado **"activa"**
- Al llegar el cliente, se marca como **"asistida"**
- Al crear comanda, cambia a **"en_curso"**
- Estados posibles: `activa`, `asistida`, `en_curso`, `completada`, `cancelada`

### 2. Estados de Mesa ✓
- Mesa inicia en estado **"disponible"**
- Al crear comanda, cambia a **"ocupada"**
- Estados posibles: `disponible`, `ocupada`, `reservada`

### 3. Validaciones de Reserva ✓
- Solo se puede crear comanda para reservas en estado "activa" o "asistida"
- No se puede crear comanda para reserva cancelada
- No se pueden crear dos comandas para la misma reserva

### 4. Validaciones de Mesa ✓
- La mesa de la reserva debe ser válida y activa
- No se pueden tener dos comandas abiertas en la misma mesa
- La mesa coincide automáticamente con los datos de la reserva

### 5. Validaciones de Mozo ✓
- El mozo debe existir y estar activo

### 6. Validaciones de Productos ✓
- Solo se incluyen productos activos (no dados de baja)
- Se valida cantidad mayor a 0
- Se captura el precio unitario del producto al crear el detalle

### 7. Cálculo de Total ✓
- Se calcula automáticamente la suma de (precio_unitario × cantidad) para cada detalle
- Se devuelve en la respuesta JSON

### 8. Cambios de Estado ✓
- Reserva: `activa/asistida` → `en_curso`
- Mesa: `disponible/reservada` → `ocupada`

## 📊 Cambios en Modelos

### Modelo Reserva
```python
estado = Column(String(20), default='activa', nullable=False)
asistida = Column(Boolean, default=False)  # Deprecado, por retrocompatibilidad
```

### Modelo Mesa
```python
estado = Column(String(20), default='disponible', nullable=False)
```

### Modelo Comanda
```python
id_reserva = Column(Integer, ForeignKey('reserva.id_reserva'), nullable=True)
reserva = relationship("Reserva", foreign_keys=[id_reserva])
```

## 🛣️ Endpoints Nuevos/Modificados

### Endpoints Nuevos

#### 1. Marcar Reserva como Asistida
```
PUT /api/reserva/{id_reserva}/asistida
```
**Cambios:** Cambia el estado de "activa" a "asistida"

#### 2. Crear Comanda desde Reserva
```
POST /api/comanda/desde-reserva
```
**Cambios:**
- Valida que reserva esté en estado correcto
- Vincula comanda a reserva
- Cambia estado de reserva a "en_curso"
- Cambia estado de mesa a "ocupada"
- Agrega productos si se proporcionan
- Calcula total automáticamente

## 🧪 Tests Incluidos

Archivo: `backend/tests/test_comanda_desde_reserva.py`

### Casos de Prueba:
1. ✅ Crear comanda exitosamente desde reserva asistida
2. ✅ Validar error si reserva no está asistida
3. ✅ Validar error si reserva está cancelada
4. ✅ Validar error si reserva no existe
5. ✅ Validar error si mozo no existe
6. ✅ No permitir dos comandas por la misma reserva
7. ✅ No permitir dos comandas abiertas en la misma mesa
8. ✅ Validar que comanda incluye todos los datos de reserva
9. ✅ Validar cálculo correcto del total
10. ✅ Validar que solo se incluyen productos activos

## 📦 Migración de Base de Datos

Archivo: `backend/migrations/versions/add_reserva_comanda_fields.py`

**Cambios de esquema:**
- Agregar columna `estado` a tabla `reserva`
- Agregar columna `estado` a tabla `mesa`
- Agregar columna `id_reserva` a tabla `comanda`
- Crear foreign key entre `comanda.id_reserva` y `reserva.id_reserva`

**Para ejecutar:**
```bash
alembic upgrade head
```

## 🔐 Validaciones de Seguridad

- ✅ Validación de IDs válidos (conversión a int)
- ✅ Validación de estados de recursos
- ✅ Validación de relaciones entre entidades
- ✅ Transacciones atómicas (rollback en caso de error)
- ✅ Manejo de excepciones completo

## 📝 JSON Response Examples

### Crear Comanda Exitosamente
```json
{
  "status": "success",
  "message": "Comanda creada exitosamente desde la reserva",
  "data": {
    "id_comanda": 42,
    "fecha": "2025-11-27 14:30:45",
    "fecha_cierre": null,
    "id_mozo": 5,
    "id_mesa": 1,
    "id_reserva": 10,
    "estado": "Abierta",
    "observaciones": null,
    "baja": false,
    "detalles": [
      {
        "id_detalle_comanda": 1,
        "id_producto": 10,
        "cantidad": 2,
        "precio_unitario": 100.0,
        "entregado": false,
        "producto": { ... }
      }
    ],
    "total": 200.0,
    "mesa": { ... },
    "mozo": { ... },
    "reserva": { ... }
  }
}
```

### Errores Comunes
```json
{
  "status": "error",
  "message": "La reserva debe estar en estado \"activa\" o \"asistida\". Estado actual: completada"
}
```

## 🚀 Próximos Pasos (Opcionales)

1. Agregar endpoint para filtrar comandas por reserva
2. Agregar endpoint para completar una reserva (cerrar comanda + generar factura)
3. Agregar métrica de tiempo entre "asistida" y "en_curso"
4. Agregar log de auditoría para cambios de estado

## ✨ Notas Técnicas

- Los cambios de estado son atómicos (se ejecutan en la misma transacción)
- La fecha de la comanda se toma automáticamente con `datetime.now()`
- El precio unitario se captura al momento de crear el detalle
- Se mantiene retrocompatibilidad con el campo `asistida` (booleano) en Reserva
