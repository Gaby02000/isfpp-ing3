Ingeniería de Software III \-T

ISFPP:

\-- “--”

2025 

Desarrollar un sistema que permita la siguiente funcionalidad:

**Gestión de mesas**

* ABM mesas.  
* ABM sectores.  
* Listar mesas disponibles.

**Gestión de productos (platos, postres, bebidas y menú del día) y carta**

* ABM secciones de la carta.  
* ABM productos.  
* Consultar carta.

**Gestión de mozos y atención al público**

* ABM clientes.  
* ABM mozos.  
* Crear comanda restaurante.  
* Modificar comanda restaurante.  
* Cancelar comanda restaurante.  
* Cerrar comanda.  
* Entregar producto.  
* Crear factura con pre-ticket.

**Gestión de reservas**

* Crear comanda con reserva.  
* Crear reserva.  
* Cancelar reserva anticipada.  
* Cancelar reserva por ausencia.  
* Modificar reservas.  
* Listar reservas.

**Gestión de pagos**

* Cobrar Factura adeudada.  
* ABM medios de pago.

Agregar al menos 4 reportes.

Aplicando los principios y artefactos de Scrum. Convierta las especificaciones del enunciado en un Product Backlog y realice las siguientes, especificaciones, modelos y diagramas:

1. Análisis de riesgos.  
2. Plan de desarrollo con actividades y personas a cargo. Indique los hitos y puntos de control para la revisión de los artefactos construidos.  
3. En base a los requerimientos funcionales provistos. Confeccionar las historias de usuario (HU) e indicar los criterios de aceptación.  
4. Diagrama de clases de software.  
5. Indicar requerimientos no funcionales (tecnologías a utilizar).  
6. Indicar decisiones de diseño.  
7. Estimar el tiempo y esfuerzo necesario para llevar a cabo el proyecto. (PF).  
   1. En base a los requerimientos funcionales planteados, realice el modelado de datos y calcule los Puntos de Función Ajustados. Justifique cada valor de los factores de ajuste y estime una cantidad de LDC y el esfuerzo requerido (en personas/mes) para completar el trabajo.  
   2. Al finalizar, haga un cálculo de la cantidad de líneas de código que involucró el software ya terminado. Realice una conclusión con respecto a los valores obtenidos.  
8. Elaborar casos de prueba. Seleccione una herramienta y genere algunos casos de pruebas teniendo en cuenta las HU.  
9. Codificación y producción de contenido. Se deberá indicar los estándares de programación para cada lenguaje utilizado durante la producción de contenido.

Al finalizar con el desarrollo:

* Investigue y aplique una herramienta para la evaluación de la codificación y la producción de contenido.   
* Identifique los riesgos ocurridos durante el desarrollo y explique a qué se debió la ocurrencia de los mismos. 

# **Gestión de riesgos**

| N° | Riesgo | Probabilidad | Impacto | Categoría |
| :---- | :---- | :---- | :---- | :---- |
| **1** | La interfaz de usuario (UI) puede no gustar o resultar confusa | 50% (media) | Medio | Negocio |
| **2** | Poca experiencia del equipo con Flask | 60%(media) | Alto | Proyecto |
| **3** | Poca experiencia con Docker y contenedores | 60%(media) | Alto  | Tecnico |
| **4** | Posibles problemas de disponibilidad en la aplicación web | 25%(baja) | Alto | Tecnico |
| **5** | Posibles incompatibilidades con distintos navegadores | 30%(baja) | Medio | Tecnico |
| **6** | Tiempo de desarrollo subestimado respecto al cronograma real | 70%(alta) | Alto | Proyecto |
| **7** | Baja productividad por falta de experiencia o motivación | 60%(media) | Medio | Proyecto |
| **8** | Poca experiencia general del grupo en proyectos grandes | 70%(alta) | Alto | Proyecto |
| **9** | Cambios de tecnologías a mitad del desarrollo | 40% (media) | Alto | Negocio |
| **10** | Falta de comunicación con el cliente. | 40% (media) | Alto | Negocio |
| **11** | Falta de comunicación entre los integrantes del grupo  | 60%(media) | Alto | Proyecto |
| **12** | Requerimiento cambiantes durante el desarrollo | 50%(media) | Alto | Negocio |
| **13** | Falta de tiempo para ejecutar pruebas antes de la entrega | 70%(alta) | Alto | Proyecto |
| **14** | Problemas de integración entre módulos del sistema | 60%(media) | Alto | Tecnico |
| **15** | Ausencia de estándares y buenas prácticas de codificación | 50%(media) | Medio | Tecnico |
| **16** | Poca planificación y control del tiempo en los sprints | 60%(media) | Alto | Proyecto |
| **17** | Problemas de integridad de datos | 30%(baja) | Alto  | Tecnico |
| **18** | Posibles limitaciones de escalabilidad del sistema | 20%(baja) | Medio | Tecnico |
| **19** | Falta de especificación o documentación de la infraestructura | 40%(media) | Alto | Tecnico |

Se efectúa una línea de corte cuando la probabilidad es 50% e impacto alto

| Riesgo | Plan de reducción | Plan de monitoreo | Plan de contingencia |
| :---- | :---- | :---- | :---- |
| **2\.** | Realizar capacitaciones internas y compartir recursos de aprendizaje | Reuniones semanales para resolver dudas y revisar | Incorporar un nuevo integrante con experiencia en FastAPI |
| **3\.** | Organizar talleres prácticos para uso de contenedores | Reuniones semanales para resolver dudas y conflictos técnicos | Incorporar un nuevo integrante con conocimiento en Docker |
| **6\.** | Definir entregas parciales y puntos de control por sprint | Reuniones semanales para medir avance y detectar retrasos | Negociar un nuevo plazo de entrega con el docente o cliente |
| **7\.** | Establecer metas claras y roles definidos | Reuniones semanales para medir el avance individual y grupal | Negociar un nuevo plazo o incorporar un integrante de apoyo |
| **8\.** | Participar en cursos o talleres de capacitación | Reuniones semanales para despejar dudas y compartir aprendizajes | Incorporar un nuevo integrante con experiencia o buscar asesoría externa |
| **11\.** | Usar canales formales (Trello, Discord, Drive) para organizar tareas | Reuniones breves cada semana para asegurar coordinación | Asignar un líder de comunicación o mediador dentro del equipo |
| **14\.** | Definir estándares de codificación y comunicación entre módulos | Verificar integraciones en cada iteración | Dividir el trabajo en equipos más pequeños y reestructurar tareas |
| **16\.** | Establecer un cronograma con tareas y responsables | Revisar cumplimiento semanal y ajustar el plan según desvíos | Negociar nueva planificación o priorizar entregables |

**Plan de desarrollo**

