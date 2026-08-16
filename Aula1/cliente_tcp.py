import socket
import time
import logging

HOST = "127.0.0.1"
PORT = 5000

logger_tcp = logging.getLogger("cliente_tcp")
logger_tcp.setLevel(logging.INFO)
if not logger_tcp.handlers:
    # mode='w' garante que o arquivo seja sobrescrito a cada execução
    handler_tcp = logging.FileHandler("cliente_tcp.log", mode='w', encoding="utf-8")
    handler_tcp.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger_tcp.addHandler(handler_tcp)

def gerar_tcp():
    mensagens = []

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen(1)

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    conexao, endereco = servidor.accept()

    for i in range(1, 101):
        mensagem = f"Mensagem TCP {i:03d}"
        inicio = time.time()

        cliente.sendall(mensagem.encode())
        logger_tcp.info(f"Enviado (Iteração {i}): {mensagem}")

        recebido = conexao.recv(1024)

        resposta = b"ECO: " + recebido
        conexao.sendall(resposta)

        resposta_cliente = cliente.recv(1024)
        fim = time.time()
        rtt = (fim - inicio) * 1000

        logger_tcp.info(f"Recebido (Iteração {i}): {resposta_cliente.decode()} | RTT: {rtt:.2f}ms")

        mensagens.append(
            f"{i}. Enviada: `{mensagem}` | "
            f"Resposta: `{resposta_cliente.decode()}` | "
            f"RTT: `{rtt:.2f}ms`"
        )

    cliente.close()
    conexao.close()
    servidor.close()

    return mensagens

if __name__ == "__main__":
    for mensagem in gerar_tcp():
        print(mensagem)
