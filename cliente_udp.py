import socket
import time
import logging

HOST = "127.0.0.1"
PORT = 5001

logger_udp = logging.getLogger("cliente_udp")
logger_udp.setLevel(logging.INFO)
if not logger_udp.handlers:
    # mode='w' garante que o arquivo seja sobrescrito a cada execução
    handler_udp = logging.FileHandler("cliente_udp.log", mode='w', encoding="utf-8")
    handler_udp.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger_udp.addHandler(handler_udp)

def gerar_udp():
    mensagens = []

    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORT))

    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for i in range(1, 101):
        mensagem = f"Mensagem UDP {i:03d}"
        inicio = time.time()

        cliente.sendto(
            mensagem.encode(),
            (HOST, PORT)
        )
        logger_udp.info(f"Enviado (Iteração {i}): {mensagem}")

        recebido, endereco = servidor.recvfrom(1024)

        resposta = f"ECO: {recebido.decode()}"

        servidor.sendto(
            resposta.encode(),
            endereco
        )

        resposta_cliente, _ = cliente.recvfrom(1024)
        fim = time.time()
        rtt = (fim - inicio) * 1000

        logger_udp.info(f"Recebido (Iteração {i}): {resposta_cliente.decode()} | RTT: {rtt:.2f}ms")

        mensagens.append(
            f"{i}. Enviada: `{mensagem}` | "
            f"Resposta: `{resposta_cliente.decode()}` | "
            f"RTT: `{rtt:.2f}ms`"
        )

    cliente.close()
    servidor.close()

    return mensagens

if __name__ == "__main__":
    for mensagem in gerar_udp():
        print(mensagem)
