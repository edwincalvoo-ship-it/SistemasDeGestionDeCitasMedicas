# '[HU-001] Gestión de Citas Médicas'

## 📖 Historia de Usuario

Como paciente  
Quiero poder consultar la disponibilidad de citas médicas  
Para reservar una cita en el horario que más me convenga

## 🔁 Flujo Esperado

- El usuario selecciona la especialidad médica y la fecha deseada desde la interfaz.  
- El sistema consume el endpoint `/api/v1/citas/disponibilidad?especialidad=XXX&fecha=YYYY-MM-DD`.  
- El backend consulta la base de datos de agendas médicas filtrando por especialidad y fecha.  
- Se retornan los horarios disponibles para esa especialidad en la fecha solicitada.  

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint GET con parámetros `especialidad` y `fecha`.  
- [ ] Se valida que existan médicos disponibles para la especialidad solicitada.  
- [ ] Se verifica que la fecha sea futura y válida.  

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "mensaje": "Consulta de disponibilidad exitosa",
  "data": {
    "especialidad": "Cardiología",
    "fecha_consulta": "2025-09-25",
    "horarios_disponibles": ["08:00", "09:30", "11:00", "14:00", "15:30"],
    "medicos_disponibles": 3
  },
  "success": true
}
```


- [ ] Si no existen datos, el backend retorna:

```json
{
  "mensaje": "No hay horarios disponibles para la especialidad y fecha indicada",
  "data": {
    "especialidad": "Cardiología",
    "fecha_consulta": "2025-09-25",
    "horarios_disponibles": [],
    "medicos_disponibles": 0
  },
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Consulta del Último Cierre

-Endpoint – Consulta de Disponibilidad de Citas
-Método HTTP: GET

-Ruta: /api/v1/citas/disponibilidad
## 📤 Ejemplo de Respuesta JSON

````json

```json
{
  "mensaje": "Consulta de disponibilidad exitosa",
  "data": {
    "especialidad": "Cardiología",
    "fecha_consulta": "2025-09-25",
    "horarios_disponibles": ["08:00", "09:30", "11:00"],
    "medicos_disponibles": 2
  },
  "success": true
}

````

- [ ] Si no existen datos, el backend retorna:

```json
{
  "mensaje": "No hay horarios disponibles para la especialidad y fecha indicada",
  "data": {
    "especialidad": "Cardiología",
    "fecha_consulta": "2025-09-25",
    "horarios_disponibles": [],
    "medicos_disponibles": 0
  },
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: 

Caso 1: Consulta exitosa con horarios disponibles

-Precondición: Existen médicos de cardiología con horarios disponibles para la fecha 2025-09-25.
-Acción: Ejecutar el endpoint GET /api/v1/citas/disponibilidad?especialidad=Cardiología&fecha=2025-09-25.
-Resultado esperado:
-Código HTTP 200 OK
-Campo horarios_disponibles contiene al menos un horario
-Campo medicos_disponibles mayor a 0
-Campo success con valor true

  ### ✅ Caso 2:
  
*Consulta sin horarios disponibles
-Precondición: No hay médicos de dermatología disponibles para la fecha 2025-09-25.
-Acción: Ejecutar el endpoint GET /api/v1/citas/disponibilidad?especialidad=Dermatología&fecha=2025-09-25.
-Resultado esperado:
Código HTTP 200 OK

### ✅ Caso 3: 

*Precondición: Ejecución exitosa del endpoint.
-Resultado esperado: La respuesta JSON debe contener exactamente los campos:
-"especialidad" (texto)
-"fecha_consulta" (texto en formato YYYY-MM-DD)
-"horarios_disponibles" (array de textos)
-"medicos_disponibles" (número entero)
-"mensaje" (texto)

  ### ❌ Caso 4: 
-Precondición: El usuario envía el parámetro fecha con formato incorrecto.
-Acción: Ejecutar el endpoint GET /api/v1/citas/disponibilidad?especialidad=Cardiología&fecha=25-09-2025.
-Resultado esperado:
-Código HTTP 400 Bad Request
-Campo mensaje contiene el texto: "Formato de fecha no válido. Debe ser YYYY-MM-DD"

  ### ❌ Caso 5: 

-Precondición: El usuario consulta una especialidad que no existe en el sistema.
-Acción: Ejecutar el endpoint GET /api/v1/citas/disponibilidad?especialidad=EspecialidadInexistente&fecha=2025-09-25.
-Resultado esperado:
-Código HTTP 404 Not Found
-Campo mensaje contiene el texto: "Especialidad médica no encontrada"

## ✅ Definición de Hecho

#Historia: Consulta de Disponibilidad de Citas Médicas

## 📦 Alcance Funcional

- [ ] El endpoint entrega información correctamente en base a especialidad y fecha
- [ ] Los horarios disponibles son exactos y están en formato correcto
- [ ] La respuesta JSON cumple con el contrato definido

  ## 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para validar la lógica de disponibilidad
- [ ] Se cubrieron los casos de error y respuesta sin datos
- [ ] Las pruebas funcionales están documentadas y pasadas.

  ## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:

  - Propósito del endpoint
  - Campos de entrada y salida
  - Ejemplo de respuesta exitosa
  - Ejemplo de error

  ## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 500 o 503 cuando no hay conexión a la base de datos.
- [ ] El campo `mensaje` en el JSON incluye un texto amigable y claro para el usuario técnico o frontend.
