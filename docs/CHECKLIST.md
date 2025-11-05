# Checklist de Implementación - ISFPP 2025

Este documento detalla el estado de implementación del proyecto según los requerimientos del ISFPP 2025.

**Última actualización:** 2025

---

## 📊 Resumen General

| Módulo | Backend | Frontend | Estado |
|--------|---------|----------|--------|
| Gestión de Mesas | 🟡 Parcial | ❌ No | 40% |
| Gestión de Productos | 🟡 Parcial | ❌ No | 30% |
| Gestión de Mozos | ❌ No | 🟡 Parcial | 20% |
| Gestión de Clientes | ❌ No | ❌ No | 0% |
| Gestión de Comandas | ❌ No | ❌ No | 0% |
| Gestión de Reservas | ❌ No | ❌ No | 0% |
| Gestión de Pagos | ❌ No | ❌ No | 0% |
| Reportes | ❌ No | ❌ No | 0% |

---

## ✅ Módulo 1: Gestión de Mesas

### Backend
- [x] Modelo `Mesa` implementado
- [x] Modelo `Sector` implementado
- [x] Rutas ABM Mesas (`mesa_routes.py`)
- [x] Rutas ABM Sectores (`sector_routes.py`)
- [ ] Endpoint `GET /api/mesas/disponibles` (filtrar por fecha/hora y estado)
- [ ] Validación de mesas disponibles para reservas

### Frontend
- [ ] Página de listado de mesas
- [ ] Página de alta de mesa
- [ ] Página de modificación de mesa
- [ ] Página de baja de mesa
- [ ] Página de listado de sectores
- [ ] Página de alta de sector
- [ ] Página de modificación de sector
- [ ] Página de baja de sector
- [ ] Página de mesas disponibles (con filtros)

**Prioridad:** Alta 🟥

---

## ✅ Módulo 2: Gestión de Productos y Carta

### Backend
- [x] Modelo `Seccion` implementado
- [x] Modelo `Producto` implementado
- [x] Modelos `Plato`, `Postre`, `Bebida` implementados
- [x] Rutas ABM Secciones (`seccion_routes.py`)
- [x] Rutas ABM Productos (`producto_routes.py`)
- [ ] Endpoint `GET /api/carta` (productos agrupados por sección)
- [ ] Filtros por tipo de producto en listado

### Frontend
- [ ] Página de listado de secciones
- [ ] Página de alta de sección
- [ ] Página de modificación de sección
- [ ] Página de baja de sección
- [ ] Página de listado de productos
- [ ] Página de alta de producto (con selector de tipo)
- [ ] Página de modificación de producto
- [ ] Página de baja de producto
- [ ] Página de consulta de carta (vista pública)

**Prioridad:** Alta 🟥

---

## ⚠️ Módulo 3: Gestión de Mozos y Atención al Público

### Backend - Clientes
- [ ] Modelo `Cliente` (documento, nombre, apellido, teléfono, correo, baja)
- [ ] Rutas ABM Clientes (`cliente_routes.py`)
- [ ] Validación de documento único
- [ ] Validación de formato de correo

### Backend - Mozos
- [ ] Modelo `Mozo` (documento, nombre, apellido, dirección, teléfono, id_sector, baja)
- [ ] Rutas ABM Mozos (`mozo_routes.py`)
- [ ] Validación de documento único
- [ ] Relación con Sector

### Backend - Comandas
- [ ] Modelo `Comanda` (id, fecha, id_mesa, id_mozo, id_pre_ticket, estado)
- [ ] Modelo `DetalleComanda` (id, id_comanda, id_producto, cantidad, precio_unitario)
- [ ] Rutas de Comandas (`comanda_routes.py`)
  - [ ] `POST /api/comandas` - Crear comanda
  - [ ] `PUT /api/comandas/:id` - Modificar comanda
  - [ ] `DELETE /api/comandas/:id` - Cancelar comanda
  - [ ] `POST /api/comandas/:id/cerrar` - Cerrar comanda
  - [ ] `POST /api/comandas/:id/entregar-producto` - Entregar producto
  - [ ] `GET /api/comandas` - Listar comandas

