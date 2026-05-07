"""
sorting/linearithmic.py — Algoritmos de ordenação O(n log n).

Responsável: [Membro 2 — definir]

Contém: Merge Sort, Quick Sort, Heap Sort, Shell Sort.

Estes são os algoritmos mais utilizados na prática para ordenação
de propósito geral. Todos seguem a interface padrão do projeto:

    def algoritmo(lista, key=None, reverse=False) -> list
"""

from __future__ import annotations
from typing import Any, Callable, List


# ======================================================================
# MERGE SORT
# ======================================================================
# Complexidade:  Melhor O(n log n) | Médio O(n log n) | Pior O(n log n)
# Espaço:        O(n) — precisa de lista auxiliar
# Estabilidade:  ✅ ESTÁVEL
#
# NOTA SOBRE ESTABILIDADE:
#   O Merge Sort é o algoritmo IDEAL para o Cenário A (Urgência)
#   porque preserva a ordem relativa de elementos com chaves iguais.
#
#   Exemplo prático: se ordenarmos primeiro por data_postagem e depois
#   por prioridade com Merge Sort, pacotes de mesma prioridade
#   CONTINUAM ordenados por data. Isso é a base da "multi-key sort":
#
#       1° passo: merge_sort(pacotes, key=lambda p: p.data_postagem)
#       2° passo: merge_sort(resultado, key=lambda p: p.prioridade)
#
#   Resultado: pacotes ordenados por prioridade E, dentro de cada
#   nível de prioridade, por data de postagem. 🎯
#
#   Se usássemos um algoritmo INSTÁVEL (ex: Quick Sort), a sub-ordem
#   por data seria destruída no segundo passo!
# ======================================================================
def merge_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    """Ordena a lista usando Merge Sort (divisão e conquista).

    Divide a lista ao meio recursivamente até ter sublistas de tamanho
    1, depois intercala (merge) as sublistas de forma ordenada.
    """
    if key is None:
        key = lambda x: x

    arr = list(lista)

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key=key, reverse=reverse)
    right = merge_sort(arr[mid:], key=key, reverse=reverse)

    return _merge(left, right, key, reverse)


def _merge(
    left: List[Any],
    right: List[Any],
    key: Callable[[Any], Any],
    reverse: bool,
) -> List[Any]:
    """Intercala duas listas ordenadas em uma única lista ordenada.

    A estabilidade é garantida aqui: quando key(left[i]) == key(right[j]),
    o elemento da esquerda é escolhido primeiro (<=), preservando a
    ordem original.
    """
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        lk, rk = key(left[i]), key(right[j])
        # O operador <= (e não <) garante ESTABILIDADE:
        # elementos iguais da esquerda vêm antes dos da direita.
        condition = lk <= rk if not reverse else lk >= rk
        if condition:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ======================================================================
# QUICK SORT
# ======================================================================
# Complexidade:  Melhor O(n log n) | Médio O(n log n) | Pior O(n²)
# Espaço:        O(log n) — pilha de recursão
# Estabilidade:  ❌ INSTÁVEL
#
# NOTA SOBRE ESTABILIDADE:
#   O Quick Sort é INSTÁVEL na versão clássica in-place.
#   Para o Cenário C (peso), isso geralmente não é problema porque
#   estamos ordenando apenas por uma chave (peso).
#
#   ⚠ MAS: se precisar manter uma sub-ordem (ex: pacotes de mesmo
#   peso ordenados por data), seria necessário usar uma chave composta:
#       key=lambda p: (p.peso, p.data_postagem)
#   Isso transforma a multi-key sort em single-key sort, contornando
#   a instabilidade.
#
# NOTA SOBRE O PIOR CASO:
#   O pior caso O(n²) ocorre quando o pivô é sempre o menor ou maior
#   elemento (lista já ordenada + pivô fixo). A estratégia "mediana
#   de três" mitiga esse risco na prática.
# ======================================================================
def quick_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    """Ordena a lista usando Quick Sort com pivô 'mediana de três'.

    Seleciona o pivô como a mediana entre o primeiro, meio e último
    elemento, reduzindo a chance do pior caso O(n²).
    """
    if key is None:
        key = lambda x: x

    arr = list(lista)
    _quick_sort_helper(arr, 0, len(arr) - 1, key, reverse)
    return arr


def _quick_sort_helper(
    arr: List[Any], low: int, high: int,
    key: Callable[[Any], Any], reverse: bool,
) -> None:
    """Função recursiva auxiliar do Quick Sort."""
    if low < high:
        pivot_idx = _partition(arr, low, high, key, reverse)
        _quick_sort_helper(arr, low, pivot_idx - 1, key, reverse)
        _quick_sort_helper(arr, pivot_idx + 1, high, key, reverse)


