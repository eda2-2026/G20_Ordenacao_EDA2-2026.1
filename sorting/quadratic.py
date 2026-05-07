"""
sorting/quadratic.py — Algoritmos de ordenação O(n²).

Contém: Bubble Sort, Selection Sort, Insertion Sort.

╔═══════════════════════════════════════════════════════════════════════╗
║  CONVENÇÃO DE INTERFACE                                              ║
║                                                                      ║
║  Todos os algoritmos neste projeto seguem a mesma assinatura:        ║
║                                                                      ║
║      def algoritmo(lista, key=None, reverse=False) -> list           ║
║                                                                      ║
║  • lista   — lista de objetos (Pacote, int, etc.)                    ║
║  • key     — função lambda que extrai o valor de comparação          ║
║              ex: key=lambda p: p.peso                                ║
║  • reverse — se True, ordena em ordem decrescente                    ║
║                                                                      ║
║  A função retorna uma NOVA lista ordenada (não modifica a original). ║
║  Isso torna as funções "puras" — sem efeitos colaterais.             ║
╚═══════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations
from typing import Any, Callable, List


# ======================================================================
# BUBBLE SORT
# ======================================================================
# Complexidade:  Melhor O(n)  |  Médio O(n²)  |  Pior O(n²)
# Espaço:        O(1) — in-place
# Estabilidade:  ✅ ESTÁVEL
#
# NOTA SOBRE ESTABILIDADE:
#   O Bubble Sort preserva a ordem relativa de elementos iguais.
#   Isso é importante para o cenário de logística: se dois pacotes
#   têm a mesma prioridade, a ordem original (ex: por data) é mantida.
#   Isso permite ordenação em múltiplas chaves (multi-key sorting)
#   quando combinado com outros algoritmos estáveis.
# ======================================================================
def bubble_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    """Ordena a lista usando Bubble Sort.

    Percorre a lista repetidamente, comparando pares adjacentes e
    trocando-os se estiverem fora de ordem. Otimizado com flag de
    'swapped' para detecção precoce de lista já ordenada.
    """
    if key is None:
        key = lambda x: x

    arr = list(lista)  # cópia para manter a função pura
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            a, b = key(arr[j]), key(arr[j + 1])
            condition = a > b if not reverse else a < b
            if condition:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # Se nenhuma troca foi feita, a lista já está ordenada
        if not swapped:
            break

    return arr


# ======================================================================
# SELECTION SORT
# ======================================================================
# Complexidade:  Melhor O(n²)  |  Médio O(n²)  |  Pior O(n²)
# Espaço:        O(1) — in-place
# Estabilidade:  ❌ INSTÁVEL
#
# NOTA SOBRE ESTABILIDADE:
#   O Selection Sort NÃO preserva a ordem relativa de elementos iguais.
#   Exemplo prático: se dois pacotes com peso 5.0kg estão na lista,
#   suas posições relativas podem ser trocadas após a ordenação.
#   Isso é problemático se antes foi feita uma ordenação por data —
#   a sub-ordem por data seria PERDIDA.
#
#   ⚠ CONSEQUÊNCIA NO PROJETO: Evitar Selection Sort quando for
#   necessário preservar uma ordenação secundária prévia.
# ======================================================================
def selection_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    """Ordena a lista usando Selection Sort.

    A cada iteração, encontra o menor (ou maior) elemento da parte
    não-ordenada e o coloca na posição correta.
    """
    if key is None:
        key = lambda x: x

    arr = list(lista)
    n = len(arr)

    for i in range(n):
        target_idx = i
        for j in range(i + 1, n):
            a, b = key(arr[j]), key(arr[target_idx])
            condition = a < b if not reverse else a > b
            if condition:
                target_idx = j
        arr[i], arr[target_idx] = arr[target_idx], arr[i]

    return arr


# ======================================================================
# INSERTION SORT
# ======================================================================
# Complexidade:  Melhor O(n)  |  Médio O(n²)  |  Pior O(n²)
# Espaço:        O(1) — in-place
# Estabilidade:  ✅ ESTÁVEL
#
# NOTA SOBRE ESTABILIDADE:
#   O Insertion Sort é estável porque só move elementos para trás
#   quando encontra um estritamente menor (ou maior). Elementos iguais
#   nunca ultrapassam uns aos outros.
#
#   💡 DICA DE USO: Muito eficiente para listas quase ordenadas
#   (best-case O(n)). Pode ser usado como algoritmo de finalização
#   dentro de algoritmos híbridos como TimSort ou IntroSort.
# ======================================================================
def insertion_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    """Ordena a lista usando Insertion Sort.

    Constrói a lista ordenada um elemento por vez, inserindo cada
    novo elemento na posição correta dentro da parte já ordenada.
    """
    if key is None:
        key = lambda x: x

    arr = list(lista)
    n = len(arr)

    for i in range(1, n):
        current = arr[i]
        current_key = key(current)
        j = i - 1

        while j >= 0:
            condition = key(arr[j]) > current_key if not reverse else key(arr[j]) < current_key
            if not condition:
                break
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = current

    return arr
