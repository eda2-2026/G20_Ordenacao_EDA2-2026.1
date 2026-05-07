"""
main.py — Ponto de entrada do Simulador de Logística para E-commerce.

Responsável: [Membro 1 e Membro 2 — integração conjunta]

Este módulo orquestra os três cenários de logística:

    ┌─────────────────────────────────────────────────────────────────┐
    │  Cenário A — URGÊNCIA                                          │
    │  Ordenar pacotes por prioridade + data usando Merge Sort       │
    │  (estável → preserva sub-ordem por data dentro de cada prio.)  │
    ├─────────────────────────────────────────────────────────────────┤
    │  Cenário B — DISTRIBUIÇÃO GEOGRÁFICA                           │
    │  Ordenar pacotes por CEP usando Radix Sort                     │
    │  (linear O(d·n) → eficiente para strings de dígitos fixos)     │
    ├─────────────────────────────────────────────────────────────────┤
    │  Cenário C — EFICIÊNCIA DE CARGA                               │
    │  Ordenar pacotes por peso usando Quick Sort                    │
    │  (O(n log n) médio, in-place, ótima localidade de cache)       │
    └─────────────────────────────────────────────────────────────────┘

Execução:
    python main.py
    python main.py --quantidade 50000
    python main.py --cenario A
"""

from __future__ import annotations

import argparse
import sys

# Garante saída UTF-8 no Windows (evita UnicodeEncodeError com emojis/box-drawing)
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]

from models import Pacote
from utils import (
    gerar_pacotes,
    executar_benchmark,
    exibir_pacotes,
    verificar_ordenacao,
)
from sorting import merge_sort, quick_sort, radix_sort

# Importações adicionais para benchmark comparativo (opcional)
from sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    heap_sort,
    shell_sort,
    bucket_sort,
    counting_sort,
)


# ======================================================================
# CENÁRIO A — URGÊNCIA
# ======================================================================
def cenario_a_urgencia(pacotes: list[Pacote]) -> list[Pacote]:
    """Ordena pacotes por prioridade (decrescente) e data (crescente).

    Estratégia: Multi-key sort usando a ESTABILIDADE do Merge Sort.

    ╔═══════════════════════════════════════════════════════════════╗
    ║  POR QUE MERGE SORT?                                         ║
    ║                                                               ║
    ║  1. É ESTÁVEL: ao ordenar por prioridade depois de data,     ║
    ║     pacotes de mesma prioridade mantêm a ordem por data.     ║
    ║                                                               ║
    ║  2. É O(n log n) GARANTIDO: sem pior caso O(n²) como o      ║
    ║     Quick Sort. Para logística de urgência, previsibilidade  ║
    ║     de tempo de processamento é crítica.                     ║
    ║                                                               ║
    ║  ALTERNATIVA INSTÁVEL (Quick Sort):                          ║
    ║  Se usássemos Quick Sort para a segunda ordenação, pacotes   ║
    ║  com mesma prioridade poderiam ter a ordem por data PERDIDA. ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print("=" * 70)
    print("  🚨 CENÁRIO A — URGÊNCIA (Prioridade + Data)")
    print("=" * 70)

    # Passo 1: Ordenar por data de postagem (mais antigo primeiro)
    # A estabilidade preservará esta ordem no passo seguinte.
    print("\n  Passo 1: Ordenando por data_postagem (crescente)...")
    resultado, t1 = executar_benchmark(
        merge_sort, pacotes,
        key=lambda p: p.data_postagem.timestamp(),
        label="Merge Sort (por data)",
    )

    # Passo 2: Ordenar por prioridade (maior prioridade primeiro)
    # Como Merge Sort é ESTÁVEL, pacotes com mesma prioridade
    # permanecem ordenados por data do passo anterior.
    print("  Passo 2: Ordenando por prioridade (decrescente)...")
    resultado, t2 = executar_benchmark(
        merge_sort, resultado,
        key=lambda p: p.prioridade,
        reverse=True,
        label="Merge Sort (por prioridade)",
    )

    print(f"\n  Tempo total: {(t1 + t2):,.0f} μs")

    # Exibir amostra do resultado
    exibir_pacotes(resultado, titulo="📦 Pacotes ordenados por urgência")

    # Verificar que a prioridade está decrescente
    ok = verificar_ordenacao(resultado, key=lambda p: p.prioridade, reverse=True)
    print(f"  ✅ Ordenação por prioridade correta: {ok}")

    return resultado


# ======================================================================
# CENÁRIO B — DISTRIBUIÇÃO GEOGRÁFICA
# ======================================================================
def cenario_b_distribuicao(pacotes: list[Pacote]) -> list[Pacote]:
    """Ordena pacotes por CEP para rotas de entrega regionais.

    ╔═══════════════════════════════════════════════════════════════╗
    ║  POR QUE RADIX SORT?                                         ║
    ║                                                               ║
    ║  1. CEPs são strings de 8 dígitos — perfeitos para Radix.    ║
    ║  2. Complexidade O(d·n) com d=8 e base=10 → praticamente    ║
    ║     linear: 8 passadas de Counting Sort.                     ║
    ║  3. É ESTÁVEL: CEPs iguais preservam a ordem original.       ║
    ║                                                               ║
    ║  COMPARAÇÃO COM OUTROS ALGORITMOS:                           ║
    ║  - Merge/Quick Sort: O(n log n) comparações de strings de    ║
    ║    8 chars → cada comparação custa O(8), total O(8n log n).  ║
    ║  - Radix Sort: O(8n) → MAIS RÁPIDO para n grande.           ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print("=" * 70)
    print("  🗺️  CENÁRIO B — DISTRIBUIÇÃO GEOGRÁFICA (CEP)")
    print("=" * 70)

    resultado, tempo = executar_benchmark(
        radix_sort, pacotes,
        key=lambda p: p.cep,
        label="Radix Sort (por CEP)",
    )

    exibir_pacotes(resultado, titulo="📦 Pacotes ordenados por CEP")

    ok = verificar_ordenacao(resultado, key=lambda p: int(p.cep))
    print(f"  ✅ Ordenação por CEP correta: {ok}")

    return resultado


