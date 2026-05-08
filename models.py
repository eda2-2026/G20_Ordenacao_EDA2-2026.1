

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Pacote:
    

    peso: float
    cep: str
    prioridade: int
    data_postagem: datetime
    id_pacote: str = field(default_factory=lambda: str(uuid4()))

    
    def __post_init__(self) -> None:
        
        if not (0.0 < self.peso <= 30.0):
            raise ValueError(f"Peso fora do intervalo (0, 30]: {self.peso}")
        if len(self.cep) != 8 or not self.cep.isdigit():
            raise ValueError(f"CEP inválido (deve ter 8 dígitos): {self.cep}")
        if self.prioridade not in range(1, 6):
            raise ValueError(f"Prioridade deve ser 1–5: {self.prioridade}")

    
    def __repr__(self) -> str:
        data_fmt = self.data_postagem.strftime("%d/%m/%Y %H:%M")
        return (
            f"Pacote(id={self.id_pacote[:8]}..., peso={self.peso:.2f}kg, "
            f"CEP={self.cep}, prio={self.prioridade}, data={data_fmt})"
        )
