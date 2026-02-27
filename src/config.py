"""Configuração do LLM e caminhos de dados do projeto."""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def get_llm() -> ChatOpenAI:
    """Cria e retorna uma instância do ``ChatOpenAI``.

    Lê a chave de API da variável de ambiente ``OPENAI_API_KEY`` e o nome do
    modelo da variável ``LLM_MODEL_NAME``.

    """
    model_name = os.getenv("LLM_MODEL_NAME")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not model_name:
        raise EnvironmentError(
            "Variável de ambiente OPENAI_API_KEY ou LLM_MODEL_NAME não encontrada. "
            "Configure-as no arquivo .env na raiz do projeto."
        )
    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=0.3,
    )
