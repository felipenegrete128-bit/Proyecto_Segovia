from colecciones import placas, minas, tarifas_2026 #Así llamamos diccionarios creados y almacenados en otra carpeta
from funciones import *
df_limpio = []
df_a_revisar = []
df.to_dict('records') #Usamos el comando .to_dict() para convertir el df en diccionario iterable

for fila in df.to_dict('records'):
    if es_placa_nuestra(fila['Placa Vehiculo'], placas):
        df_limpio.append(fila)
    else:
        df_a_revisar.append(fila)

print(len(df_limpio))
print(len(df_a_revisar))