from math import factorial as fac

def combSinRep(n,r):
    return (fac(n)/(fac(r)*fac(n-r)));

def combConRep(n,r):
    return ( fac( n + r - 1 ) / ( fac( r ) * fac( n - 1) ) );

def perSinRep( n , r ):
    return ( fac( n ) / fac( n - r)  );

def perSinRep( n , r ):
    return ( fac( n ) / fac( n - r)  );

def perConRep( n , r ):
    return ( n ** r );

def perSinRepAll(n):
    return fac(n)

def perCir(n):
    return fac( n - 1 )
if __name__ == "__main__":
    print(combSinRep(4,2))
    print(combConRep(4,2))
    print(perSinRep(4,2))
    print(perConRep(4,2))
    print( perSinRepAll(4))
    print(perCir(4))