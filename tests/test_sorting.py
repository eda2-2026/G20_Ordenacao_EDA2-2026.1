"""
Testes para os algoritmos de ordenação.
Valida o comportamento geral e a estabilidade de cada um.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from datetime import datetime, timedelta

from models import Pacote
from sorting import (
    bubble_sort, selection_sort, insertion_sort,
    merge_sort, quick_sort, heap_sort, shell_sort,
    bucket_sort, counting_sort, radix_sort
)

ALGORITMOS_COMPARATIVOS = [
    bubble_sort, selection_sort, insertion_sort,
    merge_sort, quick_sort, heap_sort, shell_sort, bucket_sort
]

ALGORITMOS_LINEARES = [
    counting_sort, radix_sort
]

TODOS_ALGORITMOS = ALGORITMOS_COMPARATIVOS + ALGORITMOS_LINEARES

@pytest.fixture
def pacotes_teste():
    agora = datetime(2026, 5, 10, 12, 0)
    return [
        Pacote(peso=10.5, cep="11111111", prioridade=3, data_postagem=agora - timedelta(days=2)),
        Pacote(peso=2.1,  cep="22222222", prioridade=5, data_postagem=agora - timedelta(days=1)),
        Pacote(peso=20.0, cep="33333333", prioridade=1, data_postagem=agora),
        Pacote(peso=5.5,  cep="44444444", prioridade=3, data_postagem=agora - timedelta(days=3)),
    ]

@pytest.mark.parametrize("algoritmo", TODOS_ALGORITMOS)
def test_ordena_lista_vazia(algoritmo):
    assert algoritmo([]) == []

@pytest.mark.parametrize("algoritmo", TODOS_ALGORITMOS)
def test_ordena_um_elemento(algoritmo, pacotes_teste):
    lista_unica = [pacotes_teste[0]]
    resultado = algoritmo(lista_unica, key=lambda p: p.prioridade)
    assert len(resultado) == 1
    assert resultado[0] == pacotes_teste[0]

@pytest.mark.parametrize("algoritmo", ALGORITMOS_COMPARATIVOS)
def test_ordenacao_peso(algoritmo, pacotes_teste):
    """Testa ordenação pelo peso (crescente)."""
    resultado = algoritmo(pacotes_teste, key=lambda p: p.peso)
    pesos = [p.peso for p in resultado]
    assert pesos == [2.1, 5.5, 10.5, 20.0]

@pytest.mark.parametrize("algoritmo", TODOS_ALGORITMOS)
def test_ordenacao_prioridade_decrescente(algoritmo, pacotes_teste):
    """Testa ordenação decrescente usando o atributo prioridade."""
    resultado = algoritmo(pacotes_teste, key=lambda p: p.prioridade, reverse=True)
    prioridades = [p.prioridade for p in resultado]
    assert prioridades == [5, 3, 3, 1]

# --- TESTE DE ESTABILIDADE ---

def get_lista_estabilidade():
    """
    Retorna uma lista de tuplas (valor, id) para testar estabilidade.
    Existem elementos com o mesmo 'valor', mas 'id' diferentes.
    """
    return [
        (5, 'A'),
        (2, 'B'),
        (5, 'C'),
        (1, 'D'),
        (2, 'E')
    ]

@pytest.mark.parametrize("algoritmo", [
    bubble_sort, insertion_sort, merge_sort, 
    bucket_sort, counting_sort, radix_sort
])
def test_algoritmos_estaveis(algoritmo):
    """Garante que os algoritmos esperados SÃO estáveis."""
    lista = get_lista_estabilidade()
    # Ordenar extraindo apenas o primeiro valor da tupla
    resultado = algoritmo(lista, key=lambda x: x[0])
    
    # A ordem esperada para estabilidade:
    # 1: (1, 'D')
    # 2: (2, 'B'), (2, 'E') -> 'B' deve vir antes de 'E'
    # 5: (5, 'A'), (5, 'C') -> 'A' deve vir antes de 'C'
    ids_resultado = [(x[0], x[1]) for x in resultado]
    assert ids_resultado == [
        (1, 'D'),
        (2, 'B'),
        (2, 'E'),
        (5, 'A'),
        (5, 'C')
    ]

@pytest.mark.parametrize("algoritmo", [
    selection_sort, quick_sort, heap_sort, shell_sort
])
def test_algoritmos_instaveis(algoritmo):
    """
    Algoritmos instáveis PODEM alterar a ordem relativa.
    Este teste é apenas para documentar esse comportamento.
    O pytest verifica se eles realmente ordenam os valores corretamente,
    ignorando a ordem dos IDs secundários.
    """
    lista = get_lista_estabilidade()
    resultado = algoritmo(lista, key=lambda x: x[0])
    
    valores_ordenados = [x[0] for x in resultado]
    assert valores_ordenados == [1, 2, 2, 5, 5]
    # Não testamos a ordem de 'B'/'E' e 'A'/'C' pois não é garantida.

if __name__ == "__main__":
    pytest.main(["-v", __file__])
