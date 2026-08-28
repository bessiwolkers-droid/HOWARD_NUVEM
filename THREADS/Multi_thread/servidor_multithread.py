import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def atender_cliente(conexao, endereco):
    """Atende um cliente sem bloquear o laço principal do servidor."""
    print(f"[multithread] {endereco} conectou na thread {threading.current_thread().name}", flush=True)
    try:
        with conexao:
            while True:
                dados = conexao.recv(1024)
                if not dados:
                    break
                conexao.sendall(dados)
    except ConnectionResetError:
        print(f"[multithread] {endereco} encerrou a conexão abruptamente", flush=True)
    finally:
        print(f"[multithread] {endereco} desconectou", flush=True)


def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()
        print(f"[multithread] ouvindo em {HOST}:{PORT}", flush=True)

        while True:
            conexao, endereco = servidor.accept()
            thread = threading.Thread(
                target=atender_cliente,
                args=(conexao, endereco),
                name=f"cliente-{endereco[1]}",
                daemon=True,
            )
            thread.start()
            # O laço principal imediatamente aceita a próxima conexão.


if __name__ == "__main__":
    try:
        iniciar_servidor()
    except KeyboardInterrupt:
        print("\n[multithread] encerrado pelo usuário")
