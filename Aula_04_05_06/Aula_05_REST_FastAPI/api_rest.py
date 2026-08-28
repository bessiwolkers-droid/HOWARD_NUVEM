"""Interface REST do serviço de inferência."""
import logging
import time

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from app import fila
from app.modelo import carregar_modelo

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("api_rest")

app = FastAPI(title="Serviço de Inferência - C1.A2", version="1.0.0")
modelo = None


class Entrada(BaseModel):
    texto: str


@app.on_event("startup")
def subir():
    global modelo
    inicio = time.perf_counter()
    modelo = carregar_modelo()
    logger.info("modelo carregado em %.2f ms", (time.perf_counter() - inicio) * 1000)


@app.get("/saude")
def saude():
    return {"status": "ok", "modelo_carregado": modelo is not None}


@app.post("/predict-sync")
def predict_sync(entrada: Entrada):
    inicio = time.perf_counter()
    if not entrada.texto.strip():
        raise HTTPException(status_code=400, detail="texto vazio")
    resultado = modelo.prever(entrada.texto)
    resultado["tempo_ms"] = round((time.perf_counter() - inicio) * 1000, 2)
    logger.info("request=sync tamanho=%d tempo_ms=%.2f", len(entrada.texto), resultado["tempo_ms"])
    return resultado


@app.post("/predict", status_code=202)
def predict(entrada: Entrada, request: Request):
    inicio = time.perf_counter()
    if not entrada.texto.strip():
        raise HTTPException(status_code=400, detail="texto vazio")
    tarefa_id = fila.enfileirar(entrada.texto)
    tempo_ms = (time.perf_counter() - inicio) * 1000
    logger.info("request=%s id=%s tamanho=%d tempo_ms=%.2f", request.method, tarefa_id, len(entrada.texto), tempo_ms)
    return {"id": tarefa_id, "status": "na_fila"}


@app.get("/resultado/{tarefa_id}")
def resultado(tarefa_id: str, request: Request):
    inicio = time.perf_counter()
    dados = fila.buscar_resultado(tarefa_id)
    tempo_ms = (time.perf_counter() - inicio) * 1000
    logger.info("request=%s id=%s tamanho=0 tempo_ms=%.2f", request.method, tarefa_id, tempo_ms)
    if dados is None:
        raise HTTPException(status_code=404, detail="tarefa não encontrada")
    return dados
