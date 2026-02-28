import requests
from langchain_core.tools import tool

API_URL = "https://api.frankfurter.dev/v1/latest"

CURRENCY_NAMES: dict[str, str] = {
    "USD": "Dólar Americano",
    "EUR": "Euro",
    "JPY": "Iene Japonês",
}

@tool
def get_exchange(currency_code: str) -> dict:
    """
    Obtém a cotação atual da moeda desejada em relação ao real (BRL).
    Args:
        currency_code: Código da moeda (USD, EUR, JPY).
    Returns:
        Dicionário com nome da moeda, cotação, data da cotação e fonte, ou mensagem de erro.
    """
    code = currency_code.upper().strip()
    if code not in CURRENCY_NAMES:
        return {"erro": f"Moeda não suportada. Opções: {', '.join(CURRENCY_NAMES.keys())}"}
    try:
        response = requests.get(API_URL, params={"base": code, "symbols": "BRL"}, timeout=10)
        data = response.json()
        # Frankfurter retorna 'rates' e 'date' também
        if "rates" in data and "BRL" in data["rates"]:
            return {
                "moeda": code,
                "nome": CURRENCY_NAMES[code],
                "cotacao_brl": data["rates"]["BRL"],
                "data_cotacao": data.get("date"),
                "fonte": "frankfurter.dev"
            }
        else:
            return {"erro": "Não foi possível obter a cotação no momento."}
    except Exception as e:
        return {"erro": f"Erro ao consultar a cotação: {str(e)}"}
