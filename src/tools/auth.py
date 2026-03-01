"""Tool única para autenticação e triagem de solicitações do Banco Ágil."""

import logging
from langchain_core.tools import tool
from src.utils.db_utils import get_client_by_cpf_and_birth, _clean_cpf

logger = logging.getLogger(__name__)

@tool
def triage_and_authenticate(cpf: str, birth_date: str, assunto: str) -> str:
	"""Autentica o cliente e retorna o assunto da solicitação.

	Args:
		cpf: CPF do cliente (apenas números, 11 dígitos).
		birth_date: Data de nascimento no formato DD/MM/AAAA.
		assunto: Assunto da solicitação do cliente.

	Returns:
		String com status de autenticação, nome do cliente (se autenticado) e assunto.
	"""
	cpf_clean = _clean_cpf(cpf)

	if len(cpf_clean) != 11 or not cpf_clean.isdigit():
		return f"FALHA: CPF inválido. O CPF deve conter exatamente 11 dígitos numéricos. Assunto: {assunto}"

	client = get_client_by_cpf_and_birth(cpf, birth_date)
	
	if client is not None:
		return (
			f"SUCESSO: Cliente autenticado. "
			f"Nome: {client['nome']}. "
			f"CPF: {cpf_clean}. Assunto: {assunto}. "
			f"Limite de crédito: R$ {float(client['limite_credito'])}. "
			f"Score: {float(client['score'])}."
		)

	return f"FALHA: CPF ou data de nascimento não correspondem a nenhum cliente cadastrado. Assunto: {assunto}"
"""Ferramenta de autenticação de clientes do Banco Ágil."""