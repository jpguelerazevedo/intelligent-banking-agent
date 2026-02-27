from langchain_core.tools import tool

@tool
def end_chat() -> str:
	"""Encerra a conversa com o cliente de forma cordial."""
	return "Atendimento encerrado. Obrigado por conversar com o Banco Ágil! Se precisar de algo no futuro, estaremos à disposição."

@tool
def redirect_triage() -> str:
	"""Transfere o atendimento para o agente de triagem."""
	return "Você será redirecionado para o agente de triagem para dar continuidade ao seu atendimento."

@tool
def redirect_credit() -> str:
	"""Transfere o atendimento para o agente de crédito."""
	return "Você será redirecionado para o agente de crédito para tratar de assuntos relacionados a limite e solicitações de crédito."

@tool
def redirect_credit_interview() -> str:
	"""Transfere o atendimento para o agente de entrevista de crédito."""
	return "Você será redirecionado para o agente de entrevista de crédito para uma análise mais detalhada do seu perfil."

@tool
def redirect_exchange() -> str:
	"""Transfere o atendimento para o agente de câmbio."""
	return "Você será redirecionado para o agente de câmbio para consultar cotações de moedas."
