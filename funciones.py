""" print(df.info())
print(df.shape) 
print(df.head())
print(df['Placa Vehiculo'].head(10)) """

def es_placa_nuestra(placa:str, placas:list)->bool:
    "Valida la existencia de cada placa en el registro de báscula respecto a nuestra lista de placas."
    "Parámetros: placa(proviene del registro de báscula) y placas(nuestra lista de placas, donde cada placa es un diccionario)."
    "Retorno: True o False."
    placa = placa.replace(' ', '')
    for p in placas:
        if p['Placa Vehiculo'] == placa:#Siempre lo que ingrese en nuestra funcion a comparar, debe provenir del df.
            return True 
    return False    

#Calculo peso_neto
def calcular_peso_neto(peso_entrada: int, peso_salida: int)->float:
    "Calcula el peso neto de un viaje en toneladas."
    "Parámetros: peso_entrada y peso_salida, en kilos."
    "Retorno: el peso neto en toneladas (float)."
    return (peso_entrada - peso_salida)/1000
    

#Encontrar mina
def encontrar_mina(mina:str, minas:list)->dict:#A partir del nombre que viene del df, comparar con la lista de minas que tengo y debe devolver el diccionario que ya tengo
    "Valida la existencia de cada mina en el registro de báscula respecto a nuestra lista de minas"
    "Parámetros: mina (proviene del registro de báscula) y minas(nuestra lista de minas, donde cada mina es un diccionario)"
    "Retorno: Diccionario de cada mina."
    alias_minas = {
        "PM-44-1 UPM EL MANZANILLO FINO MEDIO TENOR": "El Manzanillo",
        "ASM-2026-005-TP-GOLDEN BEAK-2.3<=Au<8.0 g/t":"Golden Beak",
        "ASM-2026-0015-TP-MINERALCO TERMINAL-8.0≤Au<15.0 g/tn":"Mineralco",
        "PM-117-1 OUTSOURCING EXPLOTACIONES GOLD CARLA":"Explotaciones Gold Carla",
        "ASM-2026-018 TP LA PALMICHALA 8.0≤Au<15.0 g/t":"La Palmichala",
        "PM-00-1 OUTSOURCING SK 3-7":"Sk 3-7"
    }
    if mina in alias_minas:
        mina = alias_minas[mina]
    elif mina[:2] == 'PP':
        mina = mina[3:]
    for m in minas:
        if m['Mina'].strip() == mina.title():#strip elimina espacios vacios adelante y detrás
            return m
    return None    

#Obtener rango de acuerdo a la distancia de la mina
def definir_rango(mina:dict)->str:
    "Devuelve el rango correspondiente a cada mina."
    "Parámetro: mina (Diccionario de la mina de cada registro)"
    "Retorno: Se extrae el rango de la mina de cada registro"
    rangos_minas = [
    {"min": 0, "max": 3, "nombre": "0 a 3"},
    {"min": 3.1, "max": 8, "nombre": "3,1 a 8"},
    {"min": 8.1, "max": 20, "nombre": "8,1 a 20"}
]
    distancia = mina['Distancia']# 1. Extrae la distancia del diccionario
    for rango in rangos_minas:# 2. Recorre RANGOS_MINAS    
        if rango['min'] <= distancia <= rango['max']:# 3. Compara si la distancia está dentro de cada rango (min y max)
            return rango['nombre']# 4. Cuando encuentres coincidencia, retorna el "nombre" del rango
    return None # 5. Si no encuentra nada

#Obtener tipo de vehiculo
def obtener_vehiculo(placa:str, placas:list)->dict:
    "Devuelve la placa"
    "Parámetros: placa(proviene del registro de báscula ya limpio) y placas(nuestra lista de placas, donde cada placa es un diccionario)"
    "Retorno: Se extrae la placa de cada diccionario propio"
    placa = placa.replace(' ', '')
    for p in placas:
        if p['Placa Vehiculo'] == placa:
            return p
    return None

#Obtener tarifa
def obtener_tarifa(rango:str, tipo_vehiculo:str, ano:str, tarifas:list)->int:
    "Devuelve la tarifa luego de validar el rango y el tipo de vehiculo"
    "Parámetros: rango(rango de cada mina del registro), tipo_vehiculo(tipo de vehiculo de cada placa), ano(año al que aplica la tarifa consultada) y tarifas(Lista de tarifas, cada tarifa es un diccionario)"
    "Retorno: Se extrae la tarifa correspondinete"
    for t in tarifas:
        if t['Ano'] == ano:
            if t['Rango'] == rango and t['Tipo Vehiculo'] == tipo_vehiculo:
                return t['Tarifa']
    return 0

#Obtener facturacion
def obtener_facturacion(tarifa:int, peso_neto:float)->float:
    "Calcula el valor a facturar de cada total de tonelada transportada"
    "Parámetros: tarifa(Tarifa correspodiente al registro) y peso_neto(Total de toneladas transportadas en cada registro)"
    "Retorno: La multiplicación entre tarifa y peso_neto"
    return tarifa * peso_neto

#Obtener rango en esteril
def definir_rango(mina:str,destino:str, minas:list)->str:
    "Devuelve el rango correspondiente a cada combinación mina - destino."
    "Parámetro: mina (Diccionario de la mina de cada registro)"
    "Retorno: Se extrae el rango de la combinación mina - destino de cada registro"
    rango_minas = [
    {"min": 0, "max": 3, "nombre": "0 a 3"},
    {"min": 3.1, "max": 8, "nombre": "3,1 a 8"},
    {"min": 8.1, "max": 20, "nombre": "8,1 a 20"}
]
    for m in minas:#Recorre cada registro de minas
        if m['Mina'] == mina and m['Destino'] == destino:#Comprobar si la mina y destino coinciden con el diccionario de minas de estéril
            distancia = m['Distancia']#Cuando se cumpla la coincidencia se toma la distancia
            for rango in rango_minas:# 2. Recorre RANGOS_MINAS    
                if rango['min'] <= distancia <= rango['max']:# 3. Compara si la distancia está dentro de cada rango (min y max)
                    return rango['nombre']# 4. Cuando encuentres coincidencia, retorna el "nombre" del rango
    return None # 5. Si no encuentra nada

#Validar destino cuando sea donación
def obtener_destino(destino:str, sello:str, reporte:list)->str:
    "Valida el destino del registro de báscula respecto al reporte de esteril promediado"
    for r in reporte:
        if r['Sello'] == sello and destino == 'Donacion':
            destino = destino.replace('Donacio', r['Destino'])
    return None