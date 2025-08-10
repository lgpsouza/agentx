# src/agentx_langchain_faiss.py
import os
from pathlib import Path

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

DB_PATH = "data/faiss_memory"
os.makedirs("data", exist_ok=True)

# LLM e Embeddings
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    api_key=os.getenv("OPENAI_API_KEY"),
)
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

# Carrega ou cria FAISS
if Path(DB_PATH).exists():
    vectorstore = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
else:
    vectorstore = FAISS.from_texts(["Memória inicial do AgentX."], embeddings)
    vectorstore.save_local(DB_PATH)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 1) Retriever ciente do histórico (reformula a pergunta conforme o contexto)
rephrase_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Reescreva a pergunta do usuário considerando o histórico da conversa."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm=llm, retriever=retriever, prompt=rephrase_prompt
)

# 2) Cadeia que insere documentos + responde
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Use o contexto para responder. Se não souber, diga que não sabe.\n\nContexto:\n{context}"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
doc_chain = create_stuff_documents_chain(llm, qa_prompt)

# 3) Retrieval chain completa
retrieval_chain = create_retrieval_chain(history_aware_retriever, doc_chain)

# Histórico por sessão
store: dict[str, ChatMessageHistory] = {}
def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 4) Encapsula com histórico (a chave do histórico aqui é 'chat_history')
qa_with_history = RunnableWithMessageHistory(
    retrieval_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

if __name__ == "__main__":
    print("🤖 AgentX (LangChain + FAISS) com memória persistente. Digite 'sair' para encerrar.")
    session_id = "cli"
    while True:
        user = input("> ").strip()
        if user.lower() in {"sair", "exit", "quit"}:
            print("Até mais! 👋")
            break

        result = qa_with_history.invoke(
            {"input": user},
            config={"configurable": {"session_id": session_id}},
        )
        answer = result["answer"] if isinstance(result, dict) else str(result)
        print(answer)

        # Salva o par Q/A na base vetorial (persistência)
        vectorstore.add_texts([f"Pergunta: {user}\nResposta: {answer}"])
        vectorstore.save_local(DB_PATH)
