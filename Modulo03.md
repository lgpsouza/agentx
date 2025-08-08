# 📘 Módulo 3 — Frameworks de Agentes: Agno e CrewAI

## 🎯 Objetivo
Ampliar o AgentX utilizando frameworks modernos de agentes para:
- Integrar modelos de linguagem (LLMs) de forma nativa.
- Utilizar ferramentas externas para obter dados.
- Criar agentes colaborativos com papéis e objetivos distintos.

---

## 📚 Conceitos-chave
1. **Framework de agente** — estrutura pronta para criar e orquestrar agentes.
2. **Ferramentas** — funções externas que o agente pode acionar para buscar/processar informações.
3. **Agentes colaborativos** — múltiplos agentes com papéis definidos trabalhando juntos.
4. **LLM Integration** — modelos como GPT-4o-mini para interpretar e gerar respostas.
5. **Fluxo de trabalho (CrewAI)** — sequência de tarefas com repasse de informações entre agentes.

---

## 🛠 Passos práticos (80/20)

### Parte 1 — Agno
1. Instalamos dependências:
    ```bash
    pip install agno openai duckduckgo-search packaging
    ```
2. Criamos `src/agentx_agno.py` com:
    - Modelo GPT-4o-mini via `OpenAIChat`.
    - Ferramenta `buscar_web` usando `duckduckgo-search`.
    - Loop interativo para conversas.
3. Atualizamos `requirements.txt`:
    ```
    requests
    agno
    openai
    duckduckgo-search
    packaging
    ```
4. Ajustamos `Dockerfile` para instalar dependências.

### Parte 2 — CrewAI
1. Instalamos dependências:
    ```bash
    pip install crewai crewai-tools
    ```
2. Criamos `src/agentx_crewai.py` com:
    - Dois agentes: **Pesquisador** e **Redator**.
    - Ferramenta `SerperDevTool` para buscas online.
    - Tarefas (`Task`) com `expected_output` definido.
    - Execução via `Crew.kickoff()`.
3. Atualizamos `requirements.txt`:
    ```
    crewai
    crewai-tools
    ```

---

## 💡 Mini-projetos aplicados

**Parte 1 — Agno:**  
AgentX com LLM integrado e ferramenta de busca na web.

**Parte 2 — CrewAI:**  
Equipe de agentes trabalhando juntos: um pesquisa, o outro redige um resumo.

---

## 📄 Código adicionado/alterado

### `src/agentx_agno.py`
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.decorator import tool
from duckduckgo_search import DDGS

@tool
def buscar_web(query: str) -> str:
    if not query:
        return "Forneça um termo para busca."
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            title = r.get("title", "").strip()
            url = r.get("href", "").strip()
            snippet = r.get("body", "").strip()
            results.append(f"- {title}\n  {url}\n  {snippet}")
    if not results:
        return "Nenhum resultado encontrado."
    return "Resultados:\n" + "\n\n".join(results)

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[buscar_web],
    instructions="Você é o AgentX. Seja objetivo. Use a ferramenta 'buscar_web' quando precisar pesquisar."
)

if __name__ == "__main__":
    print("🤖 AgentX (Agno) iniciado! Digite 'sair' para encerrar.")
    while True:
        prompt = input("> ").strip()
        if prompt.lower() in {"sair", "exit", "quit"}:
            print("Até mais! 👋")
            break
        resp = agent.run(prompt)
        print(resp)
```

### `src/agentx_crewai.py`
```python
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
import os

search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))

pesquisador = Agent(
    role="Pesquisador de Conteúdo",
    goal="Encontrar informações confiáveis e relevantes sobre qualquer tópico solicitado",
    backstory="Você é um especialista em pesquisa que sabe encontrar e selecionar as melhores informações online.",
    tools=[search_tool],
    verbose=True
)

redator = Agent(
    role="Redator de Conteúdo",
    goal="Escrever um resumo claro, objetivo e bem formatado das informações recebidas",
    backstory="Você é um escritor experiente em transformar dados brutos em texto fluente e informativo.",
    verbose=True
)

tarefa_pesquisa = Task(
    description="Pesquise sobre Inteligência Artificial generativa no Brasil",
    expected_output="Uma lista com as principais descobertas e links das fontes consultadas.",
    agent=pesquisador
)

tarefa_redacao = Task(
    description="Com base nos resultados da pesquisa, escreva um resumo de até 3 parágrafos",
    expected_output="Um texto coeso, claro e objetivo, com no máximo 3 parágrafos.",
    agent=redator
)

crew = Crew(
    agents=[pesquisador, redator],
    tasks=[tarefa_pesquisa, tarefa_redacao],
    verbose=True
)

if __name__ == "__main__":
    resultado = crew.kickoff()
    print("\n📄 Resultado Final:\n")
    print(resultado)
```

---

## 📝 Exercícios de fixação
1. Criar um terceiro agente **Revisor** que melhore o texto final.
2. Adicionar mais ferramentas ao CrewAI, como tradução e análise de sentimento.
3. Usar o CrewAI para executar um fluxo com 3 ou mais etapas.

---

## 🔄 Revisão rápida
- **Agno**: deu ao AgentX poder de LLM com ferramenta de busca.
- **CrewAI**: permitiu criar múltiplos agentes que colaboram em tarefas.
- Estrutura flexível para adicionar mais papéis e ferramentas.

---
