import pandas as pd
df = pd.read_excel('Datos/reporte__mineral_bascula - 23-08-26.xlsx')
print(df.info(), df.shape, df.head())
