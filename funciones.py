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
#Pendiente hacer las demá funciones y documentarlas