2\. Plan de desarrollo con actividades y personas a cargo. Indique los hitos y puntos de control para la revisión de los artefactos construidos.

| Nro. tarea | Tarea \- descripción | Responsable | Fecha de inicio | Fecha de entrega (estimada) | Duración (días) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **1\.** | **Análisis y definición** |  |  |  |  |
| 1.1 | Definición del diagrama de clases | Todos | 07/10/25 | 15/10/25 | 10 |
| 1.2 | Análisis de requerimientos funcionales | Todos | 08/10/25 | 17/08/25 | 9 |
| 1.3 | Análisis de requerimientos NO funcionales | Todos | 08/10/25 | 09/10/25 | 1 |
| **2\.** | **Plan de gestión de riesgos** |  |  |  |  |
| 2.1 | Identificación y análisis de riesgos | Todos | 08/10/25 | 12/10/25 | 4 |
| 2.2 | Reducción y monitoreo | Todos |  |  |  |
| **3\.** | **Puntos de Función** |  |  |  |  |
| 3.1 | Cálculo de puntos de función sin ajustar | Todos | 14/10/25 | 21/10/25 | 7 |
| 3.2 | Cálculo de puntos de función ajustados | Todos |  |  |  |
| 3.3 | Cálculo de líneas de código | Todos |  |  |  |
| **4\.** | **Desarrollo \- Gestión de mesas** |  |  |  |  |
| 4.1 | ABM mesas \+ listado | Francisco Terrón |  |  |  |
| 4.2 | ABM sectores \+ listado | Scott Ellis |  |  |  |
| **5\.** | **Desarrollo \- Gestión de productos** |  |  |  |  |
| 5.1 | ABM productos \+ listado | Gabriel Gimenez |  |  |  |
| 5.2 | ABM secciones \+ listado | Gabriel Gimenez |  |  |  |
| 5.3 | Consultar carta | Scott Ellis |  |  |  |
| **6\.** | **Desarrollo \- Gestión de mozos y atención al público** |  |  |  |  |
| 6.1 | ABM clientes \+ listado | Lautaro Skarkloff |  |  |  |
| 6.2 | ABM mozos \+ listado | Patricio Zapellini |  |  |  |
| 6.3 | Crear comanda | Dos integrantes |  |  |  |
| 6.4 | Modificar comanda | Dos integrantes |  |  |  |
| 6.5 | Cancelar comanda | Dos integrantes |  |  |  |
| 6.6 | Cerrar comanda | Dos integrantes |  |  |  |
| 6.7 | Entregar producto | Francisco Terrón  |  |  |  |
| 6.8 | Crear factura con pre-ticket | Dos integrantes |  |  |  |
| **7\.** | **Desarrollo \- Gestión de reservas** |  |  |  |  |
| 7.1 | Crear reserva |  |  |  |  |
| 7.2 | Asociar reserva a comanda |  |  |  |  |
| 7.3 | Listado reservas |  |  |  |  |
| 7.4 | Modificar reserva |  |  |  |   |
| 7.5 | Cancelar comanda anticipada |  |  |  |  |
| 7.6 | Cancelar comanda por ausencia |  |  |  |  |
| **8\.** | **Gestión de pagos** |  |  |  |  |
| 8.1 | ABM medios de pago \+ listado | Patricio Zappelini  |  |  |  |
| 8.2 | Cobrar facturas impagas |  |  |  |  |
| 9\. | **Realización de casos de prueba** |  |  |  |  |
| 9.1 | Creación de pruebas de validación |  |  |  |  |
| 9.2 | Período de pruebas | TODOS |  |  |  |

**Requerimientos Funcionales**

Gestión de mesas

* Alta mesa  
* Baja mesa  
* Modificar mesa  
* Listar mesas  
* Alta sector  
* Baja sector  
* Modificar sector  
* Listar sectores  
* Listar mesas disponibles

 Gestión de productos y carta

* Alta producto (plato, postre, bebida, menú del día)  
* Baja producto  
* Modificar producto  
* Listar productos  
* Alta sección de carta  
* Baja sección de carta  
* Modificar sección de carta  
* Listar secciones de carta  
* Consultar carta

 Gestión de mozos y atención al público

* Alta cliente  
* Baja cliente  
* Modificar cliente  
* Listar clientes  
* Alta mozo  
* Baja mozo  
* Modificar mozo  
* Listar mozos  
* Crear comanda restaurante  
* Modificar comanda restaurante  
* Cancelar comanda restaurante  
* Cerrar comanda  
* Entregar producto  
* Crear factura con pre-ticket

Gestión de reservas

* Crear reserva  
* Modificar reserva  
* Cancelar reserva anticipada  
* Cancelar reserva por ausencia  
* Listar reservas  
* Crear comanda con reserva

Gestión de pagos

* Cobrar factura adeudada  
* Alta medio de pago  
* Baja medio de pago  
* Modificar medio de pago  
* Listar medios de pago

---

# **Historias de usuario**

---

 

Resumen por prioridad

* **🟥 P1 (alta):** \#1–\#8, \#10–\#17, \#19–\#20, \#24, \#27–\#28, \#30 \-\#34

* **🟧 P2 (media):** \#9, \#21–\#23, \#25–\#26, \#29, \#35-\#39

* **🟩 P3 (baja):** \#18,\#40

### **\#1 Alta Mesa**

**Como** usuario del sistema  
**Quiero** registrar una nueva mesa  
**Para** poder gestionarla en las comandas y asignarla a un sector

**Prioridad:** Alta **🟥** 

**Datos:**

* IdMesa

* número

* tipo

* cantidad de comensales

* IdSector

* baja

**Criterios de aceptación:**

* **Validación de duplicados:** si el número o IdMesa ya existe, el sistema debe mostrar un mensaje de advertencia indicando que la mesa ya está registrada.

* **Validación de sector:** si no se selecciona un sector, el sistema debe mostrar un mensaje indicando que el sector es obligatorio.

* **Validación de campos obligatorios:** tipo y cantidad de comensales no pueden estar vacíos.

* La mesa se registra con el campo *baja \= false* por defecto.




### **\#2 Baja Mesa**

**Como** usuario del sistema  
 **Quiero** dar de baja una mesa existente  
 **Para** evitar que se use en nuevas reservas o comandas

**Prioridad:** Alta **🟥** 

**Datos:**

* IdMesa

**Criterios de aceptación:**

* El sistema debe permitir marcar la mesa como *baja \= true* sin eliminarla físicamente de la base de datos.

* No se puede dar de baja una mesa que esté asignada a una comanda activa o a una reserva vigente.

* Si la mesa tiene una reserva activa, el sistema debe mostrar un mensaje indicando que primero debe liberarse.  
* Cuando se borra la mesa se muestra un mensaje de éxito al usuario.

---

### 

### 

### **\#3 Modificar Mesa**

