import os
import re
import json
from datetime import date
from datetime import datetime

# Variables globales de consulta
ARCHIVO_JSON = "base_de_datos.json"
ESTADOS = ["pendiente", "completado", "en_proceso"]

# Función que determina si exsiste el fichero .JSON, si no existe lo crea
def detectar_archivo(nombre):
	archivo = os.path.exists(nombre)
	if not archivo:
		_archivo = open(nombre, "x")
		_archivo.write('{"indice": 1, "datos": []}')
		_archivo.close()
		print("Archivo de base de datos creado")
	else:
		print("Archivo de base de datos ya creado")

# Función que lee el archivo JSON y obtiene los datos
def obtener_datos():
	archivo = open(ARCHIVO_JSON, "r")
	contenido = archivo.read()
	archivo.close()
	return json.loads(contenido)

# Función que muestra las tareas, puede filtrar por estado con el parámetro tipo
def listar_tareas(tipo = []):
	if len(tipo) > 0:
		tipo = tipo[0]
	else:
		tipo = ""
	base_de_datos = obtener_datos()["datos"]
	if not tipo == "":
		if tipo.lower() in ESTADOS:
			base_de_datos = [el for el in base_de_datos if el["estado"] == tipo]	
		else:
			print("Tipo de estado no válido")
			return False
	if len(base_de_datos) > 0:
		imprimir_tabla(base_de_datos)
	else:
		print("No hay datos para mostrar")

# Función que añade una nueva tarea
def anadir_tarea(texto):
	textp = validar_texto(texto)
	if not texto: return
	base_de_datos = obtener_datos()
	ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	ID = base_de_datos["indice"]
	base_de_datos["datos"].append({
		"ID": ID,
		"descripcion": textp,
		"estado": "pendiente",
		"fecha_creacion": ahora,
		"fecha_actualizacion": ahora
	})
	base_de_datos["indice"] += 1
	guardar_en_bd(base_de_datos)
	print(f"Tarea añadida exitosamente (ID: {ID}): {textp}")

# Función que actualiza el estado de una tarea según el parámetro ID
def marcar_tarea(tipo, id_tarea):
	base_de_datos = obtener_datos()
	tarea, id_tarea = validar_tarea(base_de_datos, id_tarea)
	if not tarea and not id_tarea: return
	tarea["fecha_actualizacion"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	tipo = tipo.split("-")[1]
	tarea["estado"] = tipo
	guardar_en_bd(base_de_datos)
	print(f"La tarea con ID: {tarea["ID"]} se marcó como '{tipo}'")

# Función que actualiza la descripción de una tarea según el parámetro ID
def actualizar_tarea(id_tarea, texto):
	base_de_datos = obtener_datos()
	tarea, id_tarea = validar_tarea(base_de_datos, id_tarea)
	if not tarea and not id_tarea: return
	texto = validar_texto(texto)
	if not texto: return
	tarea["descripcion"] = texto
	tarea["fecha_actualizacion"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	guardar_en_bd(base_de_datos)
	print(f"La tarea con el ID: {id_tarea} fue actualizada con éxito")

# Función que elimina una tarea según el parámetro ID
def eliminar_tarea(id_tarea):
	base_de_datos = obtener_datos()
	tarea, id_tarea = validar_tarea(base_de_datos, id_tarea)
	if not tarea and not id_tarea: return
	base_de_datos["datos"].remove(tarea)
	guardar_en_bd(base_de_datos)
	print(f"La tarea con el ID: {id_tarea} fue eliminado exitosamente")
	
# Funciones adicionales

#Función que transforma los datos en formato tabla para imprimir
def imprimir_tabla(datos, longitud = 100):
	print("-" * longitud)
	print("".join([clave + " " * (19 - len(clave)) + "|" for clave, valor in datos[0].items()]))
	print("-" * longitud)
	for fila in datos:
		print("".join([str(valor) + " " * (19 - len(str(valor))) + "|" for _, valor in fila.items()]))
		print("-" * longitud)

# Función que recive el parámetro base_de_datos y guarda dicha información en el archivo JSON
def guardar_en_bd(base_de_datos):
	archivo = open(ARCHIVO_JSON, "w")
	archivo.write(json.dumps(base_de_datos, indent = 3))
	archivo.close()

# Función que recive el parámetro texto, valida que el usuario digite una texto diferente de "vacio" y para múltiples palabras valida que se encuentre dentro de '"'
def validar_texto(texto):
	if len(texto) > 1:
		texto = " ".join(texto)
		if texto.count('"') == 2:
			texto = re.findall('"(.*?)"', texto)[0]
		elif '"' in texto:
			print('El texto no cumple el formato, para textos con múltiples palabras debe estar entre comillas ej: "Añada una descripción"')
			return False
		else:
			texto = texto.split(" ")[0]
	elif len(texto) == 1:
		texto = texto[0]
		while texto == "":
			texto = input("Debe especificar el nombre de la tarea: ")
	else:
		texto = ""
		while texto == "":
			texto = input("Debe especificar el nombre de la tarea: ")
	return texto

# Función que retorna una tarea segun el ID
def validar_tarea(base_de_datos, id_tarea):
	id_tarea = verificar_ID(id_tarea)
	if not id_tarea: return False, False
	tarea = [tarea for tarea in base_de_datos["datos"] if tarea["ID"] == int(id_tarea)]
	if len(tarea) == 0:
		print(f"La tarea con el ID: {id_tarea} no fue encontrado, por favor indique un ID valido")
		return False, False
	return tarea[0], id_tarea

# Función que valida la existencia de un ID
def verificar_ID(id_tarea):
	if len(id_tarea) == 0:
		print("Debe ingresar el ID de la tarea a eliminar")
		return
	id_tarea = id_tarea[0]
	if not id_tarea.isnumeric():
		print("Debe ingresar un formato válido de ID (número, ej: 1)")
		return
	return id_tarea

# Se ejecuta al inicio de la aplicación para deteminar si existe o no el archivo de base datos
detectar_archivo(ARCHIVO_JSON)

# Loop que escucha permanentementa la entrada del usuario
while True:
	try:
		_entrada = input("task-cli$: ") # Entrada del usuario
		entrada, *argumentos = _entrada.split(" ") # Obtiene el valor de la entrada y los argumentos
		os.system("clear") # Limpia la consola
		print(f"task-cli$: {_entrada}") # Muestra la entrada del usuario
		entrada = entrada.lower() # Pasa a minúscula la variable entrada
		
		# Condicional que evaluar la entrada del usuario
		if entrada == "salir":
			print("Gracias por usar el administrador de tareas :)")
			break
		elif entrada == "añadir":
			tarea = argumentos
			anadir_tarea(tarea)
		elif entrada == "listar":
			listar_tareas(argumentos)
		elif entrada == "actualizar":
			id_tarea, *texto = argumentos
			actualizar_tarea(id_tarea, texto)
		elif entrada in [f"marcar-{estado}" for estado in ESTADOS]:
			marcar_tarea(entrada, argumentos)
		elif entrada == "eliminar":
			eliminar_tarea(argumentos)
		elif entrada == "ayuda":
			print("Ayuda")
		else:
			print(f"Comando: {entrada} no encontrado, digite 'ayuda' para obtener más información")
	except:
		print("Se ha presentado un error, intente nuevamente")