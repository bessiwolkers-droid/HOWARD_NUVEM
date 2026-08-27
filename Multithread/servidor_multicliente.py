import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def atender_cliente(conexao, endereco):
    """Atende um cliente em uma thread separada."""
    print(f"[servidor] {endereco} conectou", flush=True)
    try:
        while True:
            dados = conexao.recv(1024)
            if not dados:
                break
            mensagem = dados.decode("utf-8")
            print(f"[servidor] {endereco}: {mensagem}", flush=True)
            conexao.sendall(dados)  # devolve a mesma mensagem, como eco
    except ConnectionResetError:
        print(f"[servidor] {endereco} encerrou a conexão", flush=True)
    finally:
        conexao.close()
        print(f"[servidor] {endereco} desconectou", flush=True)


def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()
        print(f"[servidor] ouvindo em {HOST}:{PORT}", flush=True)

        while True:
            conexao, endereco = servidor.accept()
            thread = threading.Thread(
                target=atender_cliente,
                args=(conexao, endereco),
                daemon=True,
            )
            thread.start()
            print(f"[servidor] thread {thread.name} criada para {endereco}", flush=True)


if __name__ == "__main__":
    try:
        iniciar_servidor()
    except KeyboardInterrupt:
        print("\n[servidor] encerrado pelo usuário")