**Como** usuario del sistema  
 **Quiero** modificar los datos de una mesa existente  
 **Para** mantener actualizada su información y capacidad

**Prioridad**: Media 🟧

**Datos:**

* idMesa

* número

* tipo

* cantidad de comensales

* IdSector

**Criterios de aceptación:**

* Solo se puede modificar una mesa que no esté marcada como *baja y que no esté ocupada en ese momento*.

* No debe permitirse cambiar el número si ya existe otra mesa con el mismo número.

* Si el sector asignado cambia, el sistema debe verificar que el nuevo sector exista.

* La cantidad de comensales debe ser un número entero positivo.

---

### **\#4 Listar Mesas**

**Como** usuario del sistema  
 **Quiero** visualizar el listado completo de mesas registradas  
 **Para** poder consultarlas, filtrarlas o modificarlas según necesidad

**Prioridad**: Media 🟧

**Datos:**

* IdMesa

* número

* tipo

* cantidad de comensales

* sector

* estado (activa/baja)

**Criterios de aceptación:**

* El listado debe mostrar todas las mesas con opción de filtrar por sector, tipo o estado.

* Las mesas dadas de baja deben visualizarse con un indicador de “inactiva”.

* El sistema debe permitir ordenar las mesas por número o por sector.

---

### **\#5 Alta Sector**

**Como** usuario del sistema  
 **Quiero** registrar un nuevo sector del salón  
 **Para** poder asignar mesas y mozos a ese sector

**Prioridad:** Alta **🟥** 

**Datos:**

* IdSector

* número

* baja

**Criterios de aceptación:**

* Validación de duplicados: no se puede registrar un sector con un número ya existente.

* El campo *baja* debe inicializarse como *false*.

* Todos los campos son obligatorios excepto *baja*.

---

###  **\#6 Baja Sector**

**Como** usuario del sistema  
 **Quiero** dar de baja un sector  
 **Para** impedir que se asignen nuevas mesas o mozos a él

**Prioridad:** Alta 🟥 

**Datos:**

* IdSector

**Criterios de aceptación:**

* No se puede dar de baja un sector que tenga mesas o mozos activos asignados.

* El sistema debe permitir marcar el sector como *baja \= true* sin eliminarlo físicamente.

* Al intentar dar de baja un sector con mesas activas, debe mostrar un mensaje indicando que primero deben reasignarse o darse de baja las mesas.

---

### **\#7 Modificar Sector**

**Como** usuario del sistema  
 **Quiero** modificar la información de un sector existente  
 **Para** mantener actualizados los datos del salón

**Prioridad**: Media 🟧

**Datos:**

* IdSector

* número

**Criterios de aceptación:**

* No debe poder modificarse un sector dado de baja.

* El número del sector no puede duplicarse con otro sector activo.

* Si se cambia el número, el sistema debe verificar que no esté en uso.

---

### **\#8 Listar Sectores**

**Como** usuario del sistema  
 **Quiero** listar todos los sectores registrados  
 **Para** poder visualizar su estado y las mesas que pertenecen a cada uno

**Prioridad**: Media 🟧

**Datos:**

* IdSector

* número

* baja

**Criterios de aceptación:**

* El listado debe incluir todos los sectores, con posibilidad de filtrar por estado (activos/inactivos).

* Debe mostrar también la cantidad de mesas asignadas a cada sector.

* Los sectores dados de baja deben mostrarse con un indicador visual.

---

### **\#9 Listar Mesas Disponibles**

**Como** usuario del sistema  
 **Quiero** consultar qué mesas están disponibles  
 **Para** poder asignarlas a nuevas reservas o comandas

**Prioridad**: Media 🟧 

**Datos:**

* IdMesa

* número

* tipo

* cantidad de comensales

* sector

**Criterios de aceptación:**

* Solo deben listarse las mesas activas (no dadas de baja).

* No deben mostrarse mesas ocupadas ni reservadas para el horario consultado.

* El sistema debe permitir filtrar por cantidad de comensales o sector.

### **\#10 Alta Producto**

**Como** usuario del sistema  
 **Quiero** registrar un nuevo producto (plato, postre, bebida o menú del día)  
 **Para** poder incorporarlo a la carta y a las comandas del restaurante

**Prioridad:** Alta 🟥 

**Datos:**

* IdProducto  
* código  
* nombre  
* precio  
* descripción  
* cm3 (solo para bebidas)  
* IdSeccion  
* Baja

**Criterios de aceptación:**

* El **código del producto debe ser único**. Si ya existe, el sistema debe mostrar un mensaje de advertencia.

* Todos los campos obligatorios deben completarse: nombre, precio, tipo y sección.

* **Validación de precio:** el valor debe ser mayor a 0\.

* **Validación de cm3:** solo aplicable si el tipo es “bebida”; debe ser un número mayor a 0\.

* El producto se registra como activo por defecto.

* Debe existir una **sección** asociada; si no se selecciona, el sistema debe mostrar un error indicando “Debe seleccionar una sección de carta”.

---

### **\#11 Baja Producto**

**Como** usuario del sistema  
 **Quiero** dar de baja un producto existente  
 **Para** que no esté disponible en la carta ni en nuevas comandas

**Prioridad:** Alta **🟥**

**Datos:**

* IdProducto

**Criterios de aceptación:**

* No se debe eliminar el producto físicamente, sino marcarlo como inactivo (*baja \= true*).

* No se puede dar de baja un producto que esté incluido en una comanda abierta o reserva.

---

### 

### 

### 

### 

### **\#12 Modificar Producto**

**Como** usuario del sistema  
**Quiero** modificar los datos de un producto existente  
**Para** mantener actualizada su información en la carta

**Prioridad:** Alta **🟥**

**Datos:**

* IdProducto  
* código  
* nombre

* precio

* descripción

* cm3 (si corresponde)

* IdSeccion

**Criterios de aceptación:**

* Solo se pueden modificar productos activos.

* El sistema debe impedir dejar campos obligatorios vacíos.

* Si se modifica el precio, debe ser un número positivo.

  

---

### **\#13 Listar Productos**

**Como** usuario del sistema  
 **Quiero** listar todos los productos del restaurante  
 **Para** visualizar su estado, precio y tipo

**Prioridad:** Alta **🟥**

**Datos:**

* IdProducto  
* código  
* nombre

* precio

* descripción

* tipo

* sección

* estado (activo/inactivo)

**Criterios de aceptación:**

* El listado debe permitir **filtrar por tipo (plato, postre, bebida)** y por estado.

* Debe permitir **buscar por nombre o descripción**.

* Los productos dados de baja deben mostrarse con un indicador de “inactivo”.

* Se debe poder **ordenar por descripción o nombre**.

---

### 

### 

### 

### **\#14 Alta Sección de Carta**