### Backend - Facturas
- [ ] Modelo `PreTicket` (código, fecha, monto_total)
- [ ] Modelo `DetallePreTicket` (id, id_pre_ticket, id_producto, cantidad, precio_unitario)
- [ ] Modelo `Factura` (id, código, monto, fecha, id_cliente)
- [ ] Modelo `DetalleFactura` (id, id_factura, id_producto, cantidad, precio_unitario)
- [ ] Ruta `POST /api/facturas/con-pre-ticket` - Crear factura con pre-ticket

### Frontend
- [x] Página de listado de mozos
- [x] Página de alta de mozo
- [x] Página de modificación de mozo
- [x] Página de baja de mozo
- [ ] Página de listado de clientes
- [ ] Página de alta de cliente
- [ ] Página de modificación de cliente
- [ ] Página de baja de cliente
- [ ] Página de gestión de comandas
- [ ] Página de creación de comanda
- [ ] Página de modificación de comanda
- [ ] Página de creación de factura

**Prioridad:** Alta 🟥

---

## ❌ Módulo 4: Gestión de Reservas

### Backend
- [ ] Modelo `Reserva` (id, número, fecha_hora, cant_personas, id_cliente, id_mesa, cancelado)
- [ ] Modelo `MenuReserva` (id, monto_seña, seña_paga)
- [ ] Modelo `DetalleMenuReserva` (id, id_menu_reserva, id_producto, cantidad, precio_unitario)
- [ ] Modelo `Seña` (id, monto, fecha, id_menu_reserva)
- [ ] Rutas de Reservas (`reserva_routes.py`)
  - [ ] `POST /api/reservas` - Crear reserva
  - [ ] `PUT /api/reservas/:id` - Modificar reserva
  - [ ] `POST /api/reservas/:id/cancelar-anticipada` - Cancelar reserva anticipada
  - [ ] `POST /api/reservas/:id/cancelar-ausencia` - Cancelar reserva por ausencia
  - [ ] `GET /api/reservas` - Listar reservas (con filtros)
  - [ ] `POST /api/reservas/:id/comanda` - Crear comanda con reserva
  - [ ] `POST /api/reservas/:id/asistida` - Marcar reserva como asistida

### Frontend
- [ ] Página de listado de reservas
- [ ] Página de creación de reserva
- [ ] Página de modificación de reserva
- [ ] Página de cancelación de reserva
- [ ] Vista de calendario de reservas

**Prioridad:** Alta 🟥

---

## ❌ Módulo 5: Gestión de Pagos

### Backend
- [ ] Modelo `MedioPago` (id, nombre, tipo, activo)
- [ ] Modelo `Pago` (id, id_factura, id_medio_pago, monto, fecha, número_comprobante)
- [ ] Rutas ABM Medios de Pago (`medio_pago_routes.py`)
- [ ] Ruta `POST /api/pagos/cobrar-factura` - Cobrar factura adeudada
- [ ] Validación de monto restante en factura
- [ ] Actualización automática de estado de factura

### Frontend
- [ ] Página de listado de medios de pago
- [ ] Página de alta de medio de pago
- [ ] Página de modificación de medio de pago
- [ ] Página de baja de medio de pago
- [ ] Página de cobro de facturas adeudadas

**Prioridad:** Alta 🟥

---

## ❌ Módulo 6: Reportes

Se requiere implementar **al menos 4 reportes**. Opciones sugeridas:

### Backend
- [ ] `GET /api/reportes/ventas-por-periodo` - Ventas por período
- [ ] `GET /api/reportes/productos-mas-vendidos` - Productos más vendidos
- [ ] `GET /api/reportes/facturas-impagas` - Facturas impagas
- [ ] `GET /api/reportes/reservas-por-periodo` - Reservas por período
- [ ] `GET /api/reportes/comandas-por-mozo` - Comandas por mozo
- [ ] `GET /api/reportes/mesas-mas-utilizadas` - Mesas más utilizadas
- [ ] `GET /api/reportes/ingresos-diarios` - Ingresos diarios

### Frontend
- [ ] Página de reportes con selector
- [ ] Visualización de reportes (tablas, gráficos)
- [ ] Exportación de reportes (PDF, Excel)

**Prioridad:** Media 🟧

---

## 📝 Historias de Usuario (HU)

