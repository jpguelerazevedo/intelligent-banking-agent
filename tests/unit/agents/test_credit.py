import pytest
from src.agents.credit import CREDIT_TOOLS, CREDIT_SYSTEM_PROMPT

def test_configuracao_agente_credito():
    ferramentas_esperadas = ["consultar_limite", "solicitar_aumento_limite", "redirect_credit_interview", "redirect_triage", "end_chat"]
    nomes_carregados = [t.name for t in CREDIT_TOOLS]
    
    for req in ferramentas_esperadas:
        assert req in nomes_carregados, f"Falta {req} em Crédito"
        
    assert "especializado em serviços de crédito" in CREDIT_SYSTEM_PROMPT.content
