

from __future__ import annotations

import random
import time
import functools
from datetime import datetime, timedelta
from typing import Any, Callable, List

from models import Pacote


def gerar_pacotes(quantidade: int = 10_000, seed: int | None = 42) -> List[Pacote]:
    
    if seed is not None:
        random.seed(seed)

    pacotes = []
    
    agora = datetime.now()

    for _ in range(quantidade):
        pacote = Pacote(
            peso=round(random.uniform(0.1, 30.0), 2),
            cep=f"{random.randint(1_000_000, 99_999_999):08d}",
            prioridade=random.randint(1, 5),
            data_postagem=agora - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            ),
        )
        pacotes.append(pacote)

    return pacotes


def medir_tempo(func: Callable) -> Callable:
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter_ns()
        resultado = func(*args, **kwargs)
        fim = time.perf_counter_ns()

        tempo_ns = fim - inicio
        tempo_us = tempo_ns / 1_000
        tempo_ms = tempo_ns / 1_000_000
        tempo_s = tempo_ns / 1_000_000_000

        print(
            f"    {func.__name__:.<30s} "
            f"{tempo_us:>12,.0f} μs  |  "
            f"{tempo_ms:>8,.2f} ms  |  "
            f"{tempo_s:>6,.4f} s"
        )

        
        wrapper.ultimo_tempo_ns = tempo_ns
        wrapper.ultimo_tempo_us = tempo_us
        wrapper.ultimo_tempo_ms = tempo_ms

        return resultado

    wrapper.ultimo_tempo_ns = 0
    wrapper.ultimo_tempo_us = 0.0
    wrapper.ultimo_tempo_ms = 0.0
    return wrapper


def executar_benchmark(
    algoritmo: Callable,
    dados: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
    label: str = "",
) -> tuple[List[Any], float]:
    
    nome = label or algoritmo.__name__

    inicio = time.perf_counter_ns()
    resultado = algoritmo(dados, key=key, reverse=reverse)
    fim = time.perf_counter_ns()

    tempo_us = (fim - inicio) / 1_000
    tempo_ms = (fim - inicio) / 1_000_000

    print(f"    {nome:.<40s} {tempo_us:>12,.0f} μs  ({tempo_ms:,.2f} ms)")

    return resultado, tempo_us


def exibir_pacotes(pacotes: List[Pacote], titulo: str = "", limite: int = 10) -> None:
    
    if titulo:
        print(f"\n{'─' * 70}")
        print(f"  {titulo}")
        print(f"{'─' * 70}")

    for i, p in enumerate(pacotes[:limite]):
        print(f"  [{i+1:>3}] {p}")

    if len(pacotes) > limite:
        print(f"  ... e mais {len(pacotes) - limite} pacotes")
    print()


def verificar_ordenacao(
    pacotes: List[Any],
    key: Callable[[Any], Any],
    reverse: bool = False,
) -> bool:
    
    for i in range(len(pacotes) - 1):
        a, b = key(pacotes[i]), key(pacotes[i + 1])
        if (not reverse and a > b) or (reverse and a < b):
            return False
    return True
