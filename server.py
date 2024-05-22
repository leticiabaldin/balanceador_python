import socket
import pickle
import time

class ProcessingServer:
    def __init__(self, host, port, central_server_host, central_server_port):
        self.host = host
        self.port = port
        self.central_server_host = central_server_host
        self.central_server_port = central_server_port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_central_server(self):
        self.server.connect((self.central_server_host, self.central_server_port))
        print(f"Conectado ao servidor central em {self.central_server_host}:{self.central_server_port}")

    def receive_tasks(self):
        while True:
            try:
                data = self.server.recv(1024)
                if not data:
                    break
                task = pickle.loads(data)
                result = self.process_task(task)
                print("teste")
                # Envia todos os resultados de uma vez
                self.server.send(pickle.dumps(result))
            except Exception as e:
                print("Erro ao receber ou processar tarefa:", e)
                break

    def process_task(self, task):
        if task['type'] == 'prime_check':
            number = task['number']
            is_prime = self.is_prime(number)
            time.sleep(1)
            return [(number, is_prime)]  # Enviar o resultado como uma lista de tuplas
        # Adicione outras lógicas para processamento de tarefas aqui
        return None

    def is_prime(self, num):
        if num <= 1:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    def start(self):
        self.connect_to_central_server()
        self.receive_tasks()

if __name__ == "__main__":
    processing_server = ProcessingServer("localhost", 5556, "localhost", 5555)
    processing_server.start()
