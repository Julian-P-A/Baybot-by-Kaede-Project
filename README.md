# 🚀 Discord Task Management Bot – MVP

**Autor:** Julian Camilo Pinzón Ariza  
**Año:** 2025  
**Licencia:** Todos los derechos reservados (ver sección de licencia)

---

## 1️⃣ Objetivo

Este bot de Discord permite a equipos gestionar tareas sin salir de Discord, integrando:

- Canales tipo foro + threads  
- Google Calendar para fechas de entrega  
- Notificaciones automáticas  
- Estados de tarea: `pendiente`, `revisión`, `cambios`, `completada`  

Funciona de manera eficiente, sin procesos constantes, reaccionando únicamente a:

- Comandos humanos  
- Eventos de Discord  
- Webhooks de Google Calendar  

---

## 2️⃣ Alcance del MVP

Desde Discord, el bot permite:

- Crear tareas y asignar responsables  
- Definir fecha de entrega  
- Crear automáticamente un thread para cada tarea  
- Crear evento en Google Calendar  
- Cambiar estados de tarea  
- Notificar al jefe en:  
  - Entrega marcada por un empleado  
  - Fecha vencida sin cierre  
- Consultar tareas del día  

**Administración:**  

- Dueño del servidor = Jefe automático  
- El jefe puede ascender otros usuarios a Manager o Jefe  
- Empleados se registran automáticamente al ejecutar cualquier comando  

---

## 3️⃣ Flujo de Usuario (resumido)

### 🧠 Crear tarea
- El jefe ejecuta `/tarea crear`  
- El bot:  
  - Crea registro en la base de datos  
  - Crea thread en el foro configurado  
  - Publica mensaje inicial en el hilo  
  - Crea evento en Google Calendar y guarda el ID  
  - Asigna responsables  
  - Marca estado `pendiente`  

### 🏁 Empleado entrega
- En el thread ejecuta `/tarea completar`  
- El bot:  
  - Cambia estado → `revision`  
  - Notifica al jefe por DM o canal privado  
  - Añade registro en `task_history`  

### 🧑‍💼 Jefe revisa
- Si aprueba → `completada`  
- Si devuelve → `cambios` y asigna nueva fecha  

### ⏰ Fecha vencida
- Webhook de Google Calendar avisa  
- El bot revisa estado y si sigue en `pendiente` o `cambios` → notifica al jefe  

---

## 4️⃣ Roles y permisos

| Rol       | Permisos                                               |
|----------|--------------------------------------------------------|
| Jefe     | Todos los comandos                                     |
| Manager  | Revisar, aprobar, devolver, ver reportes              |
| Empleado | Completar tarea, agregar notas, consultar tareas      |

**Asignación inicial:**

- Owner → Jefe  
- Todos los demás → Empleado  

**Comando para ascender:**
```bash
/promover @usuario rol

## 5️⃣ Comandos del Bot

### 📍 Tareas
- `/tarea crear` – Crear nueva tarea
- `/tarea completar` – Completar tarea (solo empleado asignado)
- `/tarea revisar` – Revisar tarea (solo jefe o manager)
- `/tarea devolver` – Devolver tarea a estado `cambios`
- `/tarea info` – Muestra estado, responsables, fecha, historial
- `/hoy` – Lista tareas activas con vencimiento hoy o atrasadas

### ⚙️ Configuración
- `/config google` – Vincula Google Calendar
- `/config foro` – Define canal de threads
- `/promover @user rol` – Asigna rol: jefe, manager o empleado

---

## 6️⃣ Base de Datos

### Tabla `users`
| Campo       | Tipo                         |
|------------|-------------------------------|
| id         | PK                            |
| discord_id | string                        |
| servidor_id| string                        |
| nombre     | string                        |
| rol        | enum `jefe/manager/empleado` |
| creado_en  | timestamp                     |

### Tabla `tasks`
| Campo           | Tipo                         |
|----------------|-------------------------------|
| id              | PK                            |
| servidor_id     | string                        |
| titulo          | string                        |
| estado          | enum `pendiente/revision/cambios/completada` |
| responsables    | array de discord_id (json)    |
| fecha_entrega   | date                          |
| id_thread       | string                        |
| id_google_event | string                        |
| created_by      | discord_id                    |
| created_at      | timestamp                     |
| updated_at      | timestamp                     |

### Tabla `task_history`
| Campo          | Tipo                              |
|---------------|----------------------------------|
| id             | PK                               |
| task_id        | FK                               |
| accion         | enum `creada/entregada/aprobada/devuelta/atrasada/nota` |
| ejecutada_por  | discord_id                        |
| fecha          | timestamp                         |
| descripcion    | string (opcional)                 |

---

## 7️⃣ Estructura del Proyecto (Python)

bot/
├─ main.py
├─ config.py
├─ commands/
│ ├─ tareas.py
│ ├─ configuracion.py
│ ├─ permisos.py
├─ services/
│ ├─ calendar_service.py
│ ├─ discord_service.py
│ ├─ scheduler_service.py
├─ db/
│ ├─ models.py
│ ├─ database.py
├─ utils/
│ ├─ permissions.py
│ ├─ logger.py
└─ requirements.txt

---

