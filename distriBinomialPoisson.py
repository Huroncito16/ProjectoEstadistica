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

def distriPoison(x, media, acumulado):
    uK = media ** x
    expMenU = math.e ** -media
    factK = math.factorial(x)
    resul = uK * expMenU / factK
    x -= 1
    if acumulado and x >= 0:
        return resul + distriPoison(x, media, acumulado)
    else:
        return resul

def distriNormal(x, mu, sigma, acumulado):
    if sigma <= 0:
        raise ValueError("La desviación estándar debe ser mayor que cero.")
    
    # Cálculo de la PDF
    densidad = (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
    
    if acumulado:
        # Cálculo de la CDF usando la aproximación de la función error (erf)
        z = (x - mu) / (sigma * math.sqrt(2))
        cdf = 0.5 * (1 + math.erf(z))
        return cdf
    else:
        return densidad

if __name__ == "__main__":
    n = 5
    disB = distriPoison(4, 7, True)
    disB = round(disB * 100, 2)

    print(disB)

    # Ejemplo de uso de la distribución normal
    x = 5
    mu = 10
    sigma = 2
    disN = distriNormal(x, mu, sigma, acumulado=False)  # PDF
    disN_acumulada = distriNormal(x, mu, sigma, acumulado=True)  # CDF

    print(f"Densidad normal (PDF) para x={x}, mu={mu}, sigma={sigma}: {disN}")
    print(f"Probabilidad acumulada (CDF) para x={x}, mu={mu}, sigma={sigma}: {disN_acumulada}")
