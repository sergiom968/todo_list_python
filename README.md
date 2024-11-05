# Seguidor de tareas (Task tracker)

Se trata de un script desarrollado en python, su objetivo es poder realizar seguimiento a diferentes tareas mediante el uso de la terminal del sistema


## Caracteristicas
- Permite listar todas las tareas o según su estado, ej: *pendiente*
- Crea nuevas tareas
- Actualiza la descripción de las tareas ya guardadas
- Permite cambiar el estado de las tareas (pendiente, en_proceso, completado)
- Elimina tareas

### Propiedades de la tarea
- **ID:** identificador único que se genera de forma automática como un dato de tipo **número**
- **Descripcióń:** texto que describe la tarea
- **Estado:** pendiente, en_proceso, completado (por defecto: pendiente)
- **Fecha de creación:** fecha en que se creó la tarea
- **Fecha de actualización:** fecha de la última actualización de la tarea


## Instalación

Requiere [Python](https://www.python.org/downloads/) v 3.12 o superior

## Uso
### Añadir tarea
```sh
añadir "Nueva tarea"
```
**"Nueva tarea"** corresponde a la descripción de la tarea a añadir

### Listar tareas
```sh
listar <estado>
```
**"estado"** corresponde al estado a filtrar (*opcional*), en caso de no proporcionar un estado se mostrarán todas las tareas

### Actualizar tarea
```sh
actualizar <ID> "Nueva descripción"
```
**"ID"** corresponde al ID de la tarea a actualizar y **"Nueva descripción"** corresponde al texto a guardar como descripción

### Cambiar estado (marcar como:)
```sh
marcar-<nuevo_estado> <ID>
```
**"ID"** corresponde al ID de la tarea a actualizar y **"nuevo_estado"** corresponde al nuevo estado de la tarea (pendiente, en_proceso, completado).

### Eliminar tarea
```sh
eliminar <ID> 
```
**"ID"** corresponde al ID de la tarea a eliminar

## Agradecimientos:
  Proyecto realizado como parte del roadmap de Backend de [Roadmap.sh](https://roadmap.sh/projects/task-tracker)
