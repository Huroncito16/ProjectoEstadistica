from collections import Counter
import math
import numpy as np
from scipy.stats import kurtosis, skew

def listas(datos):
    frecuencias = Counter(datos)
    n = len(datos)

    valores = sorted(frecuencias.keys())

    frecuencia_abs = []
    frecuencia_rel = []
    frecuencia_acum = []
    frecuencia_acum_rel = []
    frecuencia_desc = []
    frecuencia_desc_rel = []
    frecuencia_abs_x = []
    deltas = []
    frecuencia_abs_delta = []
    frecuencia_abs_delta_abs = []
    frecuencia_abs_delta_cuadrado = []
    frecuencia_abs_delta_cubo = []
    frecuencia_abs_delta_cuarta = []

    fa_acum = 0
    fd_acum = n
    media = sum([valor * frecuencias[valor] for valor in valores]) / n

    for valor in valores:
        f = frecuencias[valor]
        d = valor - media
        fa_acum += f
        fr = (f / n) * 100
        fr_acum_rel = (fa_acum / n) * 100
        fd_acum -= f
        fd_rel = (fd_acum / n) * 100
        delta = valor - media
        abs_delta = abs(delta)
        delta_cuadrado = delta ** 2
        delta_cubo = delta ** 3
        delta_cuarta = delta ** 4

        frecuencia_abs.append(f)
        frecuencia_rel.append(fr)
        frecuencia_acum.append(fa_acum)
        frecuencia_acum_rel.append(fr_acum_rel)
        frecuencia_desc.append(fd_acum)
        frecuencia_desc_rel.append(fd_rel)
        frecuencia_abs_x.append(f * valor)
        deltas.append(delta)
        frecuencia_abs_delta.append(f * delta)
        frecuencia_abs_delta_abs.append(f * abs_delta)
        frecuencia_abs_delta_cuadrado.append(f * delta_cuadrado)
        frecuencia_abs_delta_cubo.append(f * delta_cubo)
        frecuencia_abs_delta_cuarta.append(f * delta_cuarta)

    total_f = sum(frecuencia_abs)
    total_f_rel = sum(frecuencia_rel)
    total_abs_delta = sum(frecuencia_abs_delta_abs)
    total_delta = sum(frecuencia_abs_delta)
    total_delta_cuadrado = sum(frecuencia_abs_delta_cuadrado)
    total_delta_cubo = sum(frecuencia_abs_delta_cubo)
    total_delta_cuarta = sum(frecuencia_abs_delta_cuarta)

    # Cálculo de los parámetros adicionales
    valores_np = np.array(datos)
    valor_minimo = np.min(valores_np)
    valor_maximo = np.max(valores_np)
    rango = valor_maximo - valor_minimo
    media = np.mean(valores_np)
    mediana = np.median(valores_np)
    moda = [item for item, count in Counter(datos).items() if count == max(Counter(datos).values())]
    varianza = np.var(valores_np, ddof=0)
    desviacion_estandar = np.std(valores_np, ddof=0)
    curtosis = kurtosis(valores_np, fisher=True)
    asimetria = skew(valores_np, bias=False)

    return {
        'valores': valores,
        'frecuencia_abs': frecuencia_abs,
        'frecuencia_rel': frecuencia_rel,
        'frecuencia_acum': frecuencia_acum,
        'frecuencia_acum_rel': frecuencia_acum_rel,
        'frecuencia_desc': frecuencia_desc,
        'frecuencia_desc_rel': frecuencia_desc_rel,
        'frecuencia_abs_x': frecuencia_abs_x,
        'deltas': deltas,
        'frecuencia_abs_delta': frecuencia_abs_delta,
        'frecuencia_abs_delta_abs': frecuencia_abs_delta_abs,
        'frecuencia_abs_delta_cuadrado': frecuencia_abs_delta_cuadrado,
        'frecuencia_abs_delta_cubo': frecuencia_abs_delta_cubo,
        'frecuencia_abs_delta_cuarta': frecuencia_abs_delta_cuarta,
        'total_f': total_f,
        'total_f_rel': total_f_rel,
        'total_abs_delta': total_abs_delta,
        'total_delta': total_delta,
        'total_delta_cuadrado': total_delta_cuadrado,
        'total_delta_cubo': total_delta_cubo,
        'total_delta_cuarta': total_delta_cuarta,
        'valor_minimo': valor_minimo,
        'valor_maximo': valor_maximo,
        'rango': rango,
        'media': media,
        'mediana': mediana,
        'moda': moda,
        'varianza': varianza,
        'desviacion_estandar': desviacion_estandar,
        'curtosis': curtosis,
        'asimetria': asimetria
    }