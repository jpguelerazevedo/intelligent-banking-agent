"""Utilitários para acesso e manipulação dos dados dos clientes e regras de crédito."""

import csv
import logging
import os
from datetime import datetime
from src.config import DATA_DIR

logger = logging.getLogger(__name__)
CLIENTS_CSV = os.path.join(DATA_DIR, "clientes.csv")
SCORE_LIMIT_CSV = os.path.join(DATA_DIR, "score_limit.csv")
SOLICITACOES_CSV = os.path.join(DATA_DIR, "solicitacoes_aumento_limite.csv")


def _clean_cpf(cpf: str) -> str:
    """Limpa o cpf para verificação no csv, removendo pontos, traços e espaços."""
    return cpf.replace(".", "").replace("-", "").replace(" ", "").strip()

def get_client_by_cpf(cpf: str) -> dict | None:
    """Retorna os dados do cliente buscando pelo CPF."""
    cpf_clean = _clean_cpf(cpf)
    try:
        with open(CLIENTS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if _clean_cpf(row["cpf"]) == cpf_clean:
                    return row
    except FileNotFoundError:
        logger.error("Arquivo %s não encontrado.", CLIENTS_CSV)
    except Exception as e:
        logger.error("Erro ao ler %s: %s", CLIENTS_CSV, e)
    return None


def get_client_by_cpf_and_birth(cpf: str, birth_date: str) -> dict | None:
    """Retorna os dados do cliente validando CPF e data de nascimento."""
    cpf_clean = _clean_cpf(cpf)
    birth_clean = birth_date.strip()
    try:
        with open(CLIENTS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if _clean_cpf(row["cpf"]) == cpf_clean and row["data_nascimento"].strip() == birth_clean:
                    return row
    except FileNotFoundError:
        logger.error("Arquivo %s não encontrado.", CLIENTS_CSV)
    except Exception as e:
        logger.error("Erro ao ler %s: %s", CLIENTS_CSV, e)
    return None

def update_client_field(cpf: str, field: str, new_value) -> dict | None:
    """Atualiza um campo específico do cliente no arquivo clientes.csv.
    Retorna o valor anterior do campo se for bem-sucedido, None caso contrário."""
    cpf_clean = _clean_cpf(cpf)
    old_value = None
    updated = False
    try:
        with open(CLIENTS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = list(reader)
            
        for row in rows:
            if _clean_cpf(row["cpf"]) == cpf_clean:
                old_value = row[field]
                row[field] = str(new_value)
                updated = True
                break
                
        if updated:
            with open(CLIENTS_CSV, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            return old_value
    except FileNotFoundError:
        logger.error("Arquivo %s não encontrado.", CLIENTS_CSV)
    except Exception as e:
        logger.error("Erro ao atualizar %s: %s", CLIENTS_CSV, e)
    
    return None


def is_limit_approved(score: int, novo_limite: float) -> bool:
    """Verifica na tabela score_limit.csv se o novo \
    limite solicitado é permitido para o score do cliente."""
    try:
        with open(SCORE_LIMIT_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row["score_minimo"]) <= score <= int(row["score_maximo"]):
                    max_limit = float(row["max_limit"])
                    if novo_limite <= max_limit:
                        return True
                    break
    except FileNotFoundError:
        logger.error("Arquivo %s não encontrado.", SCORE_LIMIT_CSV)
    except Exception as e:
        logger.error("Erro ao ler %s: %s", SCORE_LIMIT_CSV, e)
    return False

def register_limit_request(cpf: str, limite_atual: float, novo_limite: float, status: str) -> bool:
    """Registra uma solicitação de aumento de limite no arquivo de solicitações."""
    now = datetime.now().isoformat()
    registro = {
        "cpf_cliente": cpf,
        "data_hora_solicitacao": now,
        "limite_atual": limite_atual,
        "novo_limite_solicitado": novo_limite,
        "status_pedido": status
    }
    file_exists = os.path.isfile(SOLICITACOES_CSV)
    try:
        with open(SOLICITACOES_CSV, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(registro.keys()))
            if not file_exists:
                writer.writeheader()
            writer.writerow(registro)
        return True
    except Exception as e:
        logger.error("Erro ao gravar em %s: %s", SOLICITACOES_CSV, e)
        return False