**Como** usuario del sistema  
 **Quiero** registrar una nueva sección de carta  
 **Para** poder clasificar los productos del restaurante de forma ordenada

**Prioridad:** Alta **🟥**

**Datos:**

* IdSección

* nombre

**Criterios de aceptación:**

* El **nombre de la sección debe ser único**.

* No se puede registrar una sección con el campo “nombre” vacío.

* Se debe registrar con estado activo por defecto.

---

### **\#15 Baja Sección de Carta**

**Como** usuario del sistema  
 **Quiero** dar de baja una sección de carta  
 **Para** impedir que se agreguen nuevos productos a ella

**Prioridad:** Alta **🟥**

**Datos:**

* IdSección

**Criterios de aceptación:**

* No se puede dar de baja una sección que tenga productos activos asociados.

* El sistema debe solicitar confirmación antes de marcarla como inactiva.

* El proceso no elimina la sección, solo la desactiva (*baja \= true*).

---

### **\#16 Modificar Sección de Carta**

**Como** usuario del sistema  
 **Quiero** modificar el nombre de una sección de carta  
 **Para** mantener actualizada la organización de la carta del restaurante

**Prioridad:** Media 🟧 

**Datos:**

* IdSección

* nombre

**Criterios de aceptación:**

* No se debe permitir duplicar el nombre con otra sección activa.

* Solo se pueden modificar secciones activas.

* El campo “nombre” no puede quedar vacío.

---

### **\#17 Listar Secciones de Carta**

**Como** usuario del sistema  
 **Quiero** visualizar todas las secciones de la carta  
 **Para** conocer su estado y los productos asociados

**Prioridad:** Media 🟧

**Datos:**

* IdSección

* nombre

**Criterios de aceptación:**

* Debe incluir la cantidad de productos activos por sección.

---

### **\#18 Consultar Carta**

**Como** usuario del sistema  
 **Quiero** consultar la carta completa del restaurante  
 **Para** visualizar los productos disponibles para la venta agrupados por sección

**Prioridad:** Baja 🟩 

**Datos:**

* sección

* productos (código, nombre, precio, descripción, tipo)

**Criterios de aceptación:**

* Solo deben mostrarse productos activos.

* Los productos deben aparecer agrupados por sección.

* Debe poder filtrarse por tipo de producto o por rango de precio.

* Si una sección no tiene productos activos, debe indicarse “Sin productos disponibles”.

### **\#19 Alta Cliente**

**Como** usuario del sistema  
 **Quiero** registrar un nuevo cliente  
 **Para** poder asociarlo a reservas y comandas en el restaurante

**Prioridad:** Alta **🟥**

**Datos:**

* IdCliente

* documento

* nombre

* apellido

* número de teléfono

* correo electrónico

* baja

**Criterios de aceptación:**

* El **documento del cliente debe ser único**.

* Todos los campos obligatorios (documento, nombre, apellido) deben estar completos.

* El correo debe tener un formato válido (ej: [nombre@dominio.com](mailto:nombre@dominio.com))

### **\#20 Modificar Cliente**

**Como** usuario del sistema  
 **Quiero** modificar un  cliente  
 **Para** poder asociarlo a reservas y comandas en el restaurante

**Prioridad:** Alta **🟥**

**Datos:**

* IdCliente

* documento

* nombre

* apellido

* número de teléfono

* correo electrónico

**Criterios de aceptación:**

* El **documento del cliente debe ser único**.

* Todos los campos obligatorios (documento, nombre, apellido) deben estar completos.

* El correo debe tener un formato válido (ej: nombre@dominio.com)

### **\#21 Baja Cliente**

**Como** usuario del sistema  
 **Quiero** dar de baja un cliente  
 **Para** poder asociarlo a reservas y comandas en el restaurante

**Prioridad:** Alta **🟥**

**Datos:**

* IdCliente  
* Baja

**Criterios de aceptación:**

* El **IdCliente** debe existir.

* El cliente no se puede dar de baja porque posee facturas impagas.

### **\#22 Crear Reserva**

**Como** usuario del sistema  
 **Quiero** registrar una nueva reserva  
 **Para** asignar una mesa a un cliente en una fecha y horario determinado

**Prioridad:** Alta **🟥**

**Datos:**

* IdReserva

* número

* fechaHora

* cantidad de personas

* IdCliente

* IdMesa

* cancelado (Sí/No)

**Criterios de aceptación:**

* La mesa seleccionada debe estar **disponible** en la fecha y horario de la reserva.

* El cliente debe existir y estar activo.

* La cantidad de personas debe ser menor o igual a la capacidad de la mesa.

* Todos los campos son obligatorios excepto *cancelado*, que debe inicializarse en “No”.

* No se puede crear una reserva con fecha pasada.

* El sistema debe guardar la fecha y hora de creación de la reserva.

---

### 

### **\#23 Modificar Reserva**

**Como** usuario del sistema  
 **Quiero** modificar una reserva existente  
 **Para** actualizar su información si cambian los datos del cliente, la mesa o la fecha

**Prioridad:** Media 🟧

**Datos:**

* IdReserva

* fechaHora

* cantidad de personas

* idCliente

* idMesa

**Criterios de aceptación:**

* Solo se pueden modificar reservas activas (no canceladas).

* No se pueden asignar mesas ya reservadas o ocupadas en el nuevo horario.

* El sistema debe validar que la nueva cantidad de personas no supere la capacidad de la mesa.

* Si se cambia la fecha, debe ser futura.

* Se debe registrar la fecha y hora de modificación.

---

### **\#24 Cancelar Reserva Anticipada**

**Como** usuario del sistema  
 **Quiero** cancelar una reserva antes de la fecha programada  
 **Para** liberar la mesa y registrar el motivo de cancelación

**Prioridad**: Media 🟧

**Datos:**

* IdReserva

* motivo de cancelación

**Criterios de aceptación:**

* Solo se pueden cancelar reservas con estado “activa”.

* El campo “motivo” debe ser obligatorio.

* El sistema debe marcar la reserva como *cancelado \= Sí* y liberar la mesa asociada.

* Si la reserva tenía una **seña paga**, el sistema debe registrar si corresponde devolverla o mantenerla según la política del restaurante.

---

### **\#25 Cancelar Reserva por Ausencia**

**Como** usuario del sistema  
 **Quiero** cancelar una reserva cuando el cliente no se presenta  
 **Para** registrar la ausencia y liberar la mesa para otros clientes

**Prioridad**: Media 🟧

**Datos:**

* idReserva

**Criterios de aceptación:**

* Solo se pueden marcar como “canceladas por ausencia” las reservas cuya hora ya haya pasado y que no se hayan confirmado en el sistema como “asistidas”.

* El sistema debe cambiar el estado de la reserva a *cancelado \= Sí* y liberar la mesa.

