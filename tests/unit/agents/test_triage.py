import pytest
from src.agents.triage import TRIAGE_TOOLS, TRIAGE_SYSTEM_PROMPT

def test_configuracao_agente_triagem():
    """Valida se o Prompt e as Tools do primeiro agente batem com a arquitetura definida."""
    ferramentas_esperadas = ["triage_and_authenticate", "end_chat", "redirect_credit", "redirect_exchange"]
    nomes_carregados = [t.name for t in TRIAGE_TOOLS]
    
    for req in ferramentas_esperadas:
        assert req in nomes_carregados, f"Falta {req} em Triage"
    
    assert "assistente virtual do Banco Ágil, atuando como o primeiro contato" in TRIAGE_SYSTEM_PROMPT.content
