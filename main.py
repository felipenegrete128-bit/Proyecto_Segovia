import os #primero se ubican bibliotecas externas y luego bibliotecas de nuestros archivos
import pandas as pd
from datetime import date, timedelta
from openpyxl.utils import get_column_letter
from colecciones import placas, minas, tarifas_2026 #Así llamamos diccionarios creados y almacenados en otra carpeta
from funciones import *
fecha_hoy = date.today()#Esto nos devuelve una fecha
fecha = fecha_hoy - timedelta(days=1)#En tipo de dato de tiempo, restar 1 día.
fecha = fecha.strftime("%d-%m-%y")#Aplicamos el metodo para formatear el str para fecha
df = pd.read_excel(f'Datos/reporte__mineral_bascula - {fecha}.xlsx')
df_limpio = []
df_a_revisar = []
df_final = []

df.to_dict('records') #Usamos el comando .to_dict() para convertir el df en diccionario iterable

for fila in df.to_dict('records'):
    if type(fila['Placa Vehiculo']) == str and es_placa_nuestra(fila['Placa Vehiculo'], placas):
        df_limpio.append(fila)
    else:
        df_a_revisar.append(fila)

for registro in df_limpio:
    rango = ""
    peso_neto = calcular_peso_neto(registro['Peso Entrada'], registro['Peso Salida'])
    if peso_neto == 0:
        registro['Motivo_Rechazo'] = 'Peso Neto en 0'
        df_a_revisar.append(registro)
        continue

    mina = encontrar_mina(registro['Item'], minas)
    if not mina:
        registro['Motivo_Rechazo'] = 'Mina no encontrada'
        df_a_revisar.append(registro)
        continue
    registro['Item'] = mina['Mina'].strip()
    rango = definir_rango(mina)

    placa = obtener_vehiculo(registro['Placa Vehiculo'], placas)
    if not placa:
        registro['Motivo_Rechazo'] = 'Vehículo no encontrado'
        df_a_revisar.append(registro)
        continue
    registro['Tipo Vehiculo'] = placa['Tipo Vehiculo']
    registro['Propiedad'] = placa['Propiedad']
    registro['Placa Vehiculo'] = placa['Placa Vehiculo']    
    sobre_peso = peso_neto >= placa['Capacidad'] #Hacer función para calcular cantidad de toneladas de sobrepeso (Peso_Neto - Capacidad)
    registro['Sobre_Peso'] = sobre_peso   
    tarifa = obtener_tarifa(rango,placa['Tipo Vehiculo'],'2026', tarifas_2026)
    if not tarifa:
        registro['Motivo_Rechazo'] = 'Tarifa no encontrada'
        df_a_revisar.append(registro)
        continue
    registro['Tarifa'] = tarifa
    registro['Facturacion'] = obtener_facturacion(tarifa, peso_neto)
    registro['Peso Neto'] = peso_neto
    registro['Rango'] = rango
    df_final.append(registro)

nuevas_columnas = ['Numero Consecutivo', 'Item', 'Fecha Registro', 'Placa Vehiculo', 'Nombre Conductor', 'Hora Registro', 'Hora Salida', 'Peso Entrada', 'Peso Salida', 'Peso Neto', 'Tipo Vehiculo', 'Propiedad', 'Tarifa', 'Sobre_Peso', 'Facturacion', 'Rango']
df_final = pd.DataFrame(df_final)
if not df_final.empty:
    df_final = df_final[nuevas_columnas]

for fila in df.to_dict('records'):
    if type(fila['Placa Vehiculo']) == str and es_placa_nuestra(fila['Placa Vehiculo'], placas):
        df_limpio.append(fila)
    else:
        fila['Motivo_Rechazo'] = 'Placa no pertenece a la flota o es inválida'
        df_a_revisar.append(fila)
columnas_revisar = list(df.columns) + ['Motivo_Rechazo']
df_a_revisar = pd.DataFrame(df_a_revisar, columns=columnas_revisar)
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
df_a_revisar.to_excel(f'salida/Revisar reporte_mineral {fecha}.xlsx',index=False)