* Si existía una seña asociada, debe registrarse como “no recuperada”.

* El sistema debe guardar la fecha y hora de la cancelación automática o manual.

---

### **\#26 Listar Reservas**

**Como** usuario del sistema  
 **Quiero** visualizar todas las reservas registradas  
 **Para** consultar su estado, fecha, cliente y mesa asignada

**Prioridad:** Alta **🟥**

**Datos:**

* idReserva

* número

* fechaHora

* cantidad de personas

* cliente (nombre, apellido)

* mesa (número, sector)

* estado (activa, cancelada, por ausencia)

**Criterios de aceptación:**

* El listado debe permitir filtrar por **fecha, cliente o estado**.

* Las reservas canceladas o por ausencia deben mostrarse con un indicador visual.

* Debe poder ordenarse por fecha o número de reserva.

* El sistema debe permitir acceder al detalle de cada reserva.

---

### **\#27 Crear Comanda con Reserva**

**Como** mozo del sistema  
 **Quiero** crear una comanda asociada a una reserva existente  
 **Para** registrar los pedidos del cliente al llegar al restaurante

**Prioridad:** Media 🟧

**Datos:**

* idComanda

* idReserva

* idMesa

* idMozo

* fecha

* lista de productos (idProducto, cantidad, precioUnitario)

**Criterios de aceptación:**

* Solo se puede crear una comanda para reservas con estado “activa” y “asistida”.

* La mesa y el cliente deben coincidir con los datos de la reserva.

* La comanda debe generarse automáticamente con la información de la reserva.

* No se pueden incluir productos inactivos.

* Al confirmar, la reserva debe pasar a estado “en curso” y la mesa a “ocupada”.

* El sistema debe calcular el total de la comanda y permitir cerrarla como cualquier otra.

* Primero la reserva debe marcarse como "Asistida" (el cliente llegó) y luego, al crear la comanda, pasa a "En Curso"

### **\#28 Cobrar Factura Adeudada**

**Como** usuario del sistema  
 **Quiero** registrar el cobro de una factura pendiente  
 **Para** actualizar el estado de la deuda y asociar el medio de pago utilizado

**Prioridad:** Media 🟧

**Datos:**

* idFactura

* idCliente

* fechaPago

* montoPagado

* idMedioPago

* número de comprobante (si aplica)

**Criterios de aceptación:**

* Solo se pueden cobrar facturas con estado “pendiente” o “parcialmente pagada”.

* El monto abonado no puede exceder el saldo restante de la factura.

* El sistema debe actualizar automáticamente el estado de la factura (por ejemplo, “pagada” o “parcial”).

* Debe quedar registrado el medio de pago utilizado y la fecha del cobro.

* Si el medio de pago requiere comprobante (ej. tarjeta, transferencia), el número debe ser obligatorio.

* El sistema debe permitir imprimir o generar un comprobante de pago.

---

### **\#29 Alta Medio de Pago**

**Como** usuario del sistema  
 **Quiero** registrar un nuevo medio de pago  
 **Para** poder ofrecerlo al momento de cobrar facturas o generar comprobantes

**Prioridad:** Alta 🟥

**Datos:**

* idMedioPago

* nombre

* tipo (efectivo, tarjeta, transferencia, billetera virtual, etc.)

* activo (Sí/No)

**Criterios de aceptación:**

* No puede crearse un medio de pago con nombre duplicado.

* Todos los campos son obligatorios excepto *activo*, que debe inicializarse en “Sí”.

* El tipo debe seleccionarse de una lista predefinida.

* El sistema debe guardar la fecha y usuario que creó el medio de pago.

---

### **\#30 Baja Medio de Pago**

**Como** usuario del sistema  
 **Quiero** dar de baja un medio de pago  
 **Para** evitar que siga apareciendo entre las opciones disponibles al cobrar

**Prioridad:** Alta 🟥

**Datos:**

* idMedioPago

**Criterios de aceptación:**

* Solo pueden darse de baja los medios de pago que no tengan movimientos pendientes.

* El sistema debe solicitar confirmación antes de proceder.

* En lugar de eliminar el registro, debe marcarse como *activo \= No*.

* Debe registrarse la fecha y usuario que realizó la baja.

---

### **\#31 Modificar Medio de Pago**

**Prioridad:** Media 🟧

**Como** usuario del sistema  
 **Quiero** modificar los datos de un medio de pago existente  
 **Para** actualizar su nombre, tipo o estado si cambia la política del restaurante

**Datos:**

* idMedioPago

* nombre

* tipo

* activo

**Criterios de aceptación:**

* No se puede cambiar el tipo si el medio ya fue utilizado en facturas históricas.

* El nuevo nombre no debe duplicar otro medio de pago activo.

* Se debe registrar la fecha y usuario de la modificación.

* Si se desactiva, el sistema debe mostrar una advertencia sobre facturas pendientes asociadas.

---

### **\#32 Listar Medios de Pago**

**Como** usuario del sistema  
 **Quiero** ver todos los medios de pago registrados  
 **Para** consultar cuáles están disponibles y su estado actual

**Prioridad:** Alta 🟥

**Datos:**

* idMedioPago

* nombre

* tipo

* activo

**Criterios de aceptación:**

* El listado debe permitir filtrar por *tipo* y *estado*.

* Los medios de pago inactivos deben visualizarse diferenciados (por color o etiqueta).

* Debe poder ordenarse por nombre o tipo.

* El sistema debe permitir acceder a la opción de modificar o reactivar cada medio.

---

## **\#33 Alta Mozo**

**Como** administrador del sistema  
 **Quiero** registrar un nuevo mozo con sus datos personales y sector asignado  
 **Para** poder incorporarlo al sistema y asignarle mesas según su sector

**Prioridad:** Alta 🟥

**Datos:**

* idMozo

* Documento

* Nombre y Apellido

* Dirección

* Teléfono

* idSector

* Activo (por defecto en “Sí”)

**Criterios de aceptación:**

* Todos los campos obligatorios deben validarse antes del alta.

* No se debe permitir registrar dos mozos con el mismo número de documento.

* El sistema debe confirmar la creación con un mensaje de éxito.

* El mozo debe quedar automáticamente disponible en su sector asignado.

---

## **\#34 Baja Mozo**

**Como** administrador del sistema  
 **Quiero** poder dar de baja un mozo  
 **Para** reflejar que ya no se encuentra activo en el restaurante

**Prioridad:** Alta 🟥

**Datos:**

* idMozo

* Estado (activo/inactivo)

**Criterios de aceptación:**

* La baja no debe eliminar los datos, solo marcar al mozo como inactivo.

* No se debe permitir asignar mesas ni comandas a mozos inactivos.

* El sistema debe pedir confirmación antes de realizar la baja.

* Debe mostrarse un mensaje indicando que la baja se realizó correctamente.

