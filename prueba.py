
"""
from hospital import Hospital
import pandas as pd
def leer_csv():
        try:
        # Leer el archivo CSV especificando la codificación
            lista_hospitales = pd.read_csv("Hospitales.csv", encoding='utf-8',delimiter=';')  # Cambia 'utf-8' por la codificación correcta si es necesario

            # Iterar sobre las filas del DataFrame y crear instancias de Persona
            for index, row in lista_hospitales.iterrows():
                nombre = row['Nombre']
                direccion = row['Direccion']
                distrito = row['Distrito']
                oxi_disp = row['Oxigeno Disponible']
                cost_oxi = row['Costo Oxigeno']
                lat = row['Latitud']
                lon = row['longitud']
                hospital = Hospital(nombre,direccion,distrito,oxi_disp,cost_oxi,lat,lon)
                hospital.insertar_hospital()

        except Exception as e:
            print(f"Error al leer el archivo CSV: {e}")

leer_csv()"""


"""from internado import Internado
import pandas as pd
def leer_csv():
        try:
        # Leer el archivo CSV especificando la codificación
            lista_hospitales = pd.read_csv("internados.csv", encoding='utf-8',delimiter=';')  # Cambia 'utf-8' por la codificación correcta si es necesario

            # Iterar sobre las filas del DataFrame y crear instancias de Persona
            for index, row in lista_hospitales.iterrows():
                dni = str(row['dni'])
                id_hospital = int(row['id_hospital'])
                cant_oxi = int(row['oxigeno_requerido'])
                internado = Internado(dni,id_hospital,cant_oxi)
                internado.insertar_internado()

        except Exception as e:
            print(f"Error al leer el archivo CSV: {e}")

leer_csv()"""


import math

def distancia(hospital1, hospital2):
    
    #Calcula la distancia entre dos puntos en la Tierra especificados en grados de latitud y longitud.
    #La distancia se devuelve en kilómetros.
    
    # Convertir grados a radianes
    lat1 = math.radians(hospital1.lat)
    lon1 = math.radians(hospital1.lon)
    lat2 = math.radians(hospital2.lat)
    lon2 = math.radians(hospital2.lon)
    
    # Diferencias de coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Fórmula del haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Radio de la Tierra en kilómetros (puedes usar 3956 para millas)
    R = 6371.0
    
    # Distancia en kilómetros
    distance = R * c
    
    return distance



