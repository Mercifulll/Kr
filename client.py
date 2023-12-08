import socket
import pickle
import numpy as np

def generate_and_fill_matrices():
    # Генерація розмірів матриць (N, M, L)
    N = np.random.randint(1001, 2000)
    M = np.random.randint(1001, 2000)
    L = np.random.randint(1001, 2000)

    # Генерація матриць з випадковими розмірами
    matrix_a = np.random.random((N, M))
    matrix_b = np.random.random((M, L))

    return matrix_a, matrix_b

def communicate_with_server(matrix_a, matrix_b):
    # З'єднання з сервером
    server_address = ('127.0.0.1', 12345)  # IP та порт сервера
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_address)

        # Відправлення розмірів та матриць
        data_to_send = {'matrix_a': matrix_a, 'matrix_b': matrix_b}
        serialized_data = pickle.dumps(data_to_send)
        client_socket.sendall(serialized_data)

        # Отримання результату від сервера
        received_data = client_socket.recv(4096)
        result = pickle.loads(received_data)

    return result

if __name__ == "__main__":
    # Генерація та заповнення матриць
    matrix_a, matrix_b = generate_and_fill_matrices()

    result_from_server = communicate_with_server(matrix_a, matrix_b)

    print("\nResult from server:")
    print(result_from_server)