---

## **\#35 Modificar Mozo**

**Como** administrador del sistema  
 **Quiero** editar los datos personales o el sector de un mozo existente  
 **Para** mantener actualizada su información en el sistema

**Prioridad:** Alta 🟥

**Datos:**

* idMozo

* Documento

* Nombre y Apellido

* Dirección

* Teléfono

* idSector

* Estado (activo/inactivo)

**Criterios de aceptación:**

* Solo los mozos activos pueden modificarse.

* Los cambios deben registrarse con trazabilidad (fecha de modificación).

* El sistema debe validar duplicados de documento antes de guardar.

* Al guardar, se debe mostrar un mensaje confirmando la modificación exitosa.

---

## **\#36 Listar Mozos**

**Como** usuario del sistema  
 **Quiero** ver todos los mozos registrados  
 **Para** consultar su información y estado actual

**Prioridad:** Alta 🟥

**Datos:**

* idMozo

* Documento

* Nombre y Apellido

* Dirección

* Teléfono

* idSector

* Estado (activo/inactivo)

**Criterios de aceptación:**

* El listado debe permitir filtrar por sector y estado (activo/inactivo).

* Los mozos inactivos deben visualizarse diferenciados (por color o etiqueta).

* Debe poder ordenarse por nombre o documento.

* El sistema debe permitir acceder a las opciones de modificar o reactivar cada mozo.

---

## **\#35 Crear Comanda Restaurante**

**Como** mozo o encargado del salón  
 **Quiero** crear una nueva comanda asociada a una mesa y un mozo  
 **Para** registrar los pedidos realizados por los clientes

**Prioridad:** Media 🟧

**Datos:**

* idComanda

* Fecha

* idMesa

* idPreTicket

* idMozo

**Criterios de aceptación:**

* La comanda solo puede crearse si la mesa está ocupada y sin comanda abierta.

* Debe asociarse automáticamente al mozo que atiende la mesa.

* El sistema debe permitir agregar productos y cantidades al crearla.

* Al guardar, debe mostrarse el número de comanda y su estado inicial ("Abierta").

---

## **\#36 Modificar Comanda Restaurante**

**Como** mozo  
 **Quiero** modificar una comanda abierta  
 **Para** actualizar los pedidos del cliente antes del cierre o facturación

**Prioridad:** Media 🟧

**Datos:**

* idComanda

* Fecha

* idMesa

* idPreTicket

* idMozo

**Criterios de aceptación:**

* Solo pueden modificarse comandas con estado “Abierta”.

* El sistema debe registrar los cambios realizados (producto agregado, eliminado o cantidad modificada).

* No se permite modificar una comanda ya cerrada o cancelada.

* Debe mostrarse un mensaje confirmando la modificación exitosa.

---

## **\#37 Cancelar Comanda Restaurante**

**Como** mozo o administrador  
 **Quiero** poder cancelar una comanda abierta  
 **Para** anular pedidos erróneos o mesas que se retiraron sin consumir

**Prioridad:** Media 🟧

**Datos:**

* idComanda

* Motivo de cancelación

* Estado (Cancelada)

**Criterios de aceptación:**

* El sistema debe solicitar confirmación y motivo antes de cancelar.

* Una comanda cancelada no puede reabrirse ni facturarse.

* Los productos asociados deben revertirse al stock (si aplica).

* Debe quedar registrada la fecha y usuario que realizó la cancelación.

---

## **\#38 Cerrar Comanda**

**Como** mozo o encargado  
 **Quiero** cerrar una comanda cuando los clientes terminan su consumo  
 **Para** proceder con la generación del pre-ticket o la factura final

**Prioridad:** Media 🟧

**Datos:**

* idComanda

* Fecha cierre

* idPreTicket

* Estado (Cerrada)

**Criterios de aceptación:**

* Solo pueden cerrarse comandas con todos los productos entregados.

* El cierre debe generar un pre-ticket vinculado.

* No se deben permitir modificaciones posteriores al cierre.

* El sistema debe mostrar confirmación de cierre exitoso.

# **Diagrama de clases**

[https://app.diagrams.net/?splash=0\#G1MIpXCsPmHNTZ6HTz7WV3cBhVFEPTzu81\#%7B%22pageId%22%3A%22YnwQl8CMOVd9g4ci0JJN%22%7D](https://app.diagrams.net/?splash=0#G1MIpXCsPmHNTZ6HTz7WV3cBhVFEPTzu81#%7B%22pageId%22%3A%22YnwQl8CMOVd9g4ci0JJN%22%7D)

---

# **Requerimientos NO funcionales**

La aplicación se desarrollará utilizando las siguientes tecnologías:

* **Lenguaje de programación:** Python (Versión 3.11 o superior).  
* **Framework Backend:** Flask (Última versión).  
* **Base de datos**: PostgreSQL (relacional).  
* **Contenerización:** Docker (última versión), utilizando contenedores independientes para el frontend, backend y la base de datos.  
* **Framework Frontend**: React (JavaScript)  
* **Interfaz de usuario (UI):** Bootstrap?? React  
* **Sistema operativo:** Windows, Linux (cualquier distribución).  
* **Comunicación backend-frontend:** Mediante API Rest.

**Navegadores?**

(Correciones))

#### **Legibilidad**

El código tiene que ser fácil de leer y entender.  
 Ejemplo: nombres de variables claros, comentarios útiles, indentación prolija.

#### **Diseño del código**

La estructura del codigo va a ser: 

* separación en módulos,

* funciones cortas y con un único propósito,

* uso adecuado de clases si corresponde,

* evitar repetir código, etc.

#### **Convenciones de nomenclatura**

Seguir las convenciones estándar de Python (PEP8):

* variables y funciones: `minusculas_con_guiones_bajos`

* clases: `MayusculaInicial`

* constantes: `MAYUSCULAS`

---

 Herramientas de estandarización

Son herramientas automáticas para **comprobar y corregir el estilo** del código:

* **PyLint** → analiza el código y te marca advertencias o errores de estilo o lógica.

* **Flake8** → más liviana, también revisa errores de formato y estilo.

* **Black** → formatea automáticamente el código para cumplir el estándar PEP8.

---

| Requerimiento | Significado |
| ----- | ----- |
| **Python 3.11+** | versión mínima del lenguaje |
| **Flask** | framework del backend |
| **PostgreSQL** | base de datos relacional |
| **Docker** | monorepo (backend, frontend y DB) |
| **React (JavaScript)** | framework del frontend |
| **Bootstrap** | para el diseño visual de la UI  |
|  |  |
| **API REST** | comunicación entre backend y frontend por HTTP (GET, POST, etc.) |
| **Navegadores** | Firefox, Brave, Edge, Chrome |

**Decisiones de diseño**

