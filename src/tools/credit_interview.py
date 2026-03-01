"""Ferramentas de entrevista financeira para recálculo e update de score de crédito."""
import logging
from langchain_core.tools import tool
from src.utils.db_utils import update_client_field

logger = logging.getLogger(__name__)

PESO_RENDA = 30

PESO_EMPREGO = {
    "formal": 300,
    "autônomo": 200,  # Aceitar variação sem acento
    "desempregado": 0,
}

PESO_DEPENDENTES = {
    0: 100,
    1: 80,
    2: 60,
}

PESO_DEPENDENTES_3_MAIS = 30

PESO_DIVIDAS = {
    "sim": -100,
    "não": 100,
}

@tool
def calculate_credit_score(
    renda_mensal: float,
    tipo_emprego: str,
    despesas_fixas: float,
    num_dependentes: int,
    tem_dividas: str,
) -> dict:
    """Calcula um novo score de crédito com base em dados da entrevista financeira.
    Retorna um dicionário com o score e detalhes ou mensagem de erro.
    """
    # Validar entradas
    if renda_mensal < 0:
        return {"erro": "Renda mensal não pode ser negativa."}
    if despesas_fixas < 0:
        return {"erro": "Despesas fixas não podem ser negativas."}
    if num_dependentes < 0:
        return {"erro": "Número de dependentes não pode ser negativo."}
    tipo_emprego_lower = tipo_emprego.lower().strip()
    if tipo_emprego_lower not in PESO_EMPREGO:
        return {"erro": "Tipo de emprego inválido. Use: formal, autônomo ou desempregado."}
    tem_dividas_lower = tem_dividas.lower().strip()
    if tem_dividas_lower not in PESO_DIVIDAS:
        return {"erro": "Resposta sobre dívidas inválida. Use: sim ou não."}
    # Calcular score
    peso_dep = PESO_DEPENDENTES.get(num_dependentes, PESO_DEPENDENTES_3_MAIS)
    score = (
        (renda_mensal / (despesas_fixas + 1)) * PESO_RENDA
        + PESO_EMPREGO[tipo_emprego_lower]
        + peso_dep
        + PESO_DIVIDAS[tem_dividas_lower]
    )
    score = max(0, min(1000, int(round(score))))
    return {
        "score": score,
        "detalhes": {
            "renda_mensal": renda_mensal,
            "despesas_fixas": despesas_fixas,
            "tipo_emprego": tipo_emprego_lower,
            "num_dependentes": num_dependentes,
            "tem_dividas": tem_dividas_lower
        }
    }

@tool
def update_client_score(cpf: str, new_score: int) -> str:
    """Atualiza o score de crédito de um cliente em clientes.csv.
    Retorna confirmação com scores anterior e novo, ou mensagem de erro.
    """
    old_score = update_client_field(cpf, "score", new_score)
    if old_score is not None:
        return (
            f"ATUALIZADO: Score do cliente atualizado de {old_score} para "
            f"{new_score}."
        )
    return "ERRO: Cliente não encontrado na base de dados ou ocorreu um erro."
