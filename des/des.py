from .table import *
import random

class DES:
  def __init__(self, key):
    self.key = self.int_to_binary(key)
    self.rk, self.rkb, self.rk_reversed, self.rkb_reserved = self.generate_round_key()

  def int_to_binary(self, number):
    try:
      binary = bin(number)[2:].zfill(64)
      return binary
    except ValueError:
      return "Invalid int input"
  
  def binary_to_hex(self, binary_string):
    try:
      decimal_number = int(binary_string, 2)
      hex_string = hex(decimal_number)[2:]
      return hex_string.upper() 
    except ValueError:
      return "Invalid binary input"
    
  def hex_to_binary(self, hex_string):
    try:
      hex_string = hex_string.lstrip('0x')
      decimal_number = int(hex_string, 16)
      binary_string = bin(decimal_number)[2:]
      binary_string = binary_string.zfill(64)
      return binary_string
    except ValueError:
      return "Invalid hexadecimal input"
    
  def binary_to_decimal(self, binary):
    decimal, i = 0, 0
    while(binary != 0):
      dec = binary % 10
      decimal = decimal + dec * pow(2, i)
      binary = binary//10
      i += 1
    return decimal
  
  def decimal_to_binary(self, num):
    res = bin(num).replace("0b", "")
    if(len(res) % 4 != 0):
      div = len(res) / 4
      div = int(div)
      counter = (4 * (div + 1)) - len(res)
      for i in range(0, counter):
        res = '0' + res
    return res
  
  def xor(self, a, b):
    ans = ""
    for i in range(len(a)):
      if a[i] == b[i]:
        ans = ans + "0"
      else:
        ans = ans + "1"
    return ans  
    
  def shift_left(self, k, nth_shifts):
    return k[nth_shifts:] + k[:nth_shifts]
  
  def permute(self, k, arr, n):
    permutation = ""
    for i in range(0, n):
      permutation = permutation + k[arr[i] - 1]
    return permutation
  
  def generate_round_key(self):
    key = self.permute(self.key, keyp, 56)
    left = key[0:28]
    right = key[28:56]
    rk = []
    rkb = []

    for i in range(0, 16):
      left = self.shift_left(left, shift_table[i])
      right = self.shift_left(right, shift_table[i])

      # Combination of left and right string
      combine_str = left + right

      # Compression of key from 56 to 48 bits
      round_key = self.permute(combine_str, key_comp, 48)

      rkb.append(round_key)
      rk.append(self.binary_to_hex(round_key))

    rk_reversed = rk[::-1]
    rkb_reversed = rkb[::-1]

    return rk, rkb, rk_reversed, rkb_reversed
  
  def encrypt(self, plain_text):
    plain_text = self.hex_to_binary(plain_text)
    # Initial Permutation
    plain_text = self.permute(plain_text, initial_perm, 64)

    # Splitting
    left = plain_text[0:32]
    right = plain_text[32:64]
    for i in range(0, 16):
      # Expansion D-box: from 32 bits to 48 bits
      right_expanded = self.permute(right, exp_d, 48)

      # XOR RoundKey[i] and right_expanded
      xor_x = self.xor(right_expanded, self.rkb[i])

      # S-box: subtituting the value from s-box table by calculating row and column
      sbox_str = ""
      for j in range(0, 8):
        row = self.binary_to_decimal(int(xor_x[j*6] + xor_x[j*6+5]))
        col = self.binary_to_decimal(int(xor_x[j*6+1] + xor_x[j*6+2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
        val = sbox[j][row][col]
        sbox_str = sbox_str + self.decimal_to_binary(val)

      # Straight D-box: After substituting rearranging the bits
      sbox_str = self.permute(sbox_str, per, 32)
      
      # XOR left and sbox_str
      result = self.xor(left, sbox_str)
      left = result

      # Swapper
      if(i != 15):
        left, right = right, left
      
    # Combination
    combine = left + right

    # Final permutation: final rearranging of bits to get cipher text
    cipher_text = self.permute(combine, final_perm, 64)
    return self.binary_to_hex(cipher_text)
  
  def decrypt(self, plain_text):
    plain_text = self.hex_to_binary(plain_text)
    # Initial Permutation
    plain_text = self.permute(plain_text, initial_perm, 64)

    # Splitting
    left = plain_text[0:32]
    right = plain_text[32:64]

    for i in range(0, 16):
      # Expansion D-box: from 32 bits to 48 bits
      right_expanded = self.permute(right, exp_d, 48)

      # XOR RoundKey[i] and right_expanded
      xor_x = self.xor(right_expanded, self.rkb_reserved[i])

      # S-box: subtituting the value from s-box table by calculating row and column
      sbox_str = ""
      for j in range(0, 8):
        row = self.binary_to_decimal(int(xor_x[j*6] + xor_x[j*6+5]))
        col = self.binary_to_decimal(int(xor_x[j*6+1] + xor_x[j*6+2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
        val = sbox[j][row][col]
        sbox_str = sbox_str + self.decimal_to_binary(val)

      # Straight D-box: After substituting rearranging the bits
      sbox_str = self.permute(sbox_str, per, 32)
      
      # XOR left and sbox_str
      result = self.xor(left, sbox_str)
      left = result

      # Swapper
      if(i != 15):
        left, right = right, left
      
    # Combination
    combine = left + right

    # Final permutation: final rearranging of bits to get cipher text
    cipher_text = self.permute(combine, final_perm, 64)
    return self.binary_to_hex(cipher_text)


if __name__ == "__main__":
  key = random.randint(0, 1000)
  des = DES(key)

  original_message = "ABCD1234ABCD1234"

  encrypted_message = des.encrypt(original_message)

  decrypted_message = des.decrypt(encrypted_message)

  print(f"\nOriginal Message: {original_message}")
  print(f"Encrypted Message: {encrypted_message}")
  print(f"Decrypted Message: {decrypted_message}")
