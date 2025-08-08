
# src/agentx_agno.py
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.decorator import tool
from duckduckgo_search import DDGS

@tool
def buscar_web(query: str) -> str:
    """
    Busca na web (DuckDuckGo) e retorna os 5 principais resultados sumarizados.
    """
    if not query:
        return "Forneça um termo para busca."
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            # r contém keys como 'title', 'href', 'body'
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
        # O Agno decide quando chamar a tool
        resp = agent.run(prompt)
        print(resp)
