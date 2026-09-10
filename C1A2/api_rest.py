from time import perf_counter

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
