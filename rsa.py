import random
import math
from sympy import isprime

class RSA:
  def __init__(self, key_bits):
    self.key_bits = key_bits
    self.public_key, self.private_key = self.generate_keypair()

  def generate_prime(self):
    while True:
      num = random.getrandbits(self.key_bits)
      if isprime(num):
        return num
      
  def gcd(self, a, b):
    return math.gcd(a, b)
  
  def modinv(self, a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
      q = a // m
      m, a = a % m, m
      x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1
  
  def generate_keypair(self):
    p = self.generate_prime()
    q = self.generate_prime()
    n = p * q
    toitent_n = (p-1)*(q-1)

    while True:
      e = random.randint(2, toitent_n - 1)
      if self.gcd(e, toitent_n) == 1:
        break

    d = self.modinv(e, toitent_n)
    return ((n, e), (n, d))
  
  def encrypt(self, message):
    n, e = self.public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

  def decrypt(self, encrypted_message):
    n, d = self.private_key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
    return decrypted_message
  
if __name__ == "__main__":
  key_bits = 64
  rsa_instance = RSA(key_bits)

  original_message = "Hello, passwordnya adalah sdadwd123132adw"

  encrypted_message = rsa_instance.encrypt(original_message)

  decrypted_message = rsa_instance.decrypt(encrypted_message)

  print(f"Original Message: {original_message}")
  print(f"Encrypted Message: {encrypted_message}")
  print(f"Decrypted Message: {decrypted_message}")