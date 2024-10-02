import pandas as pd
import numpy as np

def esNumero(num):
    try:
        # Verificar que el dato no es NaN antes de intentar convertirlo a float
        if pd.isna(num):
            return False
        float(num)  # Asegurarse de que es un número
        return True
    except Exception:
        return False

def leerDatos(ubi):
    terFila = False
    terColumna = False
    nFila = -1
    datos = list()
    x = pd.read_excel(ubi)
    maxFilas, maxColumnas = x.shape
    
    while not terFila:
        nFila += 1
        
        # Verificar que nFila está dentro del rango
        if nFila >= maxFilas:
            break
        
        nColumnas = -1
        terColumna = False
        
        while not terColumna:
            nColumnas += 1
            
            # Verificar que nColumnas está dentro del rango
            if nColumnas >= maxColumnas:
                break
            
            dato = x.iloc[nFila, nColumnas]

            if esNumero(dato):
                # Conservar el valor tal cual
                datos.append(float(dato))
            
            # Verificar que nColumnas+1 está dentro del rango antes de acceder
            if nColumnas + 1 >= maxColumnas:
                terColumna = True
            else:
                datoSiguiente = x.iloc[nFila, nColumnas + 1]
                if not esNumero(datoSiguiente):
                    terColumna = True
        
        # Verificar que nFila+1 está dentro del rango antes de acceder
        if nFila + 1 >= maxFilas:
            terFila = True
        else:
            datoSiguiente = x.iloc[nFila + 1, nColumnas]
            if not esNumero(datoSiguiente):
                terFila = True

    datos.sort()
    return datos