def _median_of_three(
    arr: List[Any], low: int, high: int,
    key: Callable[[Any], Any],
) -> int:
    """Seleciona o índice da mediana entre arr[low], arr[mid], arr[high]."""
    mid = (low + high) // 2
    trio = [(key(arr[low]), low), (key(arr[mid]), mid), (key(arr[high]), high)]
    trio.sort(key=lambda x: x[0])
    return trio[1][1]  # índice do valor mediano


def _partition(
    arr: List[Any], low: int, high: int,
    key: Callable[[Any], Any], reverse: bool,
) -> int:
    """Particiona o array ao redor do pivô (mediana de três)."""
    pivot_idx = _median_of_three(arr, low, high, key)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    pivot_val = key(arr[high])

    i = low - 1
    for j in range(low, high):
        val = key(arr[j])
        condition = val <= pivot_val if not reverse else val >= pivot_val
        if condition:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ======================================================================
# HEAP SORT
# ======================================================================
# Complexidade:  Melhor O(n log n) | Médio O(n log n) | Pior O(n log n)
# Espaço:        O(1) — in-place
# Estabilidade:  ❌ INSTÁVEL
#
# NOTA SOBRE ESTABILIDADE:
#   O Heap Sort é instável devido à operação de heapify, que pode
#   trocar elementos iguais de posição. Na logística, isso significa
#   que pacotes com mesmo peso podem ter sua ordem de chegada alterada.
#
# VANTAGEM:
#   Tem garantia de O(n log n) no pior caso (diferente do Quick Sort),
#   e usa espaço O(1) (diferente do Merge Sort). É o melhor dos dois
#   mundos em termos de garantias, mas na prática tende a ser mais
#   lento que o Quick Sort por ter pior localidade de cache.
# ======================================================================
def heap_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    """Ordena a lista usando Heap Sort.

    Constrói um max-heap (ou min-heap) e extrai repetidamente o
    elemento raiz para construir a lista ordenada.
    """
    if key is None:
        key = lambda x: x

    arr = list(lista)
    n = len(arr)

    # Fase 1: Construir o max-heap (bottom-up)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i, key, reverse)

    # Fase 2: Extrair elementos do heap um por um
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0, key, reverse)

    return arr


def _heapify(
    arr: List[Any], n: int, i: int,
    key: Callable[[Any], Any], reverse: bool,
) -> None:
    """Mantém a propriedade de heap para a subárvore com raiz em i."""
    target = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n:
        cond = key(arr[left]) > key(arr[target]) if not reverse else key(arr[left]) < key(arr[target])
        if cond:
            target = left

    if right < n:
        cond = key(arr[right]) > key(arr[target]) if not reverse else key(arr[right]) < key(arr[target])
        if cond:
            target = right

    if target != i:
        arr[i], arr[target] = arr[target], arr[i]
        _heapify(arr, n, target, key, reverse)


# ======================================================================
# SHELL SORT
# ======================================================================
# Complexidade:  Depende da sequência de gaps. Com Knuth: O(n^(3/2))
# Espaço:        O(1) — in-place
# Estabilidade:  ❌ INSTÁVEL
#
# NOTA SOBRE ESTABILIDADE:
#   O Shell Sort é instável porque compara e troca elementos distantes
#   (separados pelo gap), podendo alterar a ordem relativa de iguais.
#
# NOTA SOBRE GAPS:
#   A escolha da sequência de gaps afeta diretamente a complexidade:
#   - Shell original (N/2, N/4, ...): O(n²) no pior caso
#   - Knuth (1, 4, 13, 40, ...): O(n^1.5) — usamos esta aqui
#   - Sedgewick, Tokuda, Ciura: complexidades melhores mas mais complexas
# ======================================================================
def shell_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    """Ordena a lista usando Shell Sort com sequência de gaps de Knuth.

    Generalização do Insertion Sort que permite trocar elementos
    distantes, reduzindo o número total de movimentações.
    """
    if key is None:
        key = lambda x: x

    arr = list(lista)
    n = len(arr)

    # Gera a sequência de Knuth: 1, 4, 13, 40, 121, ...
    gap = 1
    while gap < n // 3:
        gap = gap * 3 + 1

    while gap >= 1:
        # Insertion Sort com passo = gap
        for i in range(gap, n):
            current = arr[i]
            current_key = key(current)
            j = i

            while j >= gap:
                condition = key(arr[j - gap]) > current_key if not reverse else key(arr[j - gap]) < current_key
                if not condition:
                    break
                arr[j] = arr[j - gap]
                j -= gap

            arr[j] = current

        gap //= 3

    return arr
