""" print(df.info())
print(df.shape) 
print(df.head())
print(df['Placa Vehiculo'].head(10)) """

def es_placa_nuestra(placa:str, placas:list)->bool:
    placa = placa.replace(' ', '')
    for p in placas:
        if p['Placa Vehiculo'] == placa:#Siempre lo que ingrese en nuestra funcion a comparar, debe provenir del df.
            return True 
    return False    

#Funciones a realizar: contadores, calcular peso_neto, obtener rango, calcular facturacion, obtener tarifa, encontrar mina, obtener tipo vehiculo, Hay sobrepeso, Calcular sobrepeso
#Calculo peso_neto
def calcular_peso_neto(peso_entrada: int, peso_salida: int)->float:
    return (peso_entrada - peso_salida)/1000
    
#Encontrar mina
def encontrar_mina(mina:str, minas:list)->dict:#A partir del nombre que viene del df, comparar con la lista de minas que tengo y debe devolver el diccionario que ya tengo
    alias_minas = {
        "PP MINERAL EL SILENCIO": "Mineral El Silencio",
        "PP MINERAL PROVIDENCIA RC": "Mineral Providencia Rc",
    }
    if nombre in alias_minas:
        nombre = alias_minas[nombre]
    for m in minas:
        if m['Mina'] == mina.title():
            return m
    return None 
   
#Obtener rango de acuerdo a la distancia de la mina
rangos_minas = [
    {"min": 0, "max": 3, "nombre": "0-3km"},
    {"min": 3.1, "max": 8, "nombre": "3.1-8km"},
    {"min": 8.1, "max": 20, "nombre": "8.1-20km"}
]
def definir_rango(minas:list)->str:
    distancia = minas['Distancia']# 1. Extrae la distancia del diccionario
    for rango in rangos_minas:# 2. Recorre RANGOS_MINAS    
        if distancia >= rango['min'] and distancia <= rango['max']:# 3. Compara si la distancia está dentro de cada rango (min y max)
            return rango['nombre']# 4. Cuando encuentres coincidencia, retorna el "nombre" del rango
    return None # 5. Si no encuentra nada

#Obtener tipo de vehiculo
def tipo_vehiculo(placa:str, placas:list)->str:
    for p in placas:
        if p['Placa'] == placa:
            return p['Tipo Vehiculo']
    return None

#Obtener tarifa
def obtener_tarifa(definir_rango:str, tipo_vehiculo:str, tarifas:list)->int:#Duda sobre si es posible poner funciones como parámetros
    for t in tarifas:
        if t['Rango'] == definir_rango and t['Tipo Vehiculo'] == tipo_vehiculo:
            return t['Tarifa']
    return None

#Obtener facturacion
def obtener_facturacion(tarifa:int, peso_neto:float)->int:
    return tarifa * peso_neto