Para el desarrollo del sistema se adoptó una arquitectura monolítica, en la cual todos los componentes del backend se integran dentro de una misma aplicación desarrollada con Flask. Esta decisión se tomó debido a la simplicidad que ofrece este enfoque para la implementación, el despliegue y el mantenimiento en proyectos de pequeña y mediana escala.

El frontend se implementará utilizando React, lo que permite una interfaz de usuario dinámica, moderna y fácilmente escalable. La comunicación entre el frontend y el backend se realizará mediante peticiones HTTP a través de una API REST, utilizando el formato JSON para el intercambio de datos.

Como sistema gestor de base de datos se seleccionó PostgreSQL, dado su buen rendimiento, confiabilidad y soporte para transacciones complejas y relaciones entre tablas.

En conjunto, estas decisiones de diseño buscan lograr una aplicación coherente, de fácil mantenimiento y con una clara separación entre la lógica del servidor y la interfaz de usuario, garantizando además una buena experiencia de uso y una estructura tecnológica sólida.

---

# **Puntos de función**

## Ficheros Lógicos 

| *Ficheros lógicos* |  |  |  |
| ----- | :---- | :---- | ----- |
| **Ficheros** | **DET** | **RET** | **PF (Complejidad)** |
| Cliente | 7 | 1 | Baja \= 7 |
| Reserva | 16 | 4 | Baja \= 7 |
| Sector | 3 | 1 | Baja \= 7 |
| Mozo | 6 | 1 | Baja \= 7 |
| Mesa | 6 | 1 | Baja \= 7 |
| Seña | 4 | 1 | Baja \= 7 |
| Comanda | 10 | 1 | Baja \= 7 |
| PreTicket | 9 | 1 | Baja \= 7 |
| Factura | 6 | 1 | Baja \= 7 |
| Pago | 5 | 1 | Baja \= 7 |
| MedioPago | 2 | 1 | Baja \= 7 |
| Sección | 2 | 1 | Baja \= 7 |
| Producto | 11 | 4 | Baja \= 7 |
|  |  | Total | … |

1. **Cliente:**	  
   **Atributos:** IdCliente, documento, nombre, apellido, num, correo, baja.  
   **Clases involucradas:** Cliente  
2. **Reserva:** 	  
   **Atributos:** idReserva, numero, fechaHora, cantPersonas, idCliente, idMesa, cancelado(Si/No),idMenuReserva,montoseña,paga(SI/NO),idSeña,monto, fecha, idDetalleMenuReserva, idProducto, cantidad, precioUnitario.  
   **Clases involucradas:** Reserva, Menu reserva, Detalle del menú, seña.  
3. **Sector:**	  
   **Atributos:** IdSector, numero, baja.  
   **Clases involucradas:** Sector  
4. **Mozo:**	  
   **Atributos:** idMozo, documento, nombreYapellido, direccion, tel, idSector, baja.  
   **Clases involucradas:** Mozo.  
5. **Mesa:**   
   **Atributos:** idMesa, numero, tipo, cantComensales, idSector, baja  
   **Clases involucradas:** Mesa, Sector.  
6. **MenuReserva:**   
   **Atributos:** idMenuReserva, montoSeña, seña(Paga/No Paga)  
   **Clases involucradas:** MenuReserva.  
7. **Comanda:**   
   **Atributos:** IdComanda, fecha.  
   **Clases involucradas:** Comanda.  
8. **DetalleMenuReserva:**   
   **Atributos:** idDetalleMenuReserva, idProducto, idMenuReserva, cant, precioUnitario.  
   **Clases involucradas:** DetalleMenuReserva, Producto, MenuReserva.  
9. **Seña:**   
   **Atributos:** idSeña,monto, fecha, idMenuReserva.  
   **Clases involucradas:** Seña, MenuReserva  
10. **DetalleComanda:**   
    **Atributos:** idDetalleComanda, idProducto, cant, idDetalleReserva, idComanda.  
    **Clases involucradas:** DetalleComanda, Producto, DetalleReserva.  
11. **PreTicket:**   
    **Atributos:** codigo, fecha, montoTotal   
    **Clases involucradas:** PreTicket.  
12. **DetallePreTicket:**   
    **Atributos:** cod, fecha, idPreTicket.  
    **Clases involucradas:** PreTicket, DetallePreTicket.  
13. **Factura:**   
    **Atributos:** idFactura, codigo, monto, fecha.  
    **Clases involucradas:** Factura  
14. **DetalleFactura:**   
    **Atributos:** codigo, fecha, idFactura.  
    **Clases involucradas:** DetalleFactura, Factura**.**  
15. **Pago:**   
    **Atributos:** codigo, fecha, idFactura.  
    **Clases involucradas:** Pago, Factura.  
16. **MedioPago:**   
    **Atributos:** codigoMedioPago, nombre.  
    **Clases involucradas:** MedioPago  
17. **Producto:**   
    **Atributos:** idProducto, codigo, nombre, precio, idSeccion, descripcion, baja, idPlato, idPostre, idBebida, cm3.  
    **Clases involucradas:** Producto, Plato, Postre, Bebida.  
18. **Sección:**   
    **Atributos:** idSeccion, nombre.  
    **Clases involucradas:** Sección.

## Entradas del sistema

| Entradas del sistema |  |  |  |
| ----- | :---- | :---: | :---: |
| **Requerimientos** | **DET (atributos)** | **RET(ficheros)** | **PF(Complejidad)** |
| Alta mesa | 6 \+ error existe | 2 |  Baja |
| Modificar mesa | 5 \+ error \+ sector no existe | 2 | Baja |
| Baja mesa | 1,6 \+ error no existe | 1 | Baja |
| Alta Sector | 3 \+ error existe | 1 | Baja |
| Modificar Sector | 2 \+ error no existe  | 1 | Baja |
| Baja Sector | 2 \+ error no existe \+ mesa asociada \+ mozo asociado | 3 | Media |
| Alta Mozo | 7 \+ error existe \+ sector no existe | 2 | Baja |
| Modificar Mozo | 6 \+ error no existe \+ sector no existe | 2 | Baja |
| Baja Mozo | 2 \+ error no existe | 1 | Baja |
| Alta Cliente | 7 \+ error existe | 1 | Baja |
| Modificar Cliente | 6 \+ error no existe | 1 | Baja |
| Baja Cliente | 2 \+ error no existe \+ error facturas impagas | 3 | Media |
| Alta Sección | 3 \+ error existe | 1 | Baja |
| Modificar Sección | 2 \+ error no existe | 1 | Baja |
| Baja Sección | 2 \+ error no existe | 1 | Baja |
| Alta Producto | 11 \+ error ya existe \+ sección no existe | 2 | Baja |
| Modificar Producto | 10 \+ error no existe \+ sección no existe | 2 | Baja |
| Baja Producto | 2 \+ error producto en reserva | 2 |  |
| Alta Medio Pago | 3 \+ error ya existe | 1 | Baja |
| Modificar Medio Pago | 2 \+ error no existe | 1 | Baja |
| Baja Medio Pago | 2 \+ error no existe | 1 | Baja |
| Crear comanda | 10 \+ 6 errores | 10 | Alta |
| Modificar comanda | 10 \+ 6 errores | 10 | Alta |
| Cerrar comanda | 10 \+ 6 errores  | 10 | Alta |
| Agregar producto | 5 \+ 4 errores | 5 | Alta |
| Crear factura con pre-ticket | 9 \+ 2 errores | 2 | Media |
| Crear reserva | 16 \+ 7 errores | 4 | Alta |
| Modificar reserva | 16 \+ 7 errores | 4 | Alta |
| Cancelar reserva anticipada | 2 \+ 1 error | 1 | Baja |
| Cancelar reserva por ausencia | 2 \+ 1 error  | 1 |  Baja  |
| Crear comanda con reserva  | 10 \+ 5 errores | 4 | Media |
| Gestion de pagos | 6 \+ 3 errores | 3 | Alta |
| Cobrar factura adeudada | Preguntar5 | Preguntar2 | Preguntarq\\Baja |

