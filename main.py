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
        registro['Item'] = mina['Mina'].strip()
        rango = definir_rango(mina)
    else:
        df_a_revisar.append(registro)
    placa = obtener_vehiculo(registro['Placa Vehiculo'], placas)
    if placa:
        registro['Tipo Vehiculo'] = placa['Tipo Vehiculo']
        registro['Propiedad'] = placa['Propiedad']
        registro['Placa Vehiculo'] = placa['Placa Vehiculo']
        tarifa = obtener_tarifa(rango,placa['Tipo Vehiculo'],'2026', tarifas_2026)
        registro['Tarifa'] = tarifa
        sobre_peso = peso_neto >= placa['Capacidad'] #Hacer función para calcular cantidad de toneladas de sobrepeso (Peso_Neto - Capacidad)
        registro['Sobre_Peso'] = sobre_peso
    else:
        df_a_revisar.append(registro)
    if tarifa:
        registro['Facturacion'] = obtener_facturacion(tarifa, peso_neto)
    else:
        df_a_revisar.append(registro)
    registro['Peso Neto'] = peso_neto
    registro['Rango'] = rango

df_limpio = pd.DataFrame(df_limpio)
nuevas_columnas = ['Numero Consecutivo', 'Item', 'Fecha Registro', 'Placa Vehiculo', 'Nombre Conductor', 'Hora Registro', 'Hora Salida', 'Peso Entrada', 'Peso Salida', 'Peso Neto', 'Tipo Vehiculo', 'Propiedad', 'Tarifa', 'Sobre_Peso', 'Facturacion', 'Rango']
df_limpio = df_limpio[nuevas_columnas]

df_a_revisar = pd.DataFrame(df_a_revisar, columns=df.columns)
os.makedirs('salida', exist_ok=True)
formatos = {
    "Fecha Registro": "dd/mm/yyyy",
    "Distancia":      "#,##0.0",
    "Peso Entrada":   "#,##0",
    "Peso Salida":    "#,##0",
    "Peso Neto":      "#,##0.00",
    "Tarifa":         "$#,##0",
    "Facturacion":    "$#,##0",
} #Formateo de excel

with pd.ExcelWriter(f'salida/reporte_mineral {fecha}.xlsx', engine='openpyxl') as writer:
    df_limpio.to_excel(writer,sheet_name='reporte_mineral', index=False)
    hoja = writer.sheets['reporte_mineral']
    for i, columna in enumerate(df_limpio.columns, start=1):
        letra = get_column_letter(i)

        if columna in formatos:
            for celda in hoja[letra][1:]:
                celda.number_format = formatos[columna]