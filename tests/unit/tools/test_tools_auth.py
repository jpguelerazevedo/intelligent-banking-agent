import pytest
from unittest.mock import patch
from src.tools.auth import triage_and_authenticate

@patch('src.tools.auth.get_client_by_cpf_and_birth')
def test_triage_and_authenticate_sucesso(mock_get_client):
    """Testa o cenário onde o cliente é encontrado com sucesso."""
    # Moca o retorno do banco de dados (CSV)
    mock_get_client.return_value = {
        'nome': 'João Silva',
        'limite_credito': '1500.00',
        'score': '750'
    }
    
    # Chama a Tool passando os parâmetros como ditados no LangChain (.invoke)
    result = triage_and_authenticate.invoke({
        "cpf": "123.456.789-01", 
        "birth_date": "01/01/1990", 
        "assunto": "Aumento de limite"
    })
    
    # Validações sem tocar no banco real
    assert "SUCESSO" in result
    assert "João Silva" in result
    assert "1500.0" in result
    assert "Aumento de limite" in result

@patch('src.tools.auth.get_client_by_cpf_and_birth')
def test_triage_and_authenticate_falha_nao_encontrado(mock_get_client):
    """Testa cenário onde o usuário não está no CSV."""
    mock_get_client.return_value = None
    
    result = triage_and_authenticate.invoke({
        "cpf": "000.000.000-00", 
        "birth_date": "01/01/1990", 
        "assunto": "Aumento"
    })
    
    assert "FALHA:" in result
    assert "não correspondem a nenhum cliente" in result

def test_triage_and_authenticate_falha_cpf_invalido():
    """Testa validação de máscara/tamanho de CPF."""
    result = triage_and_authenticate.invoke({
        "cpf": "1234", # CPF muito curto
        "birth_date": "01/01/1990", 
        "assunto": "Aumento"
    })
    
    assert "FALHA: CPF inválido" in result
