# 📦 Simulador de Logística para E-commerce

**Estruturas de Dados e Algoritmos II — 2026.1 | Grupo G20**

Simulador que utiliza algoritmos de ordenação para processar pacotes em cenários reais de logística de e-commerce.

## 📁 Estrutura do Projeto

```
G20_Ordenacao_EDA2-2026.1/
├── main.py              # Ponto de entrada — cenários de logística
├── models.py            # Classe Pacote (modelagem de dados)
├── utils.py             # Geração de dados e benchmark
├── sorting/             # Pacote de algoritmos de ordenação
│   ├── __init__.py      # Re-exporta todos os algoritmos
│   ├── quadratic.py     # O(n²):     Bubble, Selection, Insertion
│   ├── linearithmic.py  # O(n log n): Merge, Quick, Heap, Shell
│   └── linear.py        # O(n):      Bucket, Counting, Radix
├── LICENSE
└── README.md
```

## 🚀 Como Executar

```bash
# Executar todos os cenários com 10.000 pacotes (padrão)
python main.py

# Especificar quantidade de pacotes
python main.py -n 50000

# Executar cenário específico
python main.py -c A          # Urgência (Merge Sort)
python main.py -c B          # Distribuição Geográfica (Radix Sort)
python main.py -c C          # Eficiência de Carga (Quick Sort)

# Benchmark comparativo de todos os algoritmos
python main.py -c benchmark -n 5000

# Definir seed para reprodutibilidade
python main.py -n 10000 -s 123
```

## 📋 Cenários de Logística

| Cenário | Objetivo | Algoritmo | Chave | Justificativa |
|---------|----------|-----------|-------|---------------|
| **A — Urgência** | Prioridade + Data | Merge Sort | `prioridade` + `data_postagem` | Estável → preserva sub-ordem por data |
| **B — Distribuição** | Agrupamento regional | Radix Sort | `cep` (8 dígitos) | O(d·n) linear para dígitos fixos |
| **C — Carga** | Otimização de peso | Quick Sort | `peso` | O(n log n) médio, in-place, cache-friendly |

## 📊 Algoritmos Implementados

| Algoritmo | Complexidade (Médio) | Espaço | Estável? | Arquivo |
|-----------|---------------------|--------|----------|---------|
| Bubble Sort | O(n²) | O(1) | ✅ Sim | `quadratic.py` |
| Selection Sort | O(n²) | O(1) | ❌ Não | `quadratic.py` |
| Insertion Sort | O(n²) | O(1) | ✅ Sim | `quadratic.py` |
| Merge Sort | O(n log n) | O(n) | ✅ Sim | `linearithmic.py` |
| Quick Sort | O(n log n) | O(log n) | ❌ Não | `linearithmic.py` |
| Heap Sort | O(n log n) | O(1) | ❌ Não | `linearithmic.py` |
| Shell Sort | O(n^1.5) | O(1) | ❌ Não | `linearithmic.py` |
| Bucket Sort | O(n+k) | O(n+k) | ✅ Sim | `linear.py` |
| Counting Sort | O(n+k) | O(n+k) | ✅ Sim | `linear.py` |
| Radix Sort | O(d·n) | O(n+b) | ✅ Sim | `linear.py` |

## 🔀 Divisão de Trabalho 

| Membro | Responsabilidade | Arquivos |
|--------|-----------------|----------|
| **Gustavo** | Algoritmos quadráticos + lineares + utilitários | `quadratic.py`, `linear.py`, `utils.py` |
| **Pedro** | Algoritmos linearítmicos + modelo + integração | `linearithmic.py`, `models.py`, `main.py` |

## 🧪 Requisitos

- Python 3.10+
- Sem dependências externas (apenas biblioteca padrão)

## 📝 Licença

Consulte o arquivo [LICENSE](LICENSE).