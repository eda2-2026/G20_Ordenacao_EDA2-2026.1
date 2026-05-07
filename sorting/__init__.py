"""
sorting/__init__.py — Ponto de entrada do pacote de algoritmos.

Exporta todos os algoritmos de ordenação de forma centralizada para
facilitar o uso em `main.py`:

    from sorting import merge_sort, quick_sort, radix_sort
"""

# O(n²) — Algoritmos quadráticos
from sorting.quadratic import bubble_sort, selection_sort, insertion_sort

# O(n log n) — Algoritmos eficientes baseados em comparação
from sorting.linearithmic import merge_sort, quick_sort, heap_sort, shell_sort

# O(n) — Algoritmos lineares (não-comparativos)
from sorting.linear import bucket_sort, counting_sort, radix_sort

__all__ = [
    # Quadráticos
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    # Linearítmicos
    "merge_sort",
    "quick_sort",
    "heap_sort",
    "shell_sort",
    # Lineares
    "bucket_sort",
    "counting_sort",
    "radix_sort",
]
