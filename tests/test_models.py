"""
Testes para a modelagem de dados do projeto.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from datetime import datetime
from models import Pacote

def test_criacao_pacote_valido():
    """Testa a criação de um pacote com dados corretos."""
    pacote = Pacote(
        peso=15.5,
        cep="12345678",
        prioridade=3,
        data_postagem=datetime(2026, 5, 10, 14, 30)
    )
    assert pacote.peso == 15.5
    assert pacote.cep == "12345678"
    assert pacote.prioridade == 3
    assert pacote.id_pacote is not None

def test_validacao_peso():
    """Testa se pesos inválidos levantam erro."""
    with pytest.raises(ValueError, match="Peso fora do intervalo"):
        Pacote(peso=0.0, cep="12345678", prioridade=3, data_postagem=datetime.now())
    
    with pytest.raises(ValueError, match="Peso fora do intervalo"):
        Pacote(peso=30.1, cep="12345678", prioridade=3, data_postagem=datetime.now())

def test_validacao_cep():
    """Testa se CEPs inválidos levantam erro."""
    with pytest.raises(ValueError, match="CEP inválido"):
        Pacote(peso=10.0, cep="1234567", prioridade=3, data_postagem=datetime.now())  # 7 dígitos
    
    with pytest.raises(ValueError, match="CEP inválido"):
        Pacote(peso=10.0, cep="1234567A", prioridade=3, data_postagem=datetime.now())  # Contém letra

def test_validacao_prioridade():
    """Testa se prioridades fora do intervalo 1-5 levantam erro."""
    with pytest.raises(ValueError, match="Prioridade deve ser 1–5"):
        Pacote(peso=10.0, cep="12345678", prioridade=6, data_postagem=datetime.now())

if __name__ == "__main__":
    pytest.main(["-v", __file__])
