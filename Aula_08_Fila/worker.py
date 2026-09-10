from time import perf_counter

import fila
from modelo import carregar_modelo


def main():
    modelo = carregar_modelo()
    print("[worker] modelo carregado, aguardando tarefas (Ctrl+C para sair)", flush=True)

    while True:
        tarefa = fila.proxima_tarefa(timeout=5)
        if tarefa is None:
            continue

        inicio = perf_counter()
        try:
            resultado = modelo.prever(tarefa["texto"])
            resultado["status"] = "pronto"
            resultado["tempo_ms"] = round((perf_counter() - inicio) * 1000, 2)

            fila.guardar_resultado(tarefa["id"], resultado)
            print(f"[worker] id={tarefa['id']} {resultado['sentimento']} "
                  f"confianca={resultado['confianca']} tempo={resultado['tempo_ms']} ms", flush=True)
        except Exception as erro:
            print(f"[worker] erro na tarefa id={tarefa['id']}: {erro}", flush=True)


if __name__ == "__main__":
    main()