1. **Alta mesa**  
   Atributos: idMesa, numero, tipo, cantComensales, idSector, baja  
   Clases involucradas: Mesa , Sector   
   Posibles mensajes de error:  
   * “La mesa ya existe”	  
   * “El sector no existe”

2. **Baja mesa**  
   Atributos: idMesa, baja  
   Clases involucradas: Mesa, Sector  
   Posibles mensajes de error:  
   * “La mesa no existe”

   

3. **Alta sector**   
   Atributos: idSector, numero, baja.  
   Clases involucradas: Sector  
   Posibles mensajes de error:  
   * El campo *baja* debe inicializarse como *false*.

   * Validación de duplicados: no se puede registrar un sector con un número ya existente.

   * Todos los campos son obligatorios excepto *baja*.

   

4. **Modificar sector**   
   Atributos:IdSector,numero  
   Clases involucradas: Sector  
   Posibles mensajes de error:  
   * El número del sector no puede duplicarse con otro sector activo.  
   * Si se cambia el número, el sistema debe verificar que no esté en uso.  
   * No debe poder modificarse un sector dado de baja.

   

5. **Baja sector**   
   Atributos: idSector, baja  
   Clases involucradas: Sector  
   Posibles mensajes de error:  
   * No se puede dar de baja un sector que tenga mesas o mozos activos asignados.

   * El sistema debe permitir marcar el sector como *baja \= true* sin eliminarlo físicamente.

   * Al intentar dar de baja un sector con mesas activas, debe mostrar un mensaje indicando que primero deben reasignarse o darse de baja las mesas.

6. **Alta Medio de Pago**   
   Atributos: idMedioPago, nombre,tipo,activo  
   Clases involucradas: Medio Pago  
   Posibles mensajes de error:  
   * No se puede dar de baja un sector que tenga mesas o mozos activos asignados.

   * El sistema debe permitir marcar el sector como *baja \= true* sin eliminarlo físicamente.

   * Al intentar dar de baja un sector con mesas activas, debe mostrar un mensaje indicando que primero deben reasignarse o darse de baja las mesas.

7. **Baja Medio de Pago**   
   Atributos: idSector, baja  
   Clases involucradas: Sector  
   Posibles mensajes de error:  
   * No se puede dar de baja un sector que tenga mesas o mozos activos asignados.

   * El sistema debe permitir marcar el sector como *baja \= true* sin eliminarlo físicamente.

   * Al intentar dar de baja un sector con mesas activas, debe mostrar un mensaje indicando que primero deben reasignarse o darse de baja las mesas.

8. **Modificar Medio de Pago** 

Atributos: idSector, baja  
	Clases involucradas: Sector  
	Posibles mensajes de error:

* No se puede dar de baja un sector que tenga mesas o mozos activos asignados.

  * El sistema debe permitir marcar el sector como *baja \= true* sin eliminarlo físicamente.

  * Al intentar dar de baja un sector con mesas activas, debe mostrar un mensaje indicando que primero deben reasignarse o darse de baja las mesas.

9. Cobrar Factura adeudada  
10.   
    Atributos: idFactura, idPago, idMedioPago, monto, fecha  
    Clases involucradas: Factura, Pago  
    Posibles mensajes de error:  
* Factura no existe  
* Pago existe  
* medio de pago existe

	

## Consultas Externas:

| Consulta Externa |  |  |  |
| ----- | :---- | :---- | :---- |
| **Requerimientos** | **DET** | **RET** | **PF(Complejidad)** |
| Listar Sectores | 3 | 1 | Baja(3) |
| Listar Mesas | 5 | 1 | Baja(3) |
| Listar Mesas Disponibles | 6 | 1 | Baja(3) |
| Listar Productos | 8 |  1 | Baja(3) |
| Listar Secciones de Carta | 2 | 1 | Baja(3) |
| Listar Reservas | 7 | 2 | Media(4) |
| Listar Medios De Pago | 4 | 1 | Baja (3) |
| TOTAL |  |  |  |

## 

## Salidas Externas:	

| Salida Externa |  |  |  |
| ----- | :---- | :---- | :---- |
| **Requerimientos** | **DET** | **RET** | **PF(Complejidad)** |
| Total de factura | 4 | 2 | Baja(4) |
| Producto más vendido  |  |  |  |
| TOTAL |  |  |  |

## Puntos de función ajustados

| Características Generales del Sistema (GSC’s) | Puntaje |
| ----- | :---: |
| Comunicación de datos | 2 |
| Procesamiento de datos distribuido | 2 |
| Rendimiento | 3 |
| Hardware Existente | 1 |
| Transacciones | 3 |
| Entrada de datos Interactiva | 5 |
| Eficiencia | 4 |
| Actualizaciones on-line | 3 |
| Complejidad de procesamiento | 2 |
| Reusabilidad | 0 |
| Facilidad de instalación | 4 |
| Facilidad de operación | 4 |
| Múltiples instalaciones | 0 |
| Facilidad de mantenimiento | 3 |
| **Factor de ajuste** | 0,36 |

## Cálculo de los puntos de función

|  |  |
| :---- | :---- |
|  |  |
|  |  |
|  |  |

Para calcular el esfuerzo tenga e n cuenta que la productividad promedio que tenemos en la materia es de 2 horas por PFA

Pueden consultar lo siguiente para hacer una comparativa y ver al final cuál sería la estimación más acertada https://www.fattocs.com/es/blog-es/cual-es-la-productividad-del-punto-de-funcion-para-estimar-el-esfuerzo/