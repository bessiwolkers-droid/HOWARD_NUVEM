"""Worker que consome a fila e executa a inferência."""
import logging
import time

from app import fila
from app.modelo import carregar_modelo

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("worker")
MAX_TENTATIVAS = 3


def main():
    logger.info("carregando modelo")
    modelo = carregar_modelo()
    logger.info("worker pronto")

    while True:
        tarefa = fila.proxima_tarefa(timeout=5)
        if tarefa is None:
            continue

        inicio = time.perf_counter()
        tentativa = int(tarefa.get("tentativas", 0)) + 1
        tarefa["tentativas"] = tentativa
        logger.info("processando id=%s tentativa=%d", tarefa["id"], tentativa)
        try:
            resultado = modelo.prever(tarefa["texto"])
            resultado.update({
                "status": "pronto",
                "tempo_ms": round((time.perf_counter() - inicio) * 1000, 2),
            })
            fila.guardar_resultado(tarefa["id"], resultado)
            logger.info("finalizado id=%s tamanho=%d tempo_ms=%.2f", tarefa["id"], len(tarefa["texto"]), resultado["tempo_ms"])
        except Exception as erro:  # noqa: BLE001
            logger.exception("erro id=%s tentativa=%d", tarefa["id"], tentativa)
            if tentativa < MAX_TENTATIVAS:
                fila.cliente().rpush(fila.FILA_TAREFAS, __import__("json").dumps(tarefa))
            else:
                fila.mandar_para_descarte(tarefa, str(erro))


if __name__ == "__main__":
    main()
