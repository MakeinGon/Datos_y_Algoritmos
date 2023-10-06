import pandas as pd
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, ttk
import time
import sys



def bubble_sort(arr):
    start_time = time.time()
    n = len(arr)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    end_time = time.time()
    memory = sys.getsizeof(arr)
    return end_time - start_time, memory

def selection_sort(arr):
    start_time = time.time()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    end_time = time.time()
    memory = sys.getsizeof(arr)
    return end_time - start_time, memory

def linear_search(dataframe, x):
    start_time = time.time()
    matches = dataframe[dataframe['UBIGEO'] == x]  # Cambiar UUID por UBIGEO
    end_time = time.time()
    memory = sys.getsizeof(dataframe)
    
    if not matches.empty:
        return matches.index[0], end_time - start_time, memory
    return -1, end_time - start_time, memory

def binary_search(dataframe, x):
    start_time = time.time()
    l = 0
    h = len(dataframe) - 1
    dataframe_sorted = dataframe.sort_values('UBIGEO').reset_index(drop=True)  # Cambiar UUID por UBIGEO
    while l <= h:
        mid = (l + h) // 2
        if dataframe_sorted.at[mid, 'UBIGEO'] == x:  # Cambiar UUID por UBIGEO
            end_time = time.time()
            memory = sys.getsizeof(dataframe)
            return mid, end_time - start_time, memory
        elif dataframe_sorted.at[mid, 'UBIGEO'] < x:  # Cambiar UUID por UBIGEO
            l = mid + 1
        else:
            h = mid - 1
    end_time = time.time()
    memory = sys.getsizeof(dataframe)
    return -1, end_time - start_time, memory



# Leer los datos
ruta_archivo = "C:\\Users\\delso\\Documents\\fallecidos_covid.csv"
data = pd.read_csv(ruta_archivo, delimiter=';', low_memory=False)
print(data.dtypes)

print(data.head())

data = data[data['UUID'].notna()]


# Convertimos la columna de fecha a tipo datetime
data['FECHA_FALLECIMIENTO'] = pd.to_datetime(data['FECHA_FALLECIMIENTO'], format='%Y%m%d')

# Agrupar por DEPARTAMENTO
agrupados = data.groupby('DEPARTAMENTO').size().reset_index(name='fallecidos')

# Mapeo de DEPARTAMENTO a coordenadas. Estas son coordenadas aproximadas centrales para cada departamento.
departamento_coords = {
    'AMAZONAS': [-5.2295, -78.3437],
    'ANCASH': [-9.1900, -77.8608],
    'APURIMAC': [-14.0500, -73.0877],
    'AREQUIPA': [-16.3989, -71.5350],
    'AYACUCHO': [-13.1588, -74.2239],
    'CAJAMARCA': [-7.1697, -78.5128],
    'CALLAO': [-12.0219, -77.1143],
    'CUSCO': [-13.5179, -71.9785],
    'HUANCAVELICA': [-12.7866, -74.9763],
    'HUANUCO': [-9.9306, -76.2422],
    'ICA': [-14.0751, -75.7342],
    'JUNIN': [-11.9526, -75.2829],
    'LA LIBERTAD': [-8.3792, -78.8051],
    'LAMBAYEQUE': [-6.7011, -79.9066],
    'LIMA': [-12.0464, -77.0428],
    'LORETO': [-4.9036, -73.6679],
    'MADRE DE DIOS': [-12.5923, -69.1876],
    'MOQUEGUA': [-17.1956, -70.9350],
    'PASCO': [-10.6681, -76.2542],
    'PIURA': [-5.1945, -80.6328],
    'PUNO': [-15.8349, -70.0269],
    'SAN MARTIN': [-6.9198, -76.8865],
    'TACNA': [-18.0120, -70.2559],
    'TUMBES': [-3.5669, -80.4515],
    'UCAYALI': [-8.3791, -74.5741]
}

def mapa_calor(agrupados):
    agrupados['latitud'] = agrupados['DEPARTAMENTO'].apply(lambda x: departamento_coords.get(x, [None, None])[0])
    agrupados['longitud'] = agrupados['DEPARTAMENTO'].apply(lambda x: departamento_coords.get(x, [None, None])[1])

    # Filtrar los datos que no tienen coordenadas
    agrupados = agrupados.dropna(subset=['latitud', 'longitud'])

    # Crear el mapa de calor
    m = folium.Map(location=[-9.1900, -77.8608], zoom_start=6)
    heat_data = [[row['latitud'], row['longitud'], row['fallecidos']] for index, row in agrupados.iterrows()]
    HeatMap(heat_data).add_to(m)

    m.save("mapa_calor.html")
    print("El mapa de calor ha sido generado en 'mapa_calor.html'")

def histograma_edades():
    """
    Esta función muestra un histograma de fallecimientos por edad.
    """
    plt.figure(figsize=(10, 6))
    data['EDAD_DECLARADA'].dropna().astype(int).hist(bins=50, edgecolor='black', color='skyblue')
    plt.title('Histograma de Fallecimientos por Edad')
    plt.xlabel('EDAD')
    plt.ylabel('Número de Fallecidos')
    plt.grid(True, axis='y')
    plt.show()

