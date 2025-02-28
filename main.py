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





# def find_generator(p, q):
#     """Trouve un générateur g dans (Z/pZ)* de l'ordre q"""
#     i=0
#     while True:
#         i+=1
#         print(i)
#         h = secrets.randbelow(p - 4) + 2  # h ∈ [2, p-2]
#         g = gmpy2.powmod(h, (p - 1) // q, p)  # g = h^((p-1)/q) mod p
#         if g > 1 and gmpy2.powmod(g, q, p) == 1:  # Vérifier g^q ≡ 1 (mod p)
#             return g
# def find_generator_at_least_q(p, q, k):
#     nb_iteration =0
#     while True:
#         nb_iteration +=1
#         print(nb_iteration)
#         h = gmpy2.mpz(secrets.randbelow(p - 2)) + 2  # h ∈ [2, p-2]
#         g = pow(h, k, p)  # g = h^k mod p, ce qui assure un ordre multiple de q
        
#         if pow(g, q, p) == 1 and pow(g, k, p) != 1 :  # Vérifie que g^q ≡ 1 mod p
#             return g
def find_generator(p, q, k):
    cpt=0
    for g in range(2,p-2):
        cpt+=1
        if cpt %10000 == 0:
            print(cpt)
        if ExpMod(g,q,p) ==1 and  ExpMod(g,k,p) !=1:
            return g
        
    return None

"""
1. Choisir q un nombre premier d’au moins N = 256 bits.
2. Choisir al éatoirement un nombre k d’au moins O = 1792 bits.
3. Si p = 1 + kq n’est pas premier, revenir `a l’ ́etape 2.
4. Choisir un  ́el ́ement g compris entre 2 et p − 2.
5. V ́erifier si gq ≡ 1 (mod p) et si gk != 1 (mod p). Sinon, retourner `a l’ ́etape 4.
 tel que q ̸= 1 et gq ≡ 1 (mod p) 

"""
def KeyGen(N, O):
    q = gmpy2.next_prime(secrets.randbits(N)) 
    k = gmpy2.mpz(secrets.randbits(O))  
    p = gmpy2.add(1, gmpy2.mul(k, q))  

    # Vérifier que p est premier
    while not gmpy2.is_prime(p, 10):
        k = gmpy2.mpz(secrets.randbits(O))  
        p = gmpy2.add(1, gmpy2.mul(k, q))  

    while True:
        h = gmpy2.mpz(secrets.randbelow(p - 2) + 2)  # h ∈ [2, p-2]
        g = ExpMod(h, (p - 1) // q, p)  # Utilisation du PTF

        if ExpMod(g, q, p) == 1 and ExpMod(g, k, p) != 1:
            break  

    return p, q, g
# def KeyGen(N,O):
#     q = gmpy2.next_prime(secrets.randbits(N)) 
#     k = gmpy2.mpz(secrets.randbits(O))   #Format grand entier
#     p = gmpy2.add(1,gmpy2.mul(k,q))
#     fermat =1 #Paramètre pour faire le test avec Fermat
#     while not gmpy2.is_prime(p,1):
#         k = gmpy2.mpz(secrets.randbits(O))   #Format grand entier
#         p = gmpy2.add(1,gmpy2.mul(k,q))
        
        
#     nb_iteration =0
#     # # g = find_generator(p, q)
#     # g = find_generator(p, q, k)
    


#     g = gmpy2.add(gmpy2.mpz(secrets.randbelow(p-4)),2)  #Nombnre entre 2 et p-2 
#     while ExpMod(g,q,p) !=1 or  ExpMod(g,k,p) ==1:
#         nb_iteration +=1
#         if nb_iteration % 10000 ==0:
#             print(nb_iteration)
        
#         # g =find_generator(p, q)
#         g = gmpy2.add(gmpy2.mpz(secrets.randbelow(p-2)),2)
        
#     print("Reussi")
#     return

#parm N>=256,O>=1792

KeyGen(256,1792)