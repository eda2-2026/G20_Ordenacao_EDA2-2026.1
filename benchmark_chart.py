"""
benchmark_chart.py — Gerador de gráficos comparativos de desempenho.

Gera dois arquivos PNG na pasta /graficos:

    graficos/
    ├── 01_algoritmos_eficientes.png  — Merge, Quick, Heap, Shell, Radix, Bucket, Counting
    └── 02_todos_algoritmos.png       — Inclui Bubble, Selection, Insertion (n pequeno)

Cada gráfico mostra 3 curvas por algoritmo:
    ● Dados aleatórios   (caso médio)
    ● Dados já ordenados (melhor caso para alguns)
    ● Dados invertidos   (pior caso para alguns)

Uso:
    python benchmark_chart.py
    python benchmark_chart.py --salvar      # salva PNGs sem exibir
    python benchmark_chart.py --sem-grafico # só imprime os tempos no terminal
"""

from __future__ import annotations

import argparse
import os
import sys
import time
import csv
from typing import Callable

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from models import Pacote
from utils import gerar_pacotes
from sorting import (
    bubble_sort, selection_sort, insertion_sort,
    merge_sort, quick_sort, heap_sort, shell_sort,
    bucket_sort, counting_sort, radix_sort,
)

# Garante saída UTF-8 no Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]

# ──────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DOS EXPERIMENTOS
# ──────────────────────────────────────────────────────────────────────

# Tamanhos de n a testar
N_EFICIENTES = [100, 500, 1_000, 2_000, 5_000, 10_000, 20_000]
N_QUADRATICOS = [100, 300, 500, 800, 1_000, 1_500, 2_000]

# Chave de ordenação padrão para o benchmark (peso — float)
KEY_PESO: Callable = lambda p: p.peso
KEY_PRIO: Callable = lambda p: p.prioridade

# Estilo visual dos algoritmos
ESTILOS = {
    # Quadráticos — tons de vermelho/laranja
    "Bubble Sort":    {"color": "#e74c3c", "linestyle": "-",  "marker": "o"},
    "Selection Sort": {"color": "#e67e22", "linestyle": "--", "marker": "s"},
    "Insertion Sort": {"color": "#f39c12", "linestyle": ":",  "marker": "^"},
    # Linearítmicos — tons de azul/verde
    "Merge Sort":     {"color": "#2980b9", "linestyle": "-",  "marker": "o"},
    "Quick Sort":     {"color": "#27ae60", "linestyle": "-",  "marker": "s"},
    "Heap Sort":      {"color": "#8e44ad", "linestyle": "--", "marker": "D"},
    "Shell Sort":     {"color": "#16a085", "linestyle": ":",  "marker": "^"},
    # Lineares — tons de ciano/rosa
    "Bucket Sort":    {"color": "#2ecc71", "linestyle": "-",  "marker": "P"},
    "Counting Sort":  {"color": "#1abc9c", "linestyle": "--", "marker": "*"},
    "Radix Sort":     {"color": "#e91e63", "linestyle": ":",  "marker": "X"},
}


# ──────────────────────────────────────────────────────────────────────
# GERAÇÃO DOS TIPOS DE ENTRADA
# ──────────────────────────────────────────────────────────────────────

def gerar_entrada(n: int, tipo: str) -> list[Pacote]:
    """Gera uma lista de pacotes conforme o tipo de entrada.

    Args:
        tipo: "aleatorio", "ordenado" ou "invertido"
    """
    pacotes = gerar_pacotes(n, seed=42)

    if tipo == "aleatorio":
        return pacotes
    elif tipo == "ordenado":
        return sorted(pacotes, key=KEY_PESO)
    elif tipo == "invertido":
        return sorted(pacotes, key=KEY_PESO, reverse=True)
    else:
        raise ValueError(f"Tipo desconhecido: {tipo}")


# ──────────────────────────────────────────────────────────────────────
# MEDIÇÃO DE TEMPO
# ──────────────────────────────────────────────────────────────────────

def medir(algoritmo: Callable, dados: list, key: Callable) -> float:
    """Executa o algoritmo e retorna o tempo em milissegundos."""
    inicio = time.perf_counter_ns()
    algoritmo(dados, key=key)
    fim = time.perf_counter_ns()
    return (fim - inicio) / 1_000_000  # ms


