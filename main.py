

from __future__ import annotations

import argparse
import sys


if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")  
    sys.stderr.reconfigure(encoding="utf-8")  

from models import Pacote
from utils import (
    gerar_pacotes,
    executar_benchmark,
    exibir_pacotes,
    verificar_ordenacao,
)
from sorting import merge_sort, quick_sort, radix_sort


from sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    heap_sort,
    shell_sort,
    bucket_sort,
    counting_sort,
)


def cenario_a_urgencia(pacotes: list[Pacote]) -> list[Pacote]:
    
    print("=" * 70)
    print("   CENÁRIO A — URGÊNCIA (Prioridade + Data)")
    print("=" * 70)

    
    print("\n  Passo 1: Ordenando por data_postagem (crescente)...")
    resultado, t1 = executar_benchmark(
        merge_sort, pacotes,
        key=lambda p: p.data_postagem.timestamp(),
        label="Merge Sort (por data)",
    )

    
    print("  Passo 2: Ordenando por prioridade (decrescente)...")
    resultado, t2 = executar_benchmark(
        merge_sort, resultado,
        key=lambda p: p.prioridade,
        reverse=True,
        label="Merge Sort (por prioridade)",
    )

    print(f"\n  Tempo total: {(t1 + t2):,.0f} μs")

    
    exibir_pacotes(resultado, titulo=" Pacotes ordenados por urgência")

    
    ok = verificar_ordenacao(resultado, key=lambda p: p.prioridade, reverse=True)
    print(f"   Ordenação por prioridade correta: {ok}")

    return resultado


def cenario_b_distribuicao(pacotes: list[Pacote]) -> list[Pacote]:
    
    print("=" * 70)
    print("  ️  CENÁRIO B — DISTRIBUIÇÃO GEOGRÁFICA (CEP)")
    print("=" * 70)

    resultado, tempo = executar_benchmark(
        radix_sort, pacotes,
        key=lambda p: p.cep,
        label="Radix Sort (por CEP)",
    )

    exibir_pacotes(resultado, titulo=" Pacotes ordenados por CEP")

    ok = verificar_ordenacao(resultado, key=lambda p: int(p.cep))
    print(f"   Ordenação por CEP correta: {ok}")

    return resultado


def cenario_c_carga(pacotes: list[Pacote]) -> list[Pacote]:
    
    print("=" * 70)
    print("   CENÁRIO C — EFICIÊNCIA DE CARGA (Peso)")
    print("=" * 70)

    resultado, tempo = executar_benchmark(
        quick_sort, pacotes,
        key=lambda p: p.peso,
        label="Quick Sort (por peso)",
    )

    exibir_pacotes(resultado, titulo=" Pacotes ordenados por peso (leve → pesado)")

    ok = verificar_ordenacao(resultado, key=lambda p: p.peso)
    print(f"   Ordenação por peso correta: {ok}")

    return resultado


def benchmark_comparativo(pacotes: list[Pacote], criterio: str = "peso") -> None:
    
    criterios = {
        "peso":       lambda p: p.peso,
        "prioridade": lambda p: p.prioridade,
        "data":       lambda p: p.data_postagem.timestamp(),
        "cep":        lambda p: p.cep,
    }

    if criterio not in criterios:
        print(f"   Critério inválido: {criterio}")
        return

    key = criterios[criterio]

    print("=" * 70)
    print(f"   BENCHMARK COMPARATIVO — Critério: {criterio.upper()}")
    print(f"   Quantidade de pacotes: {len(pacotes):,}")
    print("=" * 70)

    
    algoritmos_comparativos = [
        ("Bubble Sort",    bubble_sort),
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort",     merge_sort),
        ("Quick Sort",     quick_sort),
        ("Heap Sort",      heap_sort),
        ("Shell Sort",     shell_sort),
    ]

    
    algoritmos_lineares = [
        ("Bucket Sort",   bucket_sort),
        ("Counting Sort", counting_sort),
        ("Radix Sort",    radix_sort),
    ]

    print("\n  ── Algoritmos Comparativos ──")
    for nome, algo in algoritmos_comparativos:
        
        if len(pacotes) > 5_000 and algo in (bubble_sort, selection_sort, insertion_sort):
            print(f"    {nome:.<40s} PULADO (n > 5000, O(n²))")
            continue
        executar_benchmark(algo, pacotes, key=key, label=nome)

    
    if criterio in ("prioridade", "cep"):
        print("\n  ── Algoritmos Lineares ──")
        for nome, algo in algoritmos_lineares:
            if criterio == "cep" and algo == counting_sort:
                print(f"    {nome:.<40s} PULADO (range do CEP muito grande)")
                continue
            int_key = lambda p: int(key(p)) if isinstance(key(p), str) else key(p)
            executar_benchmark(algo, pacotes, key=int_key, label=nome)

    print()


def main() -> None:
    
    parser = argparse.ArgumentParser(
        description="Simulador de Logística para E-commerce — EDA2 2026.1",
    )
    parser.add_argument(
        "-n", "--quantidade",
        type=int, default=10_000,
        help="Quantidade de pacotes a gerar (padrão: 10.000)",
    )
    parser.add_argument(
        "-c", "--cenario",
        choices=["A", "B", "C", "todos", "benchmark"],
        default="todos",
        help="Cenário a executar: A, B, C, todos ou benchmark",
    )
    parser.add_argument(
        "-s", "--seed",
        type=int, default=42,
        help="Semente para reprodutibilidade (padrão: 42)",
    )

    args = parser.parse_args()

    
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║     SIMULADOR DE LOGÍSTICA PARA E-COMMERCE                 ║")
    print("║     Estruturas de Dados e Algoritmos II — 2026.1           ║")
    print("║     G20 — Projeto de Ordenação                             ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║     Pacotes: {args.quantidade:<10,}  |  Seed: {args.seed:<18}  ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    
    print(f"\n   Gerando {args.quantidade:,} pacotes aleatórios...")
    pacotes = gerar_pacotes(args.quantidade, seed=args.seed)
    print(f"   Pacotes gerados com sucesso!\n")

    
    cenario = args.cenario.upper()

    if cenario in ("A", "TODOS"):
        cenario_a_urgencia(pacotes)
    if cenario in ("B", "TODOS"):
        cenario_b_distribuicao(pacotes)
    if cenario in ("C", "TODOS"):
        cenario_c_carga(pacotes)
    if cenario == "BENCHMARK":
        benchmark_comparativo(pacotes, criterio="peso")
        benchmark_comparativo(pacotes, criterio="prioridade")

    print("   Simulação concluída!\n")


if __name__ == "__main__":
    main()
