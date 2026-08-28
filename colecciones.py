#Creacion de diccionarios de minas mineral
import csv

minas = []

with open('Datos/Minas_Mineral.csv', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo, delimiter=';')
    for fila in lector:
        minas.append({
            'Mina': fila['Mina'],
            'Tipo Material': fila['Tipo Material'],
            'Grupo': fila['Grupo'],
            'Distancia': float(fila['Distancia '].replace(',', '.')),
            'Pertenencia': fila['Pertenencia']
        })

#Creacion de diccionarios de placas
placas = []

with open('Datos/Placas.csv', encoding='latin-1') as archivo:
    lector = csv.DictReader(archivo, delimiter=';')
    for fila in lector:
        placas.append({
            'Placa Vehiculo': fila['Placa'],
            'Propiedad': fila['Propiedad'],
            'Capacidad': int(fila['Capacidad']),
            'Tipo Vehiculo': fila['Tipo Vehiculo'].replace(' ', '_')
        }) 

#Tarifas M&E
tarifas_2026 = []

with open('Datos/Tarifas_M&E.csv') as archivo:
    lector = csv.DictReader(archivo, delimiter=';')
    for fila in lector:
        tarifas_2026.append({
            'Rango': fila['Rango'],
            'Tipo Vehiculo': fila['Tipo Vehiculo'],
            'Tarifa': int(fila['Tarifa']),
            'Ano': fila['Ano']
        })
