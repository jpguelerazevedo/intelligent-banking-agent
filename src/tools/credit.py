import logging
from langchain_core.tools import tool
from src.utils.db_utils import (
	get_client_by_cpf,
	is_limit_approved,
	update_client_field,
	register_limit_request
)

logger = logging.getLogger(__name__)

@tool
def consultar_limite(cpf: str) -> dict:
	"""Consulta o limite de crédito disponível para o cliente."""
	cliente = get_client_by_cpf(cpf)
	if cliente:
		return {
			"cpf": cpf,
			"nome": cliente["nome"],
			"limite_credito": float(cliente["limite_credito"]),
			"score": int(cliente["score"])
		}
	return {"erro": "Cliente não encontrado."}

@tool
def solicitar_aumento_limite(cpf: str, novo_limite: float) -> dict:
	"""Solicita aumento de limite de crédito, registra o pedido e retorna o status.
	Bloqueia solicitações se o novo limite for igual ou inferior ao limite atual."""
	cliente = get_client_by_cpf(cpf)
	if not cliente:
		return {"erro": "Cliente não encontrado."}

	limite_atual = float(cliente["limite_credito"])
	score = int(cliente["score"])

	# Bloquear solicitação se já está no limite máximo ou novo limite não é maior
	if novo_limite <= limite_atual:
		return {
			"erro": "O novo limite solicitado deve ser maior que o limite atual.",
			"limite_atual": limite_atual,
			"novo_limite_solicitado": novo_limite
		}

	# Checar score para aprovação
	aprovado = is_limit_approved(score, novo_limite)
	status = "aprovado" if aprovado else "rejeitado"

	# Se aprovado, atualizar o limite
	if status == "aprovado":
		update_client_field(cpf, "limite_credito", novo_limite)

	# Registrar solicitação
	register_limit_request(cpf, limite_atual, novo_limite, status)

	return {
		"cpf": cpf,
		"limite_atual": limite_atual,
		"novo_limite_solicitado": novo_limite,
		"status": status
	}
