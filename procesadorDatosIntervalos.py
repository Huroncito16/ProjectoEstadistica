from collections import Counter
import math

def condicion(x, li, ls):
    return li <= x <= ls

def generar_tabla_por_intervalos(dato):
    cEnDatos = Counter(dato)

    min_val = min(dato)
    max_val = max(dato)
    n = len(dato)
    rango = max_val - min_val
    
    ni = 1 + 3.322 * math.log(n, 10)
    ni = round(ni, 2)
    i = round(rango / ni, 0)  # Tamaño del intervalo

    li, ls, xi, frecuencia, fr, fa, faPor, fd, fdPor, fPorXi, d = ([] for _ in range(11))
    faDato = 0
    fdVar = n

    x = min_val
    while x < max_val:
        li.append(x)
        ls.append(x + i - 1)
        x += i 

    canIntervalos = len(li)

    for indice in range(canIntervalos):
        promedio = (li[indice] + ls[indice]) / 2 
        xi.append(promedio)
        fre = [x for x in dato if condicion(x, li[indice], ls[indice])]
        freVar = len(fre)
        frecuencia.append(freVar)
        xFR = round((freVar * 100) / n, 2)
        fr.append(xFR)
        faDato += freVar
        fa.append(faDato)
        faPor.append(round((faDato * 100) / n, 2))
        fd.append(fdVar)
        fdPor.append(round((fdVar * 100) / n, 2))
        fdVar -= freVar
        fPorXi.append(round((freVar * promedio), 2))

    mediaArit = round(sum(fPorXi) / n, 2)
    
    fPorAbsD, fPorDD, fPorDDD, fPorDDDD = ([] for _ in range(4))
    maxFre, indMaxFre, posicionMediana, mediana = 0, 0, n / 2, 0
    serchMediana = True

    for indice in range(canIntervalos):
        dVar = round(xi[indice] - mediaArit, 2)
        d.append(dVar)
        fPorAbsD.append(round(frecuencia[indice] * abs(dVar), 2))
        fPorDD.append(round(frecuencia[indice] * dVar**2, 2))
        fPorDDD.append(round(frecuencia[indice] * dVar**3, 2))
        fPorDDDD.append(round(frecuencia[indice] * dVar**4, 2))

        # Moda
        if frecuencia[indice] > maxFre:
            indMaxFre = indice
            maxFre = frecuencia[indice]

        # Mediana
        if posicionMediana <= fa[indice] and serchMediana:
            mediana = li[indice] + ((posicionMediana - fa[indice-1]) / frecuencia[indice]) * i
            mediana = round(mediana, 2)
            serchMediana = False

    delta1Moda = frecuencia[indMaxFre] - frecuencia[indMaxFre-1]
    delta2Moda = frecuencia[indMaxFre] - frecuencia[indMaxFre+1]
    moda = round(li[indMaxFre] + (delta1Moda / (delta1Moda + delta2Moda) * i), 2)

    desviacionMed = round(sum(fPorAbsD) / n, 2)
    desviacionEst = round(math.sqrt(sum(fPorDD) / n), 2)
    sk = round(sum(fPorDDD) / (n * (desviacionEst ** 3)), 2)
    k = round(sum(fPorDDDD) / (n * (desviacionEst ** 4)), 2)

    return {
        'valor': xi,
        'li': li, 
        'ls': ls, 
        'xi': xi, 
        'frecuencia': frecuencia, 
        'fr': fr, 
        'fa': fa, 
        'faPor': faPor, 
        'fd': fd, 
        'fdPor': fdPor, 
        'fPorXi': fPorXi, 
        'd': d, 
        'fPorAbsD': fPorAbsD, 
        'fPorDD': fPorDD, 
        'fPorDDD': fPorDDD, 
        'fPorDDDD': fPorDDDD,

        'moda': moda, 
        'mediana': mediana, 
        'mediaArit': mediaArit, 
        'desviacionMed': desviacionMed, 
        'desviacionEst': desviacionEst, 
        'sk': sk, 
        'k': k
    }