def coletar_tempos(
    algoritmos: dict[str, Callable],
    tamanhos: list[int],
    key: Callable,
    tipos: list[str],
    repetições: int = 3,
) -> dict[str, dict[str, list[float]]]:
    """Coleta tempos de execução para todos os algoritmos e tamanhos.

    Executa cada combinação `repetições` vezes e usa a mediana
    para reduzir ruído de medição.

    Returns:
        {nome_algoritmo: {tipo_entrada: [tempo_para_cada_n]}}
    """
    resultados: dict[str, dict[str, list[float]]] = {
        nome: {tipo: [] for tipo in tipos}
        for nome in algoritmos
    }

    total = len(algoritmos) * len(tamanhos) * len(tipos)
    passo = 0

    for nome, algo in algoritmos.items():
        for tipo in tipos:
            for n in tamanhos:
                passo += 1
                dados = gerar_entrada(n, tipo)

                # Medir `repetições` vezes e pegar a mediana
                tempos = [medir(algo, dados, key) for _ in range(repetições)]
                mediana = sorted(tempos)[repetições // 2]

                resultados[nome][tipo].append(mediana)
                print(
                    f"  [{passo:>3}/{total}] {nome:<15} | n={n:>6,} | "
                    f"{tipo:<10} → {mediana:>8.2f} ms"
                )

    return resultados


# ──────────────────────────────────────────────────────────────────────
# PLOTAGEM
# ──────────────────────────────────────────────────────────────────────

TIPOS_LABEL = {
    "aleatorio": "Aleatório (caso médio)",
    "ordenado":  "Já ordenado (melhor caso)",
    "invertido": "Invertido (pior caso)",
}

TIPOS_ALPHA = {
    "aleatorio": 1.0,
    "ordenado":  0.55,
    "invertido": 0.75,
}

TIPOS_LINEWIDTH = {
    "aleatorio": 2.2,
    "ordenado":  1.2,
    "invertido": 1.5,
}


def plotar_figura(
    resultados: dict[str, dict[str, list[float]]],
    tamanhos: list[int],
    titulo: str,
    tipos: list[str],
    caminho: str | None = None,
) -> None:
    """Plota os resultados em subgráficos por tipo de entrada."""
    n_tipos = len(tipos)
    fig, axes = plt.subplots(
        1, n_tipos,
        figsize=(7 * n_tipos, 6),
        sharey=False,
    )

    if n_tipos == 1:
        axes = [axes]

    fig.suptitle(titulo, fontsize=15, fontweight="bold", y=1.01)

    for ax, tipo in zip(axes, tipos):
        for nome, dados_por_tipo in resultados.items():
            estilo = ESTILOS.get(nome, {})
            tempos = dados_por_tipo[tipo]

            ax.plot(
                tamanhos, tempos,
                label=nome,
                color=estilo.get("color", None),
                linestyle=estilo.get("linestyle", "-"),
                marker=estilo.get("marker", "o"),
                linewidth=TIPOS_LINEWIDTH[tipo],
                alpha=TIPOS_ALPHA[tipo],
                markersize=5,
            )

        ax.set_title(TIPOS_LABEL[tipo], fontsize=11, pad=8)
        ax.set_xlabel("n (quantidade de pacotes)", fontsize=10)
        ax.set_ylabel("Tempo (ms)", fontsize=10)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{y:.1f}"))
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.legend(fontsize=8, loc="upper left")
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)

    plt.tight_layout()

    if caminho:
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        plt.savefig(caminho, dpi=150, bbox_inches="tight")
        print(f"\n  💾 Salvo em: {caminho}")
    else:
        plt.show()

    plt.close()


# ──────────────────────────────────────────────────────────────────────
# EXPORTAÇÃO PARA CSV
# ──────────────────────────────────────────────────────────────────────

