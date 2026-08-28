from time import perf_counter

from modelo import carregar_modelo

modelo = carregar_modelo()


def prever(texto: str) -> dict:
    if not texto.strip():
        raise ValueError("O texto não pode ficar vazio.")

    inicio = perf_counter()
    resultado = modelo.prever(texto)
    resultado["tempo_ms"] = round((perf_counter() - inicio) * 1000, 2)
    print(f"[IA] texto={len(texto)} caracteres tempo={resultado['tempo_ms']} ms", flush=True)
    return resultado


if __name__ == "__main__":
    frase = input("Digite uma frase: ")
    print(prever(frase))
