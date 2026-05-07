"""
sorting/linear.py — Algoritmos de ordenação em tempo linear O(n).

Contém: Bucket Sort, Counting Sort, Radix Sort.

╔═══════════════════════════════════════════════════════════════════════╗
║  DIFERENÇA FUNDAMENTAL DESTES ALGORITMOS                             ║
║                                                                      ║
║  Algoritmos lineares NÃO são baseados em comparação.                 ║
║  Eles exploram a ESTRUTURA dos dados (dígitos, faixas de valor)      ║
║  para atingir complexidade O(n), quebrando o lower bound de          ║
║  O(n log n) dos algoritmos comparativos.                             ║
║                                                                      ║
║  ⚠ TRADE-OFF: exigem restrições nos dados de entrada               ║
║  (inteiros, faixas conhecidas, dígitos fixos).                       ║
╚═══════════════════════════════════════════════════════════════════════╝

NOTA: Bucket Sort e Counting Sort aceitam o parâmetro `key` para manter
a interface uniforme. Radix Sort trabalha diretamente com representações
numéricas/string e aceita `key` para extrair o valor numérico do objeto.
"""

from __future__ import annotations
from typing import Any, Callable, List


# ======================================================================
# BUCKET SORT
# ======================================================================
# Complexidade:  Melhor O(n+k) | Médio O(n+k) | Pior O(n²)
#                (k = número de buckets; pior caso se todos vão para 1 bucket)
# Espaço:        O(n + k)
# Estabilidade:  ✅ ESTÁVEL (se o sort interno for estável)
#
# NOTA SOBRE ESTABILIDADE:
#   A estabilidade depende do algoritmo usado para ordenar cada bucket.
#   Aqui usamos Insertion Sort (estável), portanto o Bucket Sort
#   resultante também é estável.
#
# USO NA LOGÍSTICA:
#   Ideal para ordenar pesos, que são floats distribuídos uniformemente
#   em uma faixa conhecida (ex: 0.1 a 30.0 kg).
# ======================================================================
def bucket_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
    num_buckets: int = 10,
) -> List[Any]:
    """Ordena a lista usando Bucket Sort.

    Distribui os elementos em buckets (baldes) com base na faixa de
    valores, ordena cada bucket individualmente e concatena os resultados.

    Args:
        num_buckets: quantidade de baldes a utilizar. Mais baldes =
                     melhor distribuição, mas mais uso de memória.
    """
    if key is None:
        key = lambda x: x

    if len(lista) <= 1:
        return list(lista)

    arr = list(lista)

    # Determinar a faixa de valores
    min_val = min(key(item) for item in arr)
    max_val = max(key(item) for item in arr)

    if min_val == max_val:
        return arr  # todos os valores são iguais

    # Criar os buckets
    buckets: List[List[Any]] = [[] for _ in range(num_buckets)]

    # Distribuir elementos nos buckets
    range_val = max_val - min_val
    for item in arr:
        # Calcula o índice do bucket (normalizado para [0, num_buckets-1])
        idx = int((key(item) - min_val) / range_val * (num_buckets - 1))
        buckets[idx].append(item)

    # Ordenar cada bucket com Insertion Sort (mantém estabilidade)
    result = []
    for bucket in buckets:
        # Insertion Sort inline para cada bucket
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


