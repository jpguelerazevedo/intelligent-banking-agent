import pytest
from unittest.mock import patch
from src.tools.credit_interview import calculate_credit_score, update_client_score

def test_calculate_credit_score_cenario_1():
    """Testa regra de negócio que pondera: Peso de 1 dependente + Renda Alta + Autonomo"""
    result = calculate_credit_score.invoke({
        "renda_mensal": 5000.0,
        "tipo_emprego": "formal",
        "despesas_fixas": 2000.0,
        "num_dependentes": 1,
        "tem_dividas": "não"
    })
    
    # 5k / 2001 * 30 + 300 (formal) + 80 (1 dep) + 100 (sem div)
    # 74.96 + 300 + 80 + 100 ~= 555
    assert "score" in result
    assert result["score"] >= 500
    assert result["detalhes"]["tipo_emprego"] == "formal"

def test_calculate_credit_score_entradas_invalidas():
    result = calculate_credit_score.invoke({
        "renda_mensal": -100.0,  # não pode ser negativo
        "tipo_emprego": "formal",
        "despesas_fixas": 0.0,
        "num_dependentes": 0,
        "tem_dividas": "não"
    })
    
    assert "erro" in result
    assert "negativa" in result["erro"]

@patch('src.tools.credit_interview.update_client_field')
def test_update_client_score(mock_update):
    mock_update.return_value = "500" # o Old score mock
    
    result = update_client_score.invoke({"cpf": "12345678901", "new_score": 750})
    
    mock_update.assert_called_once_with("12345678901", "score", 750)
    assert "ATUALIZADO" in result
    assert "750" in result