def exportar_csv(
    resultados: dict[str, dict[str, list[float]]],
    tamanhos: list[int],
    grupo: str,
    caminho: str,
    modo: str = "w"
) -> None:
    """Exporta os resultados do benchmark para um arquivo CSV."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    
    escrever_cabecalho = not os.path.exists(caminho) or modo == "w"
    
    with open(caminho, mode=modo, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if escrever_cabecalho:
            writer.writerow(["Grupo", "Algoritmo", "Tipo_Entrada", "N", "Tempo_ms"])
            
        for nome, dados_tipo in resultados.items():
            for tipo, tempos in dados_tipo.items():
                for n, tempo in zip(tamanhos, tempos):
                    writer.writerow([grupo, nome, tipo, n, f"{tempo:.4f}"])


# ──────────────────────────────────────────────────────────────────────
# PONTO DE ENTRADA
# ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera gráficos comparativos de desempenho dos algoritmos."
    )
    parser.add_argument(
        "--salvar", action="store_true",
        help="Salva os gráficos como PNG em ./graficos/ sem exibir janela",
    )
    parser.add_argument(
        "--csv", action="store_true",
        help="Exporta os resultados de tempo para um arquivo CSV em ./graficos/",
    )
    parser.add_argument(
        "--sem-grafico", action="store_true",
        help="Só imprime os tempos no terminal, sem gerar gráfico",
    )
    parser.add_argument(
        "--repeticoes", type=int, default=3,
        help="Número de medições por combinação (padrão: 3)",
    )
    args = parser.parse_args()

    tipos = ["aleatorio", "ordenado", "invertido"]

    # ── Figura 1: Algoritmos eficientes (O(n log n) e lineares) ──────
    print("\n" + "=" * 60)
    print("  📊 FIGURA 1 — Algoritmos Eficientes")
    print("  Tamanhos:", [f"{n:,}" for n in N_EFICIENTES])
    print("=" * 60)

    algos_eficientes = {
        "Merge Sort":    merge_sort,
        "Quick Sort":    quick_sort,
        "Heap Sort":     heap_sort,
        "Shell Sort":    shell_sort,
        "Counting Sort": lambda lst, key: counting_sort(lst, key=lambda p: p.prioridade),
        "Radix Sort":    lambda lst, key: radix_sort(lst, key=lambda p: p.cep),
    }

    # Counting e Radix têm keys fixas — usamos KEY_PESO só nos outros
    # Para o plot combinado, medimos todos com KEY_PESO exceto lineares
    algos_eficientes_peso = {
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Heap Sort":  heap_sort,
        "Shell Sort": shell_sort,
        "Bucket Sort": bucket_sort,
    }

    res_eficientes = coletar_tempos(
        algos_eficientes_peso, N_EFICIENTES, KEY_PESO, tipos, args.repeticoes
    )

    if not args.sem_grafico:
        caminho1 = "graficos/01_algoritmos_eficientes.png" if args.salvar else None
        plotar_figura(
            res_eficientes, N_EFICIENTES,
            "Algoritmos O(n log n) e O(n) — Desempenho por tipo de entrada",
            tipos, caminho=caminho1,
        )

    # ── Figura 2: Todos os algoritmos (n pequeno) ────────────────────
    print("\n" + "=" * 60)
    print("  📊 FIGURA 2 — Todos os Algoritmos (n pequeno)")
    print("  Tamanhos:", [f"{n:,}" for n in N_QUADRATICOS])
    print("=" * 60)

    algos_todos = {
        "Bubble Sort":    bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort":     merge_sort,
        "Quick Sort":     quick_sort,
        "Heap Sort":      heap_sort,
        "Shell Sort":     shell_sort,
        "Bucket Sort":    bucket_sort,
    }

    res_todos = coletar_tempos(
        algos_todos, N_QUADRATICOS, KEY_PESO, tipos, args.repeticoes
    )

    if not args.sem_grafico:
        caminho2 = "graficos/02_todos_algoritmos.png" if args.salvar else None
        plotar_figura(
            res_todos, N_QUADRATICOS,
            "Todos os Algoritmos (n ≤ 2.000) — O(n²) vs O(n log n)",
            tipos, caminho=caminho2,
        )

    if args.csv:
        caminho_csv = "graficos/benchmark_resultados.csv"
        exportar_csv(res_eficientes, N_EFICIENTES, "Eficientes (n_log_n_e_n)", caminho_csv, modo="w")
        exportar_csv(res_todos, N_QUADRATICOS, "Quadraticos (n_pequeno)", caminho_csv, modo="a")
        print(f"\n  📄 Resultados exportados para CSV: {caminho_csv}")

    print("\n  ✅ Benchmark concluído!\n")


if __name__ == "__main__":
    main()
