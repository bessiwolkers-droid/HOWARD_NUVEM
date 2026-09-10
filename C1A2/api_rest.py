from time import perf_counter

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import fila
from modelo import carregar_modelo

app = FastAPI(title="API de sentimento com fila", version="1.0.0")
modelo = carregar_modelo()


class Entrada(BaseModel):
    texto: str


@app.get("/saude")
def saude():
    return {"status": "ok", "modelo_carregado": modelo is not None}


@app.post("/predict-sync")
def predict_sync(entrada: Entrada):
    if not entrada.texto.strip():
        raise HTTPException(status_code=400, detail="O texto não pode ficar vazio.")

    inicio = perf_counter()
    resultado = modelo.prever(entrada.texto)
    resultado["tempo_ms"] = round((perf_counter() - inicio) * 1000, 2)
    print(f"[REST] sincrono texto={len(entrada.texto)} caracteres tempo={resultado['tempo_ms']} ms", flush=True)
    return resultado


@app.post("/predict", status_code=202)
def predict(entrada: Entrada):
    if not entrada.texto.strip():
        raise HTTPException(status_code=400, detail="O texto não pode ficar vazio.")

    inicio = perf_counter()
    tarefa_id = fila.enfileirar(entrada.texto)
    tempo_ms = round((perf_counter() - inicio) * 1000, 2)
    print(f"[REST] /predict id={tarefa_id} texto={len(entrada.texto)} caracteres tempo={tempo_ms} ms", flush=True)
    return {"id": tarefa_id, "status": "na_fila"}


@app.get("/resultado/{tarefa_id}")
def resultado(tarefa_id: str):
    inicio = perf_counter()
    dados = fila.buscar_resultado(tarefa_id)
    tempo_ms = round((perf_counter() - inicio) * 1000, 2)

    if dados is None:
        print(f"[REST] /resultado id={tarefa_id} nao encontrado tempo={tempo_ms} ms", flush=True)
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

    print(f"[REST] /resultado id={tarefa_id} status={dados.get('status')} tempo={tempo_ms} ms", flush=True)
    return dados
