

from __future__ import annotations
from typing import Any, Callable, List


def bucket_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
    num_buckets: int = 10,
) -> List[Any]:
    
    if key is None:
        key = lambda x: x

    if len(lista) <= 1:
        return list(lista)

    arr = list(lista)

    
    min_val = min(key(item) for item in arr)
    max_val = max(key(item) for item in arr)

    if min_val == max_val:
        return arr  

    
    buckets: List[List[Any]] = [[] for _ in range(num_buckets)]

    
    range_val = max_val - min_val
    for item in arr:
        
        idx = int((key(item) - min_val) / range_val * (num_buckets - 1))
        buckets[idx].append(item)

    
    result = []
    for bucket in buckets:
        
        for i in range(1, len(bucket)):
            current = bucket[i]
            current_key = key(current)
            j = i - 1
            while j >= 0 and key(bucket[j]) > current_key:
                bucket[j + 1] = bucket[j]
                j -= 1
            bucket[j + 1] = current
        result.extend(bucket)

    if reverse:
        result.reverse()

    return result


def counting_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    
    if key is None:
        key = lambda x: x

    if len(lista) <= 1:
        return list(lista)

    arr = list(lista)
    n = len(arr)

    
    max_val = max(key(item) for item in arr)

    
    count = [0] * (max_val + 1)
    for item in arr:
        count[key(item)] += 1

    
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    
    output = [None] * n
    for i in range(n - 1, -1, -1):
        val = key(arr[i])
        count[val] -= 1
        output[count[val]] = arr[i]

    if reverse:
        output.reverse()

    return output


def radix_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    
    if key is None:
        key = lambda x: x

    if len(lista) <= 1:
        return list(lista)

    arr = list(lista)

    
    def int_key(item: Any) -> int:
        val = key(item)
        return int(val) if isinstance(val, str) else val

    
    max_val = max(int_key(item) for item in arr)

    
    exp = 1  
    while max_val // exp > 0:
        arr = _counting_sort_by_digit(arr, int_key, exp)
        exp *= 10

    if reverse:
        arr.reverse()

    return arr


def _counting_sort_by_digit(
    arr: List[Any],
    int_key: Callable[[Any], int],
    exp: int,
) -> List[Any]:
    
    n = len(arr)
    output = [None] * n
    count = [0] * 10  

    
    for item in arr:
        digit = (int_key(item) // exp) % 10
        count[digit] += 1

    
    for i in range(1, 10):
        count[i] += count[i - 1]

    
    for i in range(n - 1, -1, -1):
        digit = (int_key(arr[i]) // exp) % 10
        count[digit] -= 1
        output[count[digit]] = arr[i]

    return output
