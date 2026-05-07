#  Simulador de Logística — Visão Geral do Projeto

## Estrutura de Arquivos Criada

```
G20_Ordenacao_EDA2-2026.1/
├── main.py                  # Ponto de entrada + 3 cenários + benchmark
├── models.py                # Classe Pacote (dataclass)
├── utils.py                 # Geração de dados + medição de tempo
├── sorting/                 # Pacote de algoritmos
│   ├── __init__.py          # Re-exporta todos os 10 algoritmos
│   ├── quadratic.py         # Bubble, Selection, Insertion (O(n²))
│   ├── linearithmic.py      # Merge, Quick, Heap, Shell (O(n log n))
│   └── linear.py            # Bucket, Counting, Radix (O(n))
├── README.md
└── LICENSE
```

## Cenários Implementados e Testados 

| Cenário | Algoritmo | Tempo (n=3000) | Status |
|---------|-----------|----------------|--------|
| A — Urgência (prioridade + data) | Merge Sort (2 passos, estável) | ~24ms | OK |
| B — Distribuição Geográfica (CEP) | Radix Sort (LSD, 8 dígitos) | ~6.6ms | OK |
| C — Eficiência de Carga (peso) | Quick Sort (mediana-de-três) | ~9ms | OK |

## Benchmark Comparativo (n=3000, critério: peso)

| Algoritmo | Tempo | Classe |
|-----------|-------|--------|
| Quick Sort | **~9ms** | O(n log n) |
| Shell Sort | ~12ms | O(n^1.5) |
| Merge Sort | ~12ms | O(n log n) |
| Heap Sort | ~18ms | O(n log n) |
| Insertion Sort | ~388ms | O(n²) |
| Selection Sort | ~758ms | O(n²) |
| Bubble Sort | ~1,284ms | O(n²) |

## Divisão de Trabalho Sugerida

| Membro | Arquivos | Conteúdo |
|--------|----------|----------|
| **Gustavo** | `quadratic.py`, `linear.py`, `utils.py` | 6 algoritmos + geração de dados + benchmark |
| **Pedro** | `linearithmic.py`, `models.py`, `main.py` | 4 algoritmos + modelo + cenários |

> Todos os arquivos são independentes — sem risco de conflitos de merge.

## Estabilidade dos Algoritmos — Resumo de Impacto

| Algoritmo | Estável? | Impacto na Logística |
|-----------|----------|---------------------|
| Merge Sort | SIM | **Essencial** no Cenário A — preserva sub-ordem por data ao ordenar por prioridade |
| Radix Sort | SIM | Preserva ordem original para CEPs iguais |
| Quick Sort | NÃO | Aceitável no Cenário C — ordenação single-key (só peso) |
| Selection Sort | NÃO | Evitar em multi-key sort — destrói sub-ordens prévias |
| Heap Sort | NÃO | Instável, mas garante O(n log n) no pior caso |

## Sugestões de Melhoria

1. **Testes unitários** — Criar `tests/` com pytest para validar cada algoritmo individualmente
2. **Visualização gráfica** — Usar matplotlib para gerar gráficos de desempenho (tempo × n)
3. **Exportação CSV** — Salvar resultados do benchmark para análise posterior
4. **Algoritmos híbridos** — Implementar IntroSort (Quick + Heap + Insertion) para demonstrar uso prático
5. **Análise de estabilidade visual** — Cenário demonstrando como um algoritmo instável quebra multi-key sort

## Como Executar

```bash
python main.py                    # Todos os cenários (10.000 pacotes)
python main.py -n 50000           # 50.000 pacotes
python main.py -c A               # Só cenário A
python main.py -c benchmark -n 5000  # Benchmark comparativo
```
