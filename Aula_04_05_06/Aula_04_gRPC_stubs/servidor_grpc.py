"""Interface gRPC do serviço de inferência."""
import logging
import time
from concurrent import futures

import grpc

from app.modelo import carregar_modelo

try:
    import inferencia_pb2
    import inferencia_pb2_grpc
except ImportError:
    raise SystemExit("Gere os stubs com: python3 -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/inferencia.proto")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("servidor_grpc")


class ServicoInferencia(inferencia_pb2_grpc.InferenciaServicer):
    def __init__(self):
        logger.info("carregando modelo")
        self.modelo = carregar_modelo()
        logger.info("modelo pronto")

    def Prever(self, request, context):
        inicio = time.perf_counter()
        resultado = self.modelo.prever(request.texto)
        tempo_ms = (time.perf_counter() - inicio) * 1000
        logger.info("rpc=Prever tamanho=%d tempo_ms=%.2f", len(request.texto), tempo_ms)
        return inferencia_pb2.RespostaPrever(
            texto=resultado["texto"],
            sentimento=resultado["sentimento"],
            confianca=resultado["confianca"],
        )

    def PreverLote(self, request, context):
        inicio = time.perf_counter()
        resultados = [self.modelo.prever(texto) for texto in request.textos]
        tempo_ms = (time.perf_counter() - inicio) * 1000
        logger.info("rpc=PreverLote itens=%d tamanho=%d tempo_ms=%.2f", len(request.textos), sum(len(t) for t in request.textos), tempo_ms)
        return inferencia_pb2.RespostaLote(
            resultados=[
                inferencia_pb2.RespostaPrever(
                    texto=r["texto"], sentimento=r["sentimento"], confianca=r["confianca"]
                )
                for r in resultados
            ]
        )


def servir(porta: int = 50051):
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inferencia_pb2_grpc.add_InferenciaServicer_to_server(ServicoInferencia(), servidor)
    servidor.add_insecure_port(f"[::]:{porta}")
    servidor.start()
    logger.info("gRPC escutando na porta %d", porta)
    servidor.wait_for_termination()


if __name__ == "__main__":
    servir()
