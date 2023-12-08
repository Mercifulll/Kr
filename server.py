import socket
import pickle
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def matrix_multiply(matrix_a, matrix_b):
    # Реалізація множення матриць (ваша логіка обчислень)
    result = np.dot(matrix_a, matrix_b)
    return result

def handle_client(client_socket):
    # Отримання розмірів та матриць від клієнта
    received_data = client_socket.recv(4096)
    data_from_client = pickle.loads(received_data)

    matrix_a = data_from_client['matrix_a']
    matrix_b = data_from_client['matrix_b']

    try:
        # Обчислення результату
        result = matrix_multiply(matrix_a, matrix_b)

        # Відправлення результату клієнту
        serialized_result = pickle.dumps(result)
        client_socket.sendall(serialized_result)
    except Exception as e:
        error_message = f"Error during matrix multiplication: {str(e)}"
        client_socket.sendall(error_message.encode('utf-8'))

    client_socket.close()

def server_listen():
    server_address = ('127.0.0.1', 12345)  # IP та порт сервера

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(server_address)
        server_socket.listen()

        print("Server is listening for connections...")

        with ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Connected to {client_address}")

                # Обробка кожного клієнта у власному потоці
                executor.submit(handle_client, client_socket)

if __name__ == "__main__":
    server_listen()
