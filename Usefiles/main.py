import pandas as pd
import numpy as np
from faker import Faker
import random

# --- CONFIGURACIÓN INICIAL ---
NUM_REGISTROS = 2500
fake = Faker('es_CO')  # Usar localización Colombia
# Listas de datos controlados para introducir errores
productos = {
    'PROD-001': ('Laptop Pro', 'Tecnología'),
    'PROD-002': ('Mouse Inalámbrico', 'Accesorios'),
    'PROD-003': ('Teclado Mecánico', 'Accesorios'),
    'PROD-004': ('Monitor 4K', 'Tecnología'),
    'PROD-005': ('Silla de Oficina', 'Mobiliario'),
    'PROD-006': ('Libreta Inteligente', 'Oficina'),
}
ciudades = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena']

# --- GENERACIÓN DE DATOS BASE (LIMPIOS) ---
print("Generando datos base...")
data = []
for i in range(NUM_REGISTROS):
    id_producto = random.choice(list(productos.keys()))
    nombre_prod, categoria = productos[id_producto]
    cantidad = random.randint(1, 10)
    precio = round(random.uniform(20.0, 1500.0), 2)

    data.append({
        'ID_Pedido': 1000 + i,
        'ID_Cliente': fake.random_number(digits=5, fix_len=True),
        'Nombre_Cliente': fake.name(),
        'Email_Cliente': fake.email(),
        'ID_Producto': id_producto,
        'Nombre_Producto': nombre_prod,
        'Categoria': categoria,
        'Cantidad': cantidad,
        'Precio_Unitario': precio,
        'Fecha_Pedido': fake.date_between(start_date='-2y', end_date='today'),
        'Ciudad_Envio': random.choice(ciudades),
        'Pais_Envio': 'Colombia'
    })

df = pd.DataFrame(data)

print("Introduciendo errores en el dataset...")

# Problema Duplicados
num_duplicados = int(NUM_REGISTROS * 0.02)
filas_duplicadas = df.sample(n=num_duplicados)
df = pd.concat([df, filas_duplicadas], ignore_index=True)

# Problema Diferencias Ortográficas
for index in df.sample(frac=0.10).index:
    # Alternar entre errores de ciudad y categoría
    if random.random() > 0.5:
        ciudad_original = df.loc[index, 'Ciudad_Envio']
        opciones = [ciudad_original.lower(), ciudad_original.upper(),
                    ciudad_original.replace('á', 'a').replace('é', 'e')]
        df.loc[index, 'Ciudad_Envio'] = random.choice(opciones)
    else:
        categoria_original = df.loc[index, 'Categoria']
        df.loc[index, 'Categoria'] = categoria_original.lower()

# Problema Diferencias de Formato (Fechas y Precios)
for index in df.sample(frac=0.15).index:
    if random.random() > 0.5:  # Formato de fecha
        fecha_original = pd.to_datetime(df.loc[index, 'Fecha_Pedido'])
        formato = random.choice(['%d/%m/%Y', '%m-%d-%y'])
        df.loc[index, 'Fecha_Pedido'] = fecha_original.strftime(formato)
    else:  # Formato de precio (coma decimal)
        df.loc[index, 'Precio_Unitario'] = str(df.loc[index, 'Precio_Unitario']).replace('.', ',')

# Problema Números almacenados como texto
for index in df.sample(frac=0.10).index:
    if random.random() > 0.5:  # Cantidad con espacios
        df.loc[index, 'Cantidad'] = f" {df.loc[index, 'Cantidad']} "
    else:  # Precio con símbolo de moneda
        df.loc[index, 'Precio_Unitario'] = f"$ {df.loc[index, 'Precio_Unitario']}"

# Problema Espacios en las celdas 
for index in df.sample(frac=0.15).index:
    columna_a_modificar = random.choice(['Nombre_Cliente', 'Nombre_Producto'])
    valor_original = df.loc[index, columna_a_modificar]
    df.loc[index, columna_a_modificar] = f"  {valor_original} "

# Problema ===> Diferencias de codificación 
for index in df.sample(frac=0.05).index:
    nombre_original = df.loc[index, 'Nombre_Cliente']
    try:
        # Simula un texto UTF-8 mal interpretado como Latin-1
        df.loc[index, 'Nombre_Cliente'] = nombre_original.encode('utf-8').decode('latin-1')
    except:
        pass  

# Problema ==> Inconsistencias en claves (ID_Cliente) (10% de los datos)
for index in df.sample(frac=0.10).index:
    opcion = random.random()
    if opcion < 0.4:  # Prefijo
        df.loc[index, 'ID_Cliente'] = f"CUST-{df.loc[index, 'ID_Cliente']}"
    elif opcion < 0.7:  # Espacios
        df.loc[index, 'ID_Cliente'] = f" {df.loc[index, 'ID_Cliente']} "
    else:  # Nulo
        df.loc[index, 'ID_Cliente'] = np.nan

# Mezclar el dataframe para que los errores queden distribuidos aleatoriamente
df = df.sample(frac=1).reset_index(drop=True)

# Exportar a CSV
df.to_csv('pedidos_con_errores.csv', index=False, encoding='utf-8')

print("\n¡Archivo 'pedidos_con_errores.csv' generado con éxito!")
print(f"Total de registros: {len(df)}")
print("\nVista previa de los datos generados:")
print(df.head(10))