from readExcel import leerDatos as leer 
from procesadorDatosIntervalos import tablaPorIntervalos as porIntervalos

datos = leer("ej.xlsx")
tablaDeDatos,cuartiles,deciles,percentiles = porIntervalos(datos)#rawr definir variables
cadena = ""
conFila = 0
for fila  in tablaDeDatos :
    conFila += 1
    cadena = ""
    for dato in fila:
        cadena = cadena + str(dato) + " "
    print(f"{conFila}||{cadena}")
cuPor = 0
print()
print("cuartiles")
for cuartil in cuartiles:
    cuPor +=25 
    print(f"{cuPor}% ={cuartil}")
dePor = 0
print()
print("deciles")
for decil in deciles:
    dePor +=10 
    print(f"{dePor}% ={decil}")