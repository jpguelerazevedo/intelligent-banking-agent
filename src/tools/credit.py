import csv
import os
from datetime import datetime
from langchain_core.tools import tool
from src.config import DATA_DIR

CLIENTS_CSV = os.path.join(DATA_DIR, "clientes.csv")
SCORE_LIMIT_CSV = os.path.join(DATA_DIR, "score_limit.csv")
SOLICITACOES_CSV = os.path.join(DATA_DIR, "solicitacoes_aumento_limite.csv")

@tool
def consultar_limite(cpf: str) -> dict:
	"""Consulta o limite de crédito disponível para o cliente."""
	with open(CLIENTS_CSV, "r", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row["cpf"].strip() == cpf.strip():
				return {
					"cpf": cpf,
					"nome": row["nome"],
					"limite_credito": float(row["limite_credito"]),
					"score": int(row["score"])
				}
	return {"erro": "Cliente não encontrado."}

@tool
def solicitar_aumento_limite(cpf: str, novo_limite: float) -> dict:
	"""Solicita aumento de limite de crédito, registra o pedido e retorna o status.
	Bloqueia solicitações se o novo limite for igual ou inferior ao limite atual."""
	cliente = None
	with open(CLIENTS_CSV, "r", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row["cpf"].strip() == cpf.strip():
				cliente = row
				break
	if not cliente:
		return {"erro": "Cliente não encontrado."}

	limite_atual = float(cliente["limite_credito"])
	score = int(cliente["score"])
	status = "pendente"

	# Bloquear solicitação se já está no limite máximo ou novo limite não é maior
	if novo_limite <= limite_atual:
		return {
			"erro": "O novo limite solicitado deve ser maior que o limite atual.",
			"limite_atual": limite_atual,
			"novo_limite_solicitado": novo_limite
		}

	# Checar score para aprovação
	aprovado = False
	with open(SCORE_LIMIT_CSV, "r", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		for row in reader:
			if int(row["score_minimo"]) <= score <= int(row["score_maximo"]):
				max_limit = float(row["max_limit"])
				if novo_limite <= max_limit:
					aprovado = True
				break
	status = "aprovado" if aprovado else "rejeitado"

	# Se aprovado, atualizar o limite no clientes.csv
	if status == "aprovado":
		# Ler todos os clientes
		with open(CLIENTS_CSV, "r", encoding="utf-8") as f:
			reader = csv.DictReader(f)
			clientes = list(reader)
			fieldnames = reader.fieldnames
		# Atualizar o limite do cliente
		for row in clientes:
			if row["cpf"].strip() == cpf.strip():
				row["limite_credito"] = str(novo_limite)
				break
		# Salvar de volta
		with open(CLIENTS_CSV, "w", encoding="utf-8", newline="") as f:
			writer = csv.DictWriter(f, fieldnames=fieldnames)
			writer.writeheader()
			writer.writerows(clientes)

	# Registrar solicitação
	now = datetime.now().isoformat()
	registro = {
		"cpf_cliente": cpf,
		"data_hora_solicitacao": now,
		"limite_atual": limite_atual,
		"novo_limite_solicitado": novo_limite,
		"status_pedido": status
	}
	file_exists = os.path.isfile(SOLICITACOES_CSV)
	with open(SOLICITACOES_CSV, "a", encoding="utf-8", newline="\n") as f:
		writer = csv.DictWriter(f, fieldnames=list(registro.keys()))
		if not file_exists:
			writer.writeheader()
		writer.writerow(registro)

	return {
		"cpf": cpf,
		"limite_atual": limite_atual,
		"novo_limite_solicitado": novo_limite,
		"status": status
	}
