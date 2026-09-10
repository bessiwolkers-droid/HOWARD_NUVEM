import sys
from time import perf_counter, sleep

import requests

BASE = "http://localhost:8000"


def enviar(texto):
    resposta = requests.post(f"{BASE}/predict", json={"texto": texto}, timeout=10)
    resposta.raise_for_status()
    return resposta.json()["id"]


def esperar(tarefa_id, tentativas=40):
    for _ in range(tentativas):
        resposta = requests.get(f"{BASE}/resultado/{tarefa_id}", timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
        if dados.get("status") == "pronto":
            return dados
        sleep(0.5)
    return None


if __name__ == "__main__":
    texto = " ".join(sys.argv[1:]) or "o atendimento foi excelente e muito rapido"

    inicio = perf_counter()
    tarefa_id = enviar(texto)
    print(f"id recebido em {round((perf_counter() - inicio) * 1000, 2)} ms: {tarefa_id}")

    dados = esperar(tarefa_id)
    if dados is None:
        print("o resultado nao ficou pronto no tempo esperado")
    else:
        print(f"resultado: {dados['sentimento']} (confianca {dados['confianca']}) "
              f"inferencia em {dados['tempo_ms']} ms")