def grafico_barras_clasificacion():
    """
    Esta función muestra un gráfico de barras de fallecimientos por clasificación de fallecimientos.
    """
    clasificaciones = data['CLASIFICACION_DEF'].value_counts()
    
    plt.figure(figsize=(12, 7))
    clasificaciones.plot(kind='bar', color='salmon', edgecolor='black')
    plt.title('Fallecimientos por Clasificación de Fallecimientos')
    plt.xlabel('Clasificación')
    plt.ylabel('Número de Fallecidos')
    plt.grid(True, axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def serie_temporal_fallecimientos():
    """
    Esta función muestra una serie temporal de fallecimientos por COVID-19 a lo largo del tiempo.
    """
    serie_temporal = data.groupby('FECHA_FALLECIMIENTO').size()
    plt.figure(figsize=(14, 7))
    serie_temporal.plot(color='purple', linestyle='-', marker='o', markersize=4)
    plt.title('Fallecimientos por COVID-19 a lo largo del tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Fallecidos')
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()

def generar_mapa_calor():
    mapa_calor(agrupados)
    messagebox.showinfo("Información", "El mapa de calor ha sido generado en 'mapa_calor.html'")


def menu_grafico_mejorado():
    root = tk.Tk()
    root.title("Menú de Opciones")
    root.geometry("400x300")

    main_frame = ttk.Frame(root)
    main_frame.pack(pady=20, padx=20)

    def generar_mapa_calor():
        mapa_calor(agrupados)
        messagebox.showinfo("Información", "El mapa de calor ha sido generado en 'mapa_calor.html'")

    def test_bubble_sort():
        sample_data = list(range(1000, 0, -1))
        time_taken, memory_used = bubble_sort(sample_data)
        messagebox.showinfo("Bubble Sort", f"Tiempo tomado: {time_taken:.6f} segundos\nMemoria utilizada: {memory_used} bytes")

    def test_selection_sort():
        sample_data = list(range(1000, 0, -1))
        time_taken, memory_used = selection_sort(sample_data)
        messagebox.showinfo("Selection Sort", f"Tiempo tomado: {time_taken:.6f} segundos\nMemoria utilizada: {memory_used} bytes")

    def test_linear_search():
        def buscar():
            UBIGEO_a_buscar = entrada.get()
            _, tiempo_tomado, memoria_usada = linear_search(data, UBIGEO_a_buscar)  # Cambiar UUID por UBIGEO
            if _ != -1:
                mensaje = f"El UBIGEO {UBIGEO_a_buscar} fue encontrado.\nTiempo tomado: {tiempo_tomado:.6f} segundos\nMemoria utilizada: {memoria_usada} bytes"
            else:
                mensaje = f"El UBIGEO {UBIGEO_a_buscar} no fue encontrado.\nTiempo tomado: {tiempo_tomado:.6f} segundos\nMemoria utilizada: {memoria_usada} bytes"
            messagebox.showinfo("Búsqueda Lineal", mensaje)

        ventana_busqueda = tk.Toplevel(root)
        ventana_busqueda.title("Búsqueda Lineal - Introduce el UBIGEO")
        entrada = ttk.Entry(ventana_busqueda, width=40)
        entrada.pack(pady=20, padx=20)
        ttk.Button(ventana_busqueda, text="Buscar", command=buscar).pack(pady=10)
        entrada.bind('<Return>', lambda event=None: buscar())  # Aquí vinculamos la tecla Enter al botón de buscar.
        ventana_busqueda.mainloop()

    def interfaz_busqueda_binaria():
        def buscar():
            UBIGEO_a_buscar = entrada.get()
            indice, tiempo_tomado, memoria_usada = binary_search(data, UBIGEO_a_buscar)  # Cambiar UUID por UBIGEO
            if indice != -1:
                mensaje = f"El UBIGEO {UBIGEO_a_buscar} fue encontrado en la posición {indice}.\nTiempo tomado: {tiempo_tomado:.6f} segundos\nMemoria utilizada: {memoria_usada} bytes"
            else:
                mensaje = f"El UBIGEO {UBIGEO_a_buscar} no fue encontrado.\nTiempo tomado: {tiempo_tomado:.6f} segundos\nMemoria utilizada: {memoria_usada} bytes"
            messagebox.showinfo("Búsqueda Binaria", mensaje)

        ventana_busqueda = tk.Toplevel(root)
        ventana_busqueda.title("Búsqueda Binaria - Introduce el UBIGEO")
        entrada = ttk.Entry(ventana_busqueda, width=40)
        entrada.pack(pady=20, padx=20)
        ttk.Button(ventana_busqueda, text="Buscar", command=buscar).pack(pady=10)
        entrada.bind('<Return>', lambda event=None: buscar())  # Aquí vinculamos la tecla Enter al botón de buscar.
        ventana_busqueda.mainloop()

   
    ttk.Button(main_frame, text="Generar Mapa de Calor", command=generar_mapa_calor).pack(fill="x", pady=5)
    ttk.Button(main_frame, text="Ver Histograma de Fallecimientos por Edad", command=histograma_edades).pack(fill="x", pady=5)
    ttk.Button(main_frame, text="Ver Gráfico de Barras por Clasificación de Fallecimientos", command=grafico_barras_clasificacion).pack(fill="x", pady=5)
    ttk.Button(main_frame, text="Ver Serie Temporal de Fallecimientos a lo largo del tiempo", command=serie_temporal_fallecimientos).pack(fill="x", pady=5)
    ttk.Button(main_frame, text="Test Bubble Sort", command=test_bubble_sort).pack(fill="x", pady=5)
    ttk.Button(main_frame, text="Test Selection Sort", command=test_selection_sort).pack(fill="x", pady=5)
    ttk.Button(main_frame, text="Test Linear Search", command=test_linear_search).pack(fill="x", pady=5)
    ttk.Button(main_frame, text="Test Binary Search", command=interfaz_busqueda_binaria).pack(fill="x", pady=5)
    ttk.Button(main_frame, text="Salir", command=root.quit).pack(fill="x", pady=5)
    root.mainloop()

menu_grafico_mejorado()