import socket
import sys
import threading
import time

HOST = "127.0.0.1"
PORT = 5000


def cliente(numero, mensagens, resultados):
    inicio = time.perf_counter()
    try:
        with socket.create_connection((HOST, PORT), timeout=10) as conexao:
            for mensagem in mensagens:
                conexao.sendall(f"cliente {numero}: {mensagem}".encode("utf-8"))
                eco = conexao.recv(1024).decode("utf-8")
                if not eco:
                    raise ConnectionError("o servidor não respondeu")
        resultados[numero] = time.perf_counter() - inicio
    except Exception as erro:
        resultados[numero] = f"erro: {erro}"


def executar_carga(numero_clientes=10, mensagens_por_cliente=3):
    resultados = {}
    threads = []
    mensagens = [f"mensagem {i + 1}" for i in range(mensagens_por_cliente)]
    inicio_total = time.perf_counter()

    for numero in range(1, numero_clientes + 1):
        thread = threading.Thread(
            target=cliente,
            args=(numero, mensagens, resultados),
            name=f"cliente-{numero}",
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    tempo_total = time.perf_counter() - inicio_total
    tempos = [valor for valor in resultados.values() if isinstance(valor, float)]
    tempo_medio = sum(tempos) / len(tempos) if tempos else 0

    print(f"clientes: {numero_clientes}")
    print(f"mensagens por cliente: {mensagens_por_cliente}")
    print(f"tempo total: {tempo_total:.4f} s")
    print(f"tempo médio por cliente: {tempo_medio:.4f} s")
    print(f"clientes concluídos: {len(tempos)}")
    for numero in sorted(resultados):
        print(f"cliente {numero}: {resultados[numero]}")


if __name__ == "__main__":
    quantidade = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    executar_carga(quantidade)
