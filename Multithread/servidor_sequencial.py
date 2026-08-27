import socket

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"[servidor] ouvindo em {HOST}:{PORT}", flush=True)

    while True:
        conexao, endereco = servidor.accept()
        print(f"[servidor] {endereco} conectou", flush=True)
        with conexao:
            while True:
                dados = conexao.recv(1024)
                if not dados:
                    break
                conexao.sendall(dados)
