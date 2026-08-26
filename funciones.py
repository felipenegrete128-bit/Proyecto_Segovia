import pandas as pd
df = pd.read_excel('Datos/reporte__mineral_bascula - 23-08-26.xlsx')
""" print(df.info())
print(df.shape) 
print(df.head())
print(df['Placa Vehiculo'].head(10)) """

def es_placa_nuestra(placa:str, placas:list)->bool:
    for p in placas:
        placa_lista = ''.join(p['Placa Vehiculo'].split())
        if placa_lista == placa:#Siempre lo que ingrese en nuestra funcion a comparar, debe provenir del df.
            return True 
    return False    


""" for letra in placa_lista:
            if letra == ' ' """
#Metodos .split() y .join() aplicado a placa_lista