### Gestión de Mesas
- [x] HU #1: Alta Mesa
- [x] HU #2: Baja Mesa
- [x] HU #3: Modificar Mesa
- [x] HU #4: Listar Mesas
- [x] HU #5: Alta Sector
- [x] HU #6: Baja Sector
- [x] HU #7: Modificar Sector
- [x] HU #8: Listar Sectores
- [ ] HU #9: Listar Mesas Disponibles

### Gestión de Productos
- [x] HU #10: Alta Producto
- [x] HU #11: Baja Producto
- [x] HU #12: Modificar Producto
- [x] HU #13: Listar Productos
- [x] HU #14: Alta Sección de Carta
- [x] HU #15: Baja Sección de Carta
- [x] HU #16: Modificar Sección de Carta
- [x] HU #17: Listar Secciones de Carta
- [ ] HU #18: Consultar Carta

### Gestión de Mozos y Atención
- [ ] HU #19: Alta Cliente
- [ ] HU #20: Modificar Cliente
- [ ] HU #21: Baja Cliente
- [x] HU #33: Alta Mozo
- [x] HU #34: Baja Mozo
- [x] HU #35: Modificar Mozo
- [x] HU #36: Listar Mozos
- [ ] HU #35: Crear Comanda Restaurante
- [ ] HU #36: Modificar Comanda Restaurante
- [ ] HU #37: Cancelar Comanda Restaurante
- [ ] HU #38: Cerrar Comanda
- [ ] Entregar Producto (HU faltante en doc)
- [ ] Crear Factura con Pre-ticket (HU faltante en doc)

### Gestión de Reservas
- [ ] HU #22: Crear Reserva
- [ ] HU #23: Modificar Reserva
- [ ] HU #24: Cancelar Reserva Anticipada
- [ ] HU #25: Cancelar Reserva por Ausencia
- [ ] HU #26: Listar Reservas
- [ ] HU #27: Crear Comanda con Reserva

### Gestión de Pagos
- [ ] HU #28: Cobrar Factura Adeudada
- [ ] HU #29: Alta Medio de Pago
- [ ] HU #30: Baja Medio de Pago
- [ ] HU #31: Modificar Medio de Pago
- [ ] HU #32: Listar Medios de Pago

---

## 🗄️ Modelos de Base de Datos

### Implementados ✅
- [x] `Seccion`
- [x] `Producto`
- [x] `Plato`
- [x] `Postre`
- [x] `Bebida`
- [x] `Sector`
- [x] `Mesa`

### Pendientes ❌
- [ ] `Cliente`
- [ ] `Mozo`
- [ ] `Comanda`
- [ ] `DetalleComanda`
- [ ] `Reserva`
- [ ] `MenuReserva`
- [ ] `DetalleMenuReserva`
- [ ] `Seña`
- [ ] `PreTicket`
- [ ] `DetallePreTicket`
- [ ] `Factura`
- [ ] `DetalleFactura`
- [ ] `Pago`
- [ ] `MedioPago`

---

## 🔧 Requerimientos Técnicos

### Backend
- [x] Flask configurado
- [x] SQLAlchemy configurado
- [x] Flask-Migrate configurado
- [x] PostgreSQL configurado
- [x] Docker configurado
- [ ] Validaciones de negocio implementadas
- [ ] Manejo de errores estandarizado
- [ ] Logging implementado

### Frontend
- [x] React configurado
- [x] Bootstrap configurado
- [x] React Router configurado
- [ ] Servicios API implementados
- [ ] Manejo de errores en frontend
- [ ] Validaciones de formularios

---

## 📦 Datos de Prueba

- [x] Script seeder implementado
- [x] Datos falsos para todas las entidades
- [x] Comando `pnpm seed` configurado

---

## 🎯 Próximos Pasos Sugeridos

1. **Prioridad Alta:**
   - Implementar modelos faltantes (Cliente, Mozo, Comanda, Reserva, etc.)
   - Crear rutas backend para todas las funcionalidades
   - Implementar frontend para gestión de mesas y productos

2. **Prioridad Media:**
   - Implementar módulo de reservas
   - Implementar módulo de pagos
   - Crear reportes básicos

3. **Prioridad Baja:**
   - Mejorar UI/UX
   - Optimizar consultas
   - Agregar tests

---

**Nota:** Este checklist se actualiza conforme avanza el desarrollo del proyecto.

