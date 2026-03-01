import pytest
from src.agents.exchange import EXCHANGE_TOOLS, EXCHANGE_SYSTEM_PROMPT

def test_configuracao_agente_cambio():
    ferramentas_esperadas = ["get_exchange", "end_chat", "redirect_triage"]
    nomes_carregados = [t.name for t in EXCHANGE_TOOLS]
    
    for req in ferramentas_esperadas:
        assert req in nomes_carregados, f"Falta {req} em Câmbio"
    
    assert "cotações de moedas" in EXCHANGE_SYSTEM_PROMPT.content
