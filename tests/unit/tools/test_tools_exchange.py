import pytest
from unittest.mock import patch, MagicMock
from src.tools.exchange import get_exchange

@patch('src.tools.exchange.requests.get')
def test_get_exchange_sucesso(mock_get):
    """Moca uma requisição completa simulando a REST da Frankfurter e testa resposta."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "amount": 1.0,
        "base": "USD",
        "date": "2026-02-28",
        "rates": {"BRL": 5.10}
    }
    mock_get.return_value = mock_response
    
    result = get_exchange.invoke({"currency_code": "USD"})
    
    assert result['moeda'] == 'USD'
    assert result['cotacao_brl'] == 5.10
    assert result['fonte'] == 'frankfurter.dev'

def test_get_exchange_moeda_nao_suportada():
    """Valida se envio de código aleatório é barrado pela tool."""
    result = get_exchange.invoke({"currency_code": "XYZ"})
    assert "erro" in result
    assert "Moeda não suportada" in result["erro"]

@patch('src.tools.exchange.requests.get')
def test_get_exchange_falha_api(mock_get):
    """Testa como a tool se comporta caso a API saia do ar caindo na Exception."""
    mock_get.side_effect = Exception("Timeout da API")
    
    result = get_exchange.invoke({"currency_code": "EUR"})
    
    assert "erro" in result
    assert "Erro ao consultar a cotação" in result["erro"]
