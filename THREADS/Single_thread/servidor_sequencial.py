import socket

HOST = "127.0.0.1"
PORT = 5000


def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()
        print(f"[sequencial] ouvindo em {HOST}:{PORT}", flush=True)

        while True:
            conexao, endereco = servidor.accept()
            print(f"[sequencial] {endereco} conectou", flush=True)

            # O servidor só volta ao accept() depois que este cliente termina.
            with conexao:
                while True:
                    dados = conexao.recv(1024)
                    if not dados:
                        break
                    conexao.sendall(dados)

            print(f"[sequencial] {endereco} desconectou", flush=True)


if __name__ == "__main__":
    try:
        iniciar_servidor()
    except KeyboardInterrupt:
        print("\n[sequencial] encerrado pelo usuário")
