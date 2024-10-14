import analiCombi as comb
import math
def distriBinomial(num_exitos, ensayos, prob_exito, acumulado):
    combinat = comb.combSinRep(ensayos, num_exitos)
    pk = prob_exito ** num_exitos
    qN_K = (1 - prob_exito) ** (ensayos - num_exitos)
    resul = pk * combinat * qN_K
    num_exitos = num_exitos - 1
    if acumulado and num_exitos >= 0:
        return resul + distriBinomial(num_exitos, ensayos, prob_exito, acumulado)
    else:
        return resul

def distriPoison(x,media,acumulado):
    uK= media ** x
    expMenU= math.e ** -media
    factK = math.factorial(x)
    resul = uK * expMenU / factK
    x -= 1
    if acumulado and x >= 0:
        return resul + distriPoison(x,media,acumulado)
    else:
        return resul
    
if __name__ == "__main__":
    n = 5
    disB = distriPoison(4,7,True)
    disB = round(disB * 100,2)
  
    print(disB)