"""Operações de fila e armazenamento de resultados usando Redis."""
import json
import os
import uuid

import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
FILA_TAREFAS = "tarefas"
FILA_DESCARTE = "tarefas:dead-letter"
PREFIXO_RESULTADO = "resultado:"

_cliente = None


def cliente():
    global _cliente
    if _cliente is None:
        _cliente = redis.from_url(REDIS_URL, decode_responses=True)
    return _cliente


def enfileirar(texto: str) -> str:
    tarefa_id = str(uuid.uuid4())
    cliente().rpush(FILA_TAREFAS, json.dumps({"id": tarefa_id, "texto": texto, "tentativas": 0}))
    cliente().set(PREFIXO_RESULTADO + tarefa_id, json.dumps({"status": "na_fila"}))
    return tarefa_id


def proxima_tarefa(timeout: int = 5):
    item = cliente().blpop(FILA_TAREFAS, timeout=timeout)
    return json.loads(item[1]) if item is not None else None


def guardar_resultado(tarefa_id: str, resultado: dict) -> None:
    cliente().set(PREFIXO_RESULTADO + tarefa_id, json.dumps(resultado))


def guardar_erro(tarefa_id: str, mensagem: str) -> None:
    guardar_resultado(tarefa_id, {"status": "erro", "erro": mensagem})


def mandar_para_descarte(tarefa: dict, erro: str) -> None:
    registro = {**tarefa, "status": "dead-letter", "erro": erro}
    cliente().rpush(FILA_DESCARTE, json.dumps(registro))
    guardar_erro(tarefa["id"], erro)


def buscar_resultado(tarefa_id: str):
    bruto = cliente().get(PREFIXO_RESULTADO + tarefa_id)
    return json.loads(bruto) if bruto else None
