import secrets
import gmpy2
import hashlib
import string

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

    # p premier
    while not gmpy2.is_prime(p, 10):
        k = gmpy2.mpz(secrets.randbits(O))  
        p = gmpy2.add(1, gmpy2.mul(k, q))  

    trouve = False
    while not trouve:
        h = gmpy2.mpz(secrets.randbelow(p - 2) + 2)  # h ∈ [2, p-2]
        g = ExpMod(h, (p - 1) // q, p)  # Utilisation du Petit theorem de Fermat

        if ExpMod(g, q, p) == 1 and ExpMod(g, k, p) != 1:
            trouve = True  

    return p, q, g

# Question 6
def Key(p,q,g):
    ks = gmpy2.mpz(secrets.randbelow(q - 2) + 2)
    kp = ExpMod(g, ks, p)
    
    return kp,ks

# Question 8
def Sign(p, q, g, ks, M):

    R,r = Key(p,q,g)
    concatenation = str(R).encode() + M.encode() # encode() transforme une chaine de caractère séquence d'octet
    h = hashlib.sha256(concatenation).digest()   # Converti le hashé en sequence d'octet 
    c = ExpMod(gmpy2.mpz(int.from_bytes(h, byteorder="big")),1,q)   #On convertit h en int avec gmpy2 avant le calcul expmod
    
    a = ExpMod(gmpy2.sub(r, gmpy2.mul(c, ks)),1,q )
    
    return c,a

def Verify(p, q, g, kp, M,a,c):
    R_prim = ExpMod(gmpy2.mul(ExpMod(g,a,p),ExpMod(kp,c,p)),1,p)
    concatenation = str(R_prim).encode() + M.encode() # encode() transforme une chaine de caractère séquence d'octet
    h_str = hashlib.sha256(concatenation).digest()
    h = gmpy2.mpz(int.from_bytes(h_str, byteorder="big")) #On convertit h en int avec gmpy2 avant le calcul expmod
    
    result = ExpMod(h,1,q)  

    
    return ( c == result)



print("Nous allons tester 100 valeurs de M (longueur entre 256 et 2048 caractères). Les 80 premières seront signés avec une clé secrète valide, les autres avec une clé invalide ")

#Génération aléatoire d'une chaine de n  caractère ( 256 <= n <= 2048)
def random_string_with_length():
    length = secrets.randbelow(2048 - 256 + 1) + 256
    alphabet = string.ascii_letters + string.digits + string.punctuation  # Lettres + chiffres + symboles
    return ''.join(secrets.choice(alphabet) for _ in range(length)),length

#Test sur 100 Messages
for i in range (1,81):
    #param N>=256,O>=1792
    p,q,g = KeyGen(256,1792)
    kp,ks = Key(p,q,g)
    M,length = random_string_with_length()
    c,a = Sign(p, q, g, ks, M)
    reponse = Verify(p, q, g, kp, M,a,c)
    print(f"Message {i} de longueur {length} est correctement vérifié ? réponse = {reponse}")
for i in range(80,101):
    #param N>=256,O>=1792
    p,q,g = KeyGen(256,1792)
    kp,ks = Key(p,q,g)
    M,length = random_string_with_length()
    ks_fausse = gmpy2.mpz(secrets.randbelow(q - 2) + 2)
    c,a = Sign(p, q, g, ks_fausse, M)
    reponse = Verify(p, q, g, kp, M,a,c)
    print(f"Message {i} de longueur {length} est correctement vérifié ? réponse = {reponse}")
    
