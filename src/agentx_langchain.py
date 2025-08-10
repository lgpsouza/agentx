# src/agentx_langchain.py
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Prompt com placeholder para histórico
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é o AgentX. Seja útil, conciso e educado."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

# Cadeia básica: prompt -> LLM
chain = prompt | llm

# Store de históricos por sessão
store: dict[str, ChatMessageHistory] = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Adapta a cadeia para manter histórico
chat_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

if __name__ == "__main__":
    print("🤖 AgentX (LangChain) com memória de curto prazo. Digite 'sair' para encerrar.")
    session_id = "cli"  # poderia ser um ID do usuário
    while True:
        user = input("> ").strip()
        if user.lower() in {"sair", "exit", "quit"}:
            print("Até mais! 👋")
            break
        resp = chat_with_history.invoke(
            {"input": user},
            config={"configurable": {"session_id": session_id}},
        )
        # resp é um AIMessage
        print(resp.content)
