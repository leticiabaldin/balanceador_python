import socket
import threading
import pickle

class CentralServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.clients = []  # Lista de clientes conectados
        self.processing_servers = []  # Lista de servidores de processamento conectados
        self.pending_tasks = {}  # Dicionário de tarefas pendentes

    def start(self):
        self.server.listen()
        print(f"Servidor central ouvindo em {self.host}:{self.port}")
        while True:
            client_socket, _ = self.server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = pickle.loads(data)
                if message['type'] == 'client':
                    self.clients.append(client_socket)
                    print("Cliente conectado.")
                elif message['type'] == 'processing_server':
                    self.processing_servers.append(client_socket)
                    print("Servidor de processamento conectado.")
                    self.balance_load()
            except Exception as e:
                print("Erro ao lidar com o cliente:", e)
                break

    def balance_load(self):
        # Verifica a carga atual dos servidores de processamento
        load_per_server = [0] * len(self.processing_servers)
        for task in self.pending_tasks.values():
            for i, server in enumerate(self.processing_servers):
                if task['server'] == server:
                    load_per_server[i] += 1

        # Distribui tarefas pendentes para servidores de processamento disponíveis
        for task_id, task in self.pending_tasks.items():
            if task['status'] == 'pending':
                min_load = min(load_per_server)
                min_load_index = load_per_server.index(min_load)
                self.pending_tasks[task_id]['status'] = 'processing'
                self.pending_tasks[task_id]['server'] = self.processing_servers[min_load_index]
                load_per_server[min_load_index] += 1
                self.processing_servers[min_load_index].send(pickle.dumps(task))

    def process_results(self, results):
        for result in results:
            task_id, is_prime = result
            if is_prime:
                client_socket = self.pending_tasks[task_id]['client']
                client_socket.send(pickle.dumps(f"O número {task_id} é primo."))
            else:
                client_socket = self.pending_tasks[task_id]['client']
                client_socket.send(pickle.dumps(f"O número {task_id} não é primo."))
            del self.pending_tasks[task_id]

    def is_prime(self, num):
        if num <= 1:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

if __name__ == "__main__":
    central_server = CentralServer("localhost", 5555)
    central_server.start()


#o cliente envia para o balanceador, e o balanceador envia para o servidor
# mesmo processo ao contrário