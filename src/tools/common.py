"""Ferramentas comuns para todos os agentes."""

from langchain_core.tools import tool

@tool
def end_chat() -> str:
	"""Encerra a conversa com o cliente de forma cordial."""
	return "Atendimento encerrado. Obrigado por conversar com o Banco Ágil! Se precisar de algo no futuro, estaremos à disposição."

@tool
def redirect_triage() -> str:
	"""Transfere o atendimento para o agente de triagem."""
	return "TRANSFERÊNCIA: Cliente encaminhado para a triagem."

@tool
def redirect_credit() -> str:
	"""Transfere o atendimento para o agente de crédito."""
	return "TRANSFERÊNCIA: Cliente encaminhado para o serviço de crédito."

@tool
def redirect_credit_interview() -> str:
	"""Transfere o atendimento para o agente de entrevista de crédito."""
	return "TRANSFERÊNCIA: Cliente encaminhado para a entrevista de crédito."

@tool
def redirect_exchange() -> str:
	"""Transfere o atendimento para o agente de câmbio."""
	return "TRANSFERÊNCIA: Cliente encaminhado para o serviço de câmbio."
