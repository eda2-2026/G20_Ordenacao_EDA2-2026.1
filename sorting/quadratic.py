from __future__ import annotations
from typing import Any, Callable, List


def bubble_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    
    if key is None:
        key = lambda x: x

    arr = list(lista)  
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            a, b = key(arr[j]), key(arr[j + 1])
            condition = a > b if not reverse else a < b
            if condition:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        if not swapped:
            break

    return arr


def selection_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    
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


def insertion_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    
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
