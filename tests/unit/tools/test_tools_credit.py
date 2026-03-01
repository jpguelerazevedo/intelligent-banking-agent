import pytest
from unittest.mock import patch
from src.tools.credit import consultar_limite, solicitar_aumento_limite

@patch('src.tools.credit.get_client_by_cpf')
def test_consultar_limite_existente(mock_get_client):
    """Testa consulta simples de limite do cliente validando seu retorno."""
    mock_get_client.return_value = {
        'nome': 'Maria Souza',
        'limite_credito': '2000.00',
        'score': '800'
    }
    
    result = consultar_limite.invoke({"cpf": "11122233344"})
    
    assert result['nome'] == 'Maria Souza'
    assert result['limite_credito'] == 2000.0
    assert result['score'] == 800

@patch('src.tools.credit.get_client_by_cpf')
def test_consultar_limite_inexistente(mock_get_client):
    mock_get_client.return_value = None
    result = consultar_limite.invoke({"cpf": "11122233344"})
    assert "erro" in result

@patch('src.tools.credit.register_limit_request')
@patch('src.tools.credit.update_client_field')
@patch('src.tools.credit.is_limit_approved')
@patch('src.tools.credit.get_client_by_cpf')
def test_solicitar_aumento_limite_aprovado(mock_get_client, mock_is_approved, mock_update, mock_register):
    """Testa aprovação de limite para cenários propícios, garantindo envio ao banco (mocks)."""
    mock_get_client.return_value = {
        'limite_credito': '1000.00',
        'score': '900'
    }
    mock_is_approved.return_value = True
    
    result = solicitar_aumento_limite.invoke({"cpf": "11122233344", "novo_limite": 1500.00})
    
    assert result['status'] == 'aprovado'
    assert result['limite_atual'] == 1000.0
    mock_update.assert_called_once_with("11122233344", "limite_credito", 1500.0)
    mock_register.assert_called_once()


@patch('src.tools.credit.get_client_by_cpf')
def test_solicitar_aumento_limite_invalido_menor_que_atual(mock_get_client):
    mock_get_client.return_value = {
        'limite_credito': '1000.00',
        'score': '900'
    }
    
    result = solicitar_aumento_limite.invoke({"cpf": "11122233344", "novo_limite": 500.00})
    
    assert "erro" in result
    assert "maior que o limite atual" in result["erro"]