# ======================================================================
# CENÁRIO C — EFICIÊNCIA DE CARGA
# ======================================================================
def cenario_c_carga(pacotes: list[Pacote]) -> list[Pacote]:
    """Ordena pacotes por peso para otimização de carga em caminhões.

    ╔═══════════════════════════════════════════════════════════════╗
    ║  POR QUE QUICK SORT?                                         ║
    ║                                                               ║
    ║  1. O(n log n) no caso médio com excelente constante.        ║
    ║  2. In-place: O(log n) de espaço extra (apenas recursão).    ║
    ║  3. Ótima localidade de cache (acessa memória sequencial).   ║
    ║  4. Na prática, é o mais rápido para dados aleatórios.       ║
    ║                                                               ║
    ║  ⚠ INSTABILIDADE: Quick Sort é INSTÁVEL. Pacotes de mesmo   ║
    ║  peso podem trocar de posição. Neste cenário, isso é         ║
    ║  aceitável porque só queremos a ordenação por peso.           ║
    ║                                                               ║
    ║  MITIGAÇÃO DO PIOR CASO O(n²):                               ║
    ║  Implementação usa "mediana de três" para escolha do pivô,   ║
    ║  evitando degradação com listas já ordenadas.                ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print("=" * 70)
    print("  🚛 CENÁRIO C — EFICIÊNCIA DE CARGA (Peso)")
    print("=" * 70)

    resultado, tempo = executar_benchmark(
        quick_sort, pacotes,
        key=lambda p: p.peso,
        label="Quick Sort (por peso)",
    )

    exibir_pacotes(resultado, titulo="📦 Pacotes ordenados por peso (leve → pesado)")

    ok = verificar_ordenacao(resultado, key=lambda p: p.peso)
    print(f"  ✅ Ordenação por peso correta: {ok}")

    return resultado


# ======================================================================
# BENCHMARK COMPARATIVO (TODOS OS ALGORITMOS)
# ======================================================================
def benchmark_comparativo(pacotes: list[Pacote], criterio: str = "peso") -> None:
    """Compara todos os algoritmos usando o mesmo conjunto de dados.

    Útil para gerar tabelas comparativas para o relatório do projeto.

    Args:
        criterio: "peso", "prioridade", "data" ou "cep".
    """
    criterios = {
        "peso":       lambda p: p.peso,
        "prioridade": lambda p: p.prioridade,
        "data":       lambda p: p.data_postagem.timestamp(),
        "cep":        lambda p: p.cep,
    }

    if criterio not in criterios:
        print(f"  ❌ Critério inválido: {criterio}")
        return

    key = criterios[criterio]

    print("=" * 70)
    print(f"  📊 BENCHMARK COMPARATIVO — Critério: {criterio.upper()}")
    print(f"  📦 Quantidade de pacotes: {len(pacotes):,}")
    print("=" * 70)

    # Lista de algoritmos baseados em comparação
    algoritmos_comparativos = [
        ("Bubble Sort",    bubble_sort),
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort",     merge_sort),
        ("Quick Sort",     quick_sort),
        ("Heap Sort",      heap_sort),
        ("Shell Sort",     shell_sort),
    ]

    # Algoritmos lineares (requerem chaves inteiras)
    algoritmos_lineares = [
        ("Bucket Sort",   bucket_sort),
        ("Counting Sort", counting_sort),
        ("Radix Sort",    radix_sort),
    ]

    print("\n  ── Algoritmos Comparativos ──")
    for nome, algo in algoritmos_comparativos:
        # Para amostras grandes, pular O(n²) para evitar lentidão
        if len(pacotes) > 5_000 and algo in (bubble_sort, selection_sort, insertion_sort):
            print(f"  ⏭  {nome:.<40s} PULADO (n > 5000, O(n²))")
            continue
        executar_benchmark(algo, pacotes, key=key, label=nome)

    # Algoritmos lineares só funcionam com chaves inteiras
    if criterio in ("prioridade", "cep"):
        print("\n  ── Algoritmos Lineares ──")
        for nome, algo in algoritmos_lineares:
            if criterio == "cep" and algo == counting_sort:
                print(f"  ⏭  {nome:.<40s} PULADO (range do CEP muito grande)")
                continue
            int_key = lambda p: int(key(p)) if isinstance(key(p), str) else key(p)
            executar_benchmark(algo, pacotes, key=int_key, label=nome)

    print()


# ======================================================================
# PONTO DE ENTRADA
# ======================================================================
def main() -> None:
    """Função principal — executa os cenários de logística."""
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

    # Banner do projeto
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║     SIMULADOR DE LOGÍSTICA PARA E-COMMERCE                 ║")
    print("║     Estruturas de Dados e Algoritmos II — 2026.1           ║")
    print("║     G20 — Projeto de Ordenação                             ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║     Pacotes: {args.quantidade:<10,}  |  Seed: {args.seed:<18}  ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # Geração de dados
    print(f"\n  🔧 Gerando {args.quantidade:,} pacotes aleatórios...")
    pacotes = gerar_pacotes(args.quantidade, seed=args.seed)
    print(f"  ✅ Pacotes gerados com sucesso!\n")

    # Execução dos cenários
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

    print("  🏁 Simulação concluída!\n")


if __name__ == "__main__":
    main()
