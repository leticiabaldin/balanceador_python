import socket
import pickle

class Client:
    def __init__(self, host, port, central_server_host, central_server_port):
        self.host = host
        self.port = port
        self.central_server_host = central_server_host
        self.central_server_port = central_server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client.connect((self.central_server_host, self.central_server_port))
        print(f"Conectado ao servidor central em {self.central_server_host}:{self.central_server_port}")

    def submit_task(self, task):
        try:
            data = pickle.dumps(task)
            self.client.send(data)
            print("Tarefa enviada para processamento.")
            
        except Exception as e:
            print("Erro ao enviar tarefa:", e)

    def receive_results(self):
        try:
            data = self.client.recv(1024)
            result = pickle.loads(data)
            print("Resultado recebido:", result)
        except Exception as e:
            print("Erro ao receber resultado:", e)

    def close_connection(self):
        self.client.close()

if __name__ == "__main__":
    client = Client("localhost", 5557, "localhost", 5555)
    client.connect()

    # Exemplo de submissão de tarefa
    task = {'type': 'prime_check', 'number': 17}  # Verificar se 17 é primo
    client.submit_task(task)

    # Receber resultados das tarefas processadas
    client.receive_results()

    client.close_connection()