# ======================================================================
# COUNTING SORT
# ======================================================================
# Complexidade:  O(n + k) onde k = range dos valores
# Espaço:        O(n + k)
# Estabilidade:  ✅ ESTÁVEL
#
# NOTA SOBRE ESTABILIDADE:
#   O Counting Sort é estável porque percorre o array original de
#   trás para frente (right-to-left) ao posicionar os elementos,
#   garantindo que elementos com a mesma chave mantenham sua ordem
#   relativa original.
#
# USO NA LOGÍSTICA:
#   PERFEITO para ordenar por prioridade (valores discretos 1–5).
#   Com k=5, o overhead é mínimo e a ordenação é O(n).
#
# RESTRIÇÃO:
#   Funciona apenas com chaves inteiras não-negativas.
#   Para chaves negativas, seria necessário deslocar os valores.
# ======================================================================
def counting_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    """Ordena a lista usando Counting Sort.

    Conta a frequência de cada valor-chave, calcula as posições
    cumulativas e posiciona cada elemento diretamente na posição final.

    ⚠ Requer que key() retorne inteiros não-negativos.
    """
    if key is None:
        key = lambda x: x

    if len(lista) <= 1:
        return list(lista)

    arr = list(lista)
    n = len(arr)

    # Encontrar o valor máximo para dimensionar o array de contagem
    max_val = max(key(item) for item in arr)

    # Array de contagem: count[v] = quantas vezes o valor v aparece
    count = [0] * (max_val + 1)
    for item in arr:
        count[key(item)] += 1

    # Acumular contagens: count[v] = posição final do último elemento com valor v
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Construir o array de saída (de trás para frente para ESTABILIDADE)
    output = [None] * n
    for i in range(n - 1, -1, -1):
        val = key(arr[i])
        count[val] -= 1
        output[count[val]] = arr[i]

    if reverse:
        output.reverse()

    return output


# ======================================================================
# RADIX SORT
# ======================================================================
# Complexidade:  O(d × (n + b)) onde d = nº de dígitos, b = base
# Espaço:        O(n + b)
# Estabilidade:  ✅ ESTÁVEL
#
# NOTA SOBRE ESTABILIDADE:
#   O Radix Sort é estável porque utiliza um algoritmo estável
#   (Counting Sort) como sub-rotina em cada dígito. A estabilidade
#   é ESSENCIAL aqui: ao ordenar pelo dígito mais significativo,
#   a ordem estabelecida pelos dígitos menos significativos é preservada.
#
# USO NA LOGÍSTICA:
#   IDEAL para o Cenário B (Distribuição Geográfica) — ordenar por
#   CEP de 8 dígitos. O Radix Sort trata cada dígito do CEP como
#   uma passada independente, resultando em 8 passadas com base 10.
#
# IMPLEMENTAÇÃO:
#   Usamos LSD (Least Significant Digit) Radix Sort: começa pelo
#   dígito menos significativo e avança para o mais significativo.
# ======================================================================
def radix_sort(
    lista: List[Any],
    key: Callable[[Any], Any] | None = None,
    reverse: bool = False,
) -> List[Any]:
    """Ordena a lista usando LSD Radix Sort.

    Ordena dígito a dígito, do menos significativo (LSD) para o mais
    significativo (MSD), usando Counting Sort como sub-rotina estável.

    Args:
        key: deve retornar um inteiro não-negativo ou uma string numérica.
             Para CEPs (strings), o valor é convertido internamente para int.
    """
    if key is None:
        key = lambda x: x

    if len(lista) <= 1:
        return list(lista)

    arr = list(lista)

    # Converte a chave para inteiro se for string numérica (ex: CEP)
    def int_key(item: Any) -> int:
        val = key(item)
        return int(val) if isinstance(val, str) else val

    # Encontrar o número máximo de dígitos
    max_val = max(int_key(item) for item in arr)

    # Ordenar por cada dígito usando Counting Sort estável
    exp = 1  # 1, 10, 100, 1000, ...
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
    """Counting Sort auxiliar que ordena pelo dígito na posição `exp`.

    Extrai o dígito com: (int_key(item) // exp) % 10
    Base 10 → array de contagem com 10 posições.
    """
    n = len(arr)
    output = [None] * n
    count = [0] * 10  # base 10

    # Contar ocorrências do dígito
    for item in arr:
        digit = (int_key(item) // exp) % 10
        count[digit] += 1

    # Acumular
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Construir saída (de trás para frente → estável)
    for i in range(n - 1, -1, -1):
        digit = (int_key(arr[i]) // exp) % 10
        count[digit] -= 1
        output[count[digit]] = arr[i]

    return output
