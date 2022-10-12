import random;
import string;
import math;

class rsa:
    abc = list(string.ascii_letters + string.digits + string.punctuation + " "); # List of all lowercase letters, uppercase letters, numbers and punctuation plus a whitespace

    # Generates a public and private key pair
    def generateKeyPair(p, q):
        n = p * q;
        phi = (p - 1)*(q - 1) ;
        e = rsa.generateE(phi);
        d = rsa.egcd(e, phi) # Generates private key using extended euclidean algorithm

        return ((e, n), (d, n)); # Returns public key (e,n) and private key (d,n) as tuple;

    # Extended Euclidean algorithm - This was taken from https://www.tutorialspoint.com/python-program-for-extended-euclidean-algorithms and tweaked to suit my needs
    def egcd(e: int, phi: int):
        d = 0;
        x1 = 0;
        x2 = 1;
        y1 = 1;
        tempPhi = phi;

        while e > 0:
            temp1 = tempPhi//e;
            temp2 = tempPhi - temp1 * e;
            tempPhi = e;
            e = temp2;

            x = x2 - temp1 * x1;
            y = d - temp1 * y1;

            x2 = x1;
            x1 = x;
            d = y1;
            y1 = y;

        if tempPhi == 1:
            return d + phi;

    # Generates e. E is a coprime of phi because the only factor in common is 1.
    def generateE(phi: int):
        e = random.SystemRandom().randrange(1, phi); # Generate test e (less than phi)
        if math.gcd(e, phi) != 1: # If the test e is not a coprime of phi
            return rsa.generateE(phi); # Recursively call this function until e is a coprime of phi
        return e;

    # Encrypt using a generate public key and a userdefined plainText
    def encrypt(publicKey: int, plainText: str):
        # Iterates through plainText
        # Turns each character into a number using abc (an array of characters and numbers)
        # Runs the (p^e)%n using provided public key
        # Returns the cipherText as bytes

        return bytes([(rsa.abc.index(char)**publicKey[0] % publicKey[1]) for char in plainText]);

    # Encrypt using a generate private key and a userdefined cipherText
    def decrypt(privateKey: int, cipherText: str):
        # Iterates through cipherText
        # Turns each character into a number using abc (an array of characters and numbers)
        # Runs the (c^e)%n using provided private key where c is the ciphertext
        # Returns the plainText

        return "".join([rsa.abc[(char**privateKey[0]) % privateKey[1]] for char in cipherText]);

    
# Driver Code
p = 11; # Prime 1
q = 13; # Prime 2
publicKey, privateKey = rsa.generateKeyPair(p, q); # Generate keypair

encrypted = rsa.encrypt(publicKey,"This is a test!");
decrypted = rsa.decrypt(privateKey, encrypted);

print(encrypted);
print(decrypted);
