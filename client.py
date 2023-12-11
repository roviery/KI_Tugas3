import socket
import threading
import ast
import random
from rsa.rsa import RSA
from des.des import DES

class ChatClient:
  def __init__(self, host, port, username, des_key):
    self.host = host
    self.port = port
    self.username = username
    self.des_key = des_key
    self.des = DES(des_key)
    self.rsa = RSA(64)
    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.write_public_key()
    self.connect_to_server()

  def write_public_key(self):
    file_path = f"{self.username}.txt"
    with open(file_path, 'w') as file:
      file.write(f"{self.rsa.public_key}")

  def connect_to_server(self):
    try:
      self.client_socket.connect((self.host, self.port))
      print(f"[*] Connected to server on {self.host}:{self.port}")

      receive_thread = threading.Thread(target=self.receive_messages)
      receive_thread.start()

      self.send_messages()
    except KeyboardInterrupt:
      print("\n[*] Exiting...")
      self.client_socket.close()
      exit()

  def checkHex(self, s):
    for ch in s:
      if ((ch < '0' or ch > '9') and
        (ch < 'A' or ch > 'F')):
        return False
         
    return True

  def receive_messages(self):
    while True:
      try:
        message = self.client_socket.recv(2048).decode()
        if not message:
          break
        sender = message.split("-")[0]
        encrypted_des_key = tuple(ast.literal_eval(message.split("-")[1]))
        encrypted_message = message.split("-")[2]

        decrypted_des_key = int(self.rsa.decrypt(encrypted_des_key))
        des = DES(decrypted_des_key)
        decrypted_message = des.decrypt(encrypted_message)
        
        print(f"[{sender}] {decrypted_message}")
      except socket.error:
        print("Connection lost")
        break

  def send_messages(self):
    while True:
      message = input("")
      sender = message.split("-")[0]
      receiver = message.split("-")[1]
      ori_message = message.split("-", 2)[2]

      if (self.checkHex(ori_message) == False):
        print("Message bukan berupa Hex")
      else:
        file_path = f"{receiver}.txt"
        with open(file_path, 'r') as file:
          receiver_public_key = ast.literal_eval(file.read())

        encrypted_des_key = self.rsa.encrypt(receiver_public_key, str(self.des_key))
        encrypted_message = self.des.encrypt(ori_message)
        message = f"{sender}-{encrypted_des_key}-{encrypted_message}"
        self.client_socket.send(message.encode())


if __name__ == "__main__":
  username = input("Enter your username: ")
  client = ChatClient("127.0.0.1", 5555, username, random.randint(0, 1000))
