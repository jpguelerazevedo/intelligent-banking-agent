import pytest
from src.agents.credit_interview import CREDIT_INTERVIEW_TOOLS, CREDIT_INTERVIEW_SYSTEM_PROMPT

def test_configuracao_agente_entrevista():
    ferramentas_esperadas = ["calculate_credit_score", "update_client_score"]
    nomes_carregados = [t.name for t in CREDIT_INTERVIEW_TOOLS]
    
    for req in ferramentas_esperadas:
        assert req in nomes_carregados, f"Falta {req} em Entrevista"
        
    assert "Entrevista e coleta de dados" in CREDIT_INTERVIEW_SYSTEM_PROMPT.content
