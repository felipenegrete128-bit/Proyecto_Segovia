#Creacion de diccionarios de minas mineral
import csv

minas = []

with open('Datos/Minas_Mineral.csv', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo, delimiter=';')
    for fila in lector:
        minas.append({
            'mina': fila['Mina'],
            'tipo_material': fila['Tipo Material'],
            'grupo': fila['Grupo'],
            'distancia': float(fila['Distancia '].replace(',', '.')),
            'pertenencia': fila['Pertenencia']
        })

#Creacion de diccionarios de placas
placas = []

with open('Datos/Placas.csv', encoding='latin-1') as archivo:
    lector = csv.DictReader(archivo, delimiter=';')
    for fila in lector:
        placas.append({
            'Placa Vehiculo': fila['Placa'],
            'propiedad': fila['Propiedad'],
            'capacidad': int(fila['Capacidad']),
            'tipo_vehiculo': fila['Tipo Vehiculo'].replace(' ', '_')
        }) 

#Tarifas M&E
tarifas_2026 = []

with open('Datos/Tarifas_M&E.csv') as archivo:
    lector = csv.DictReader(archivo, delimiter=';')
    for fila in lector:
        tarifas_2026.append({
            'rango': fila['Rango'],
            'tipo_vehiculo': fila['Tipo Vehiculo'],
            'tarifa': int(fila['Tarifa']),
            'ano': fila['Ano']
        })
