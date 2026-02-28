# Intelligent Banking Agent

## Visão Geral do Projeto
O Intelligent Banking Agent é um ecossistema de atendimento ao cliente para um banco digital fictício, baseado em agentes de IA especializados. O objetivo é simular um atendimento bancário inteligente, modular e seguro, com fluxos claros e automação de decisões, utilizando LLMs e orquestração multi-agente.

## Estrutura do Código

```
├── app.py                 # Interação com Streamlit
├── main.py                # Interação com CLI
├── src/
│   ├── agents/            # Definição dos agentes e seus prompts
│   │   ├── triage.py
│   │   ├── credit.py
│   │   ├── credit_interview.py
│   │   └── exchange.py
│   ├── tools/             # Ferramentas (tools) de cada agente
│   │   ├── auth.py
│   │   ├── credit.py
│   │   ├── credit_interview.py
│   │   ├── exchange.py
│   │   └── common.py
│   ├── config.py          # Configuração do LLM e paths
│   ├── graph.py           # Orquestração do grafo multi-agente
│   └── state.py           # Definição do estado compartilhado
├── data/                  # Arquivos CSV de clientes, limites, solicitações
├── docs/                  # Documentação e fluxogramas
└── requirements.txt       # Dependências do projeto
```

## Arquitetura do Sistema
O sistema é composto por múltiplos agentes, cada um com responsabilidades bem definidas:

- **TRIAGE**: Responsável pela autenticação inicial e roteamento do cliente para o serviço adequado.
- **CREDIT**: Gerencia consultas e solicitações de aumento de limite de crédito.
- **CREDIT INTERVIEW**: Realiza entrevistas financeiras para recalcular o score do cliente.
- **EXCHANGE**: Fornece cotações de moedas estrangeiras em tempo real.

O fluxo entre agentes é orquestrado por um grafo de estados (LangGraph), que garante transições automáticas e uso obrigatório de ferramentas de transferência. O histórico de mensagens é preservado entre agentes, mantendo o contexto da conversa.

### Fluxograma da Arquitetura
![Fluxograma do sistema](docs/fluxograma.png)

> O fluxograma acima ilustra o fluxo entre os agentes, as ferramentas disponíveis em cada um e as possíveis transições.

## Funcionalidades Implementadas
- Autenticação de clientes via CPF e data de nascimento.
- Consulta e solicitação de aumento de limite de crédito.
- Entrevista financeira automatizada para recalcular score.
- Consulta de cotações de moedas (USD, EUR, JPY) em tempo real.
- Encaminhamento automático entre agentes conforme o pedido do cliente.
- Encerramento cordial do atendimento.

## Manipulação de Dados e Estado

O sistema utiliza um grafo de estados (LangGraph) para orquestrar o fluxo entre agentes. Toda a interação do usuário, respostas dos agentes e resultados de ferramentas são armazenados em um objeto de estado compartilhado (`AgentState`). Esse estado inclui:

- Histórico completo de mensagens (perguntas, respostas, tool calls e resultados), preservando o contexto da conversa mesmo após transferências entre agentes.
- Dados do cliente autenticado (nome, CPF, limite, score), atualizados dinamicamente conforme as ferramentas são usadas.
- Flags de controle, como agente atual (`current_agent`), tentativas de autenticação e sinalização de encerramento (`should_end`).

As transições entre agentes são feitas exclusivamente por ferramentas de transferência (ex: `redirect_triage`), garantindo rastreabilidade e controle do fluxo.

Para persistência, dados sensíveis (clientes, limites, solicitações) são lidos e gravados em arquivos CSV, permitindo fácil inspeção, testes e auditoria. Cada operação de consulta ou atualização de dados é feita por ferramentas específicas, que manipulam os arquivos de forma segura e transparente.

Esse modelo garante que:
- O contexto conversacional nunca é perdido, mesmo em fluxos complexos.
- Todas as decisões e atualizações são rastreáveis e auditáveis.
- O sistema é robusto contra inconsistências de estado e fácil de depurar.

## Escolhas Técnicas e Justificativas

- **Python**: Linguagem escolhida por sua ampla adoção em IA, facilidade de integração com bibliotecas de NLP, manipulação de dados e orquestração de fluxos conversacionais.
- **LangGraph**: Escolhido para orquestração multi-agente devido à flexibilidade, suporte a grafos de estado e integração nativa com LLMs, permitindo transições dinâmicas e controle preciso do fluxo.
- **LangChain + OpenAI**: Permite fácil binding de ferramentas, integração com modelos GPT, e controle do fluxo conversacional, além de facilitar logging e debugging.
- **LangSmith**: Utilizado para rastreamento, análise e depuração de fluxos de conversação, facilitando a identificação de falhas, análise de decisões do LLM e melhoria contínua dos prompts.
- **Persistência em CSV**: Dados de clientes, limites e solicitações são armazenados em arquivos CSV para simplicidade, transparência e fácil inspeção manual durante o desenvolvimento e testes.
- **API de Cotação Frankfurter**: Escolhida por ser gratuita, confiável e não exigir autenticação, permitindo obter cotações de moedas em tempo real sem custos ou limitações severas de uso.
- **Separação por módulos**: Cada agente e conjunto de ferramentas reside em seu próprio módulo, facilitando manutenção, extensibilidade e testes isolados.

### Escolha do Modelo LLM

Optou-se pelo uso do modelo **gpt5-mini** ao invés de modelos menores devido à necessidade de melhor compreensão e controle das transições entre agentes no fluxo multi-agente. Foram realizados testes com modelos menores, como o **gpt-4o-mini** e o **gpt-4.1-nano**, porém identificou-se um gargalo significativo no "entendimento" dessas transições, resultando em respostas inconsistentes e falhas no uso correto das ferramentas de transferência entre agentes. O **gpt5-mini** demonstrou desempenho superior nesse aspecto, garantindo maior robustez e aderência ao fluxo orquestrado, mesmo em cenários complexos de troca de contexto entre agentes.

## Desafios Enfrentados e Soluções
- **Obediência do LLM ao fluxo**: O maior desafio foi garantir que o LLM usasse sempre as ferramentas de transferência, sem improvisar respostas fora do escopo. Isso foi resolvido com prompts robustos, exemplos positivos/negativos e reforço de regras obrigatórias.
- **Persistência de contexto**: Manter o histórico de mensagens entre agentes sem poluir o contexto foi solucionado mantendo o state["messages"] integral, sem limpeza, e orientando os agentes a ignorar mensagens irrelevantes.
- **Separação de responsabilidades**: Cada agente foi projetado com escopo restrito e ferramentas específicas, evitando sobreposição de funções.
- **Testes de fluxo**: Foram realizados testes manuais e ajustes iterativos nos prompts e no grafo para garantir transições suaves e automáticas.

## Tutorial de Execução e Testes
1. Clone o repositório e instale as dependências:
	```bash
	git clone <repo-url>
	cd intelligent-banking-agent
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	```
2. Configure as variáveis de ambiente em `.env` (veja `.env.exemple`).
3. Execute o sistema:
	```bash
	python3 main.py
	```
4. Siga as instruções no terminal para interagir com o assistente.

### Testes
- Teste fluxos de autenticação, crédito, câmbio e entrevista.
- Simule pedidos fora do escopo para verificar se a transferência automática ocorre.
- Verifique os arquivos CSV para persistência dos dados.
