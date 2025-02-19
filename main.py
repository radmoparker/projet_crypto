import secrets
import gmpy2

""" fonction ExpMod() qui prend en entr ée p, g et a et qui renvoie en sortie A ≡ ga mod p."""
def ExpMod(g,a,p):
    return gmpy2.powmod(g, a, p)

def puissance(g, a, p):
    """Calcule g^a mod p en utilisant l'exponentiation binaire récursive avec gmpy2."""
    g = gmpy2.mpz(g)
    a = gmpy2.mpz(a)
    p = gmpy2.mpz(p)

    if a == 1:
        return gmpy2.mod(g, p)
    elif gmpy2.is_even(a):  # Vérifie si a est pair puissance(g2, a/2),
        half = puissance(gmpy2.mod(gmpy2.mul(g, g), p), gmpy2.f_div(a, 2), p)
        return half
    else:  # a est impair
        half = puissance(gmpy2.mod(gmpy2.mul(g, g), p), gmpy2.f_div(a - 1, 2), p)
        return gmpy2.mod(gmpy2.mul(g, half), p)
    


# Test de puissance = gmpy2.powmod
# print("Test de puissance = gmpy2.powmod ")
# for i in range(10):
#     p = gmpy2.next_prime(secrets.randbits(2048))    # entier premier
#     a = gmpy2.mpz(secrets.randbits(256))   #Format grand entier
#     g = gmpy2.mpz(secrets.randbelow(p))

#     print(f"(gmpy2.powmod(g{i}, a{i}, p{i}) == puissance(g, a, p))? : {gmpy2.powmod(g, a, p) == puissance(g, a, p)}")



"""
1. Choisir q un nombre premier d’au moins N = 256 bits.
2. Choisir al éatoirement un nombre k d’au moins O = 1792 bits.
3. Si p = 1 + kq n’est pas premier, revenir `a l’ ́etape 2.
4. Choisir un  ́el ́ement g compris entre 2 et p − 2.
5. V ́erifier si gq ≡ 1 (mod p) et si gk != 1 (mod p). Sinon, retourner `a l’ ́etape 4."""
def KeyGen(N,O):
    q = gmpy2.next_prime(secrets.randbits(N)) 
    k = gmpy2.mpz(secrets.randbits(O))   #Format grand entier
    p = gmpy2.add(1,gmpy2.mul(k,q))
    fermat =1 #Paramètre pour faire le test avec Fermat
    while not gmpy2.is_prime(p):
        k = gmpy2.mpz(secrets.randbits(O))   #Format grand entier
        p = gmpy2.add(1,gmpy2.mul(k,q))
    
    g = gmpy2.add(gmpy2.mpz(secrets.randbelow(p-4)),2)  #Nombnre entre 2 et p-2
    while ExpMod(g,q,p) !=1 or  ExpMod(g,k,p) ==1:
        # if (ExpMod(g,q,p) !=1):
        #     print("ok A")
        # if (ExpMod(g,k,p) ==1):
        #     print("ok B")
            
        g = gmpy2.add(gmpy2.mpz(secrets.randbelow(p-4)),2)
        
    print("Reussi")
    return

#parm N>=256,O>=1792

KeyGen(256,1792)