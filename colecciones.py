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
            'placa': fila['Placa'],
            'propiedad': fila['Propiedad'],
            'capacidad': int(fila['Capacidad']),
            'tipo_vehiculo': fila['Tipo Vehiculo'].replace(' ', '_')
        })

#Tarifas M&E
tarifas = {
    "Doble_troque": {
        "0 a 3": 11297,
        "3,1 a 8": 13205,
        "8,1 a 20": 22361
    },
    "Sencilla": {
        "0 a 3": 40946,
        "3,1 a 8": 55188,
        "8,1 a 20": 55188
    }
}