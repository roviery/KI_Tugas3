import socket
import threading
import ast
from rsa import RSA

class ChatClient:
  def __init__(self, host, port, username):
    self.host = host
    self.port = port
    self.username = username
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

  def receive_messages(self):
    while True:
      try:
        message = self.client_socket.recv(2048).decode()
        if not message:
          break

        sender = message.split(" ")[0]
        encrypted_message = tuple(ast.literal_eval(message.split(" ", 2)[2]))
        ori_message = self.rsa.decrypt(encrypted_message)
        print(f"[{sender}] {ori_message}")
      except socket.error:
        print("Connection lost")
        break

  def send_messages(self):
    while True:
      message = input("")
      sender = message.split(" ")[0]
      receiver = message.split(" ")[1]
      ori_message = message.split(" ", 2)[2]

      file_path = f"{receiver}.txt"
      with open(file_path, 'r') as file:
        receiver_public_key = ast.literal_eval(file.read())

      encrypted_message = self.rsa.encrypt(receiver_public_key, ori_message)
      encrypted_message_str = "["
      for m in encrypted_message:
        print
        encrypted_message_str += f"{m}, "
      encrypted_message_str = encrypted_message_str[:-2]
      encrypted_message_str += "]"
      message = f"{sender} {receiver} {encrypted_message_str}"
      self.client_socket.send(message.encode())

if __name__ == "__main__":
  username = input("Enter your username: ")
  client = ChatClient("127.0.0.1", 5555, username)
