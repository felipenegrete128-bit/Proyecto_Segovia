import os #primero se ubican bibliotecas externas y luego bibliotecas de nuestros archivos
import pandas as pd
from datetime import date
from openpyxl.utils import get_column_letter
from colecciones import placas, minas, tarifas_2026 #Así llamamos diccionarios creados y almacenados en otra carpeta
from funciones import *
fecha = date.today().strftime("%d-%m-%y")#Esto nos devuelve una fecha
df = pd.read_excel('Datos/reporte__mineral_bascula - 23-08-26.xlsx')
df_limpio = []
df_a_revisar = []
df.to_dict('records') #Usamos el comando .to_dict() para convertir el df en diccionario iterable

for fila in df.to_dict('records'):
    if type(fila['Placa Vehiculo']) == str and es_placa_nuestra(fila['Placa Vehiculo'], placas):
        df_limpio.append(fila)
    else:
        df_a_revisar.append(fila)

for registro in df_limpio:
    rango = ""
    mina = encontrar_mina(registro['Item'], minas)
    peso_neto = calcular_peso_neto(registro['Peso Entrada'], registro['Peso Salida'])
    if mina:
        rango = definir_rango(mina)
    else:
        df_a_revisar.append(registro)
    placa = obtener_vehiculo(registro['Placa Vehiculo'], placas)
    if placa:
        registro['Tipo Vehiculo'] = placa['Tipo Vehiculo']
        registro['Propiedad'] = placa['Propiedad']
        registro['Placa Vehiculo'] = placa['Placa']
        tarifa = obtener_tarifa(rango,placa['Tipo Vehiculo'],2026, tarifas_2026)
        registro['Tarifa'] = tarifa
        sobre_peso = peso_neto >= placa['Capacidad'] #Hacer función para calcular cantidad de toneladas de sobrepeso (Peso_Neto - Capacidad)
        registro['Sobre_Peso'] = sobre_peso
    else:
        df_a_revisar.append(registro)
    if tarifa:
        registro['Facturacion'] = obtener_facturacion(tarifa, peso_neto)
    else:
        df_a_revisar.append(registro)
    registro['Item'] = mina['Mina']
    registro['Peso Neto'] = peso_neto
    registro['Rango'] = rango

print(df_limpio[1])