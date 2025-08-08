from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
import os

# Ferramenta de busca (usa Serper API)
search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))

# Agente 1 — Pesquisador
pesquisador = Agent(
    role="Pesquisador de Conteúdo",
    goal="Encontrar informações confiáveis e relevantes sobre qualquer tópico solicitado",
    backstory="Você é um especialista em pesquisa que sabe encontrar e selecionar as melhores informações online.",
    tools=[search_tool],
    verbose=True
)

# Agente 2 — Redator
redator = Agent(
    role="Redator de Conteúdo",
    goal="Escrever um resumo claro, objetivo e bem formatado das informações recebidas",
    backstory="Você é um escritor experiente em transformar dados brutos em texto fluente e informativo.",
    verbose=True
)

# Definição das tarefas com expected_output obrigatório
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

# Montagem da equipe
crew = Crew(
    agents=[pesquisador, redator],
    tasks=[tarefa_pesquisa, tarefa_redacao],
    verbose=True
)

if __name__ == "__main__":
    resultado = crew.kickoff()
    print("\n📄 Resultado Final:\n")
    print(resultado)
