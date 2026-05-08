

from __future__ import annotations
from typing import Any, Callable, List


def merge_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    
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
    
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        lk, rk = key(left[i]), key(right[j])
        
        
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


def quick_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    
    if key is None:
        key = lambda x: x

    arr = list(lista)
    _quick_sort_helper(arr, 0, len(arr) - 1, key, reverse)
    return arr


def _quick_sort_helper(
    arr: List[Any], low: int, high: int,
    key: Callable[[Any], Any], reverse: bool,
) -> None:
    
    if low < high:
        pivot_idx = _partition(arr, low, high, key, reverse)
        _quick_sort_helper(arr, low, pivot_idx - 1, key, reverse)
        _quick_sort_helper(arr, pivot_idx + 1, high, key, reverse)


def _median_of_three(
    arr: List[Any], low: int, high: int,
    key: Callable[[Any], Any],
) -> int:
    
    mid = (low + high) // 2
    trio = [(key(arr[low]), low), (key(arr[mid]), mid), (key(arr[high]), high)]
    trio.sort(key=lambda x: x[0])
    return trio[1][1]  


def _partition(
    arr: List[Any], low: int, high: int,
    key: Callable[[Any], Any], reverse: bool,
) -> int:
    
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


def heap_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    
    if key is None:
        key = lambda x: x

    arr = list(lista)
    n = len(arr)

    
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i, key, reverse)

    
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0, key, reverse)

    return arr


def _heapify(
    arr: List[Any], n: int, i: int,
    key: Callable[[Any], Any], reverse: bool,
) -> None:
    
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


def shell_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    
    if key is None:
        key = lambda x: x

    arr = list(lista)
    n = len(arr)

    
    gap = 1
    while gap < n // 3:
        gap = gap * 3 + 1

    while gap >= 1:
        
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
