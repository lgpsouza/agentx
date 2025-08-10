# 📘 Módulo 4 — LangChain e Memória de Agentes

## 🎯 Objetivo

Dar **memória** ao AgentX para que ele use contexto recente (curto prazo) e **lembre** informações entre sessões (memória persistente com FAISS). Também padronizamos a execução via **Docker Compose** e `.env`.

---

## 📚 Conceitos‑chave

* **RunnableWithMessageHistory**: forma moderna do LangChain para manter histórico de mensagens sem classes deprecadas.
* **Memória de curto prazo**: histórico só da sessão atual (em memória).
* **Memória persistente**: usa **FAISS** para salvar e consultar fatos passados.
* **Retriever consciente do histórico**: reformula perguntas usando o histórico para recuperar documentos relevantes.
* **.env + Docker Compose**: variáveis de ambiente seguras e execução simplificada.

---

## 🛠 Passos práticos (80/20)

1. **Instalamos dependências** (no `requirements.txt`):

   ```txt
   langchain
   langchain-openai
   langchain-community
   faiss-cpu
   ```
2. **Criamos/atualizamos arquivos**:

   * `src/agentx_langchain.py` → memória de **curto prazo** (sem warnings).
   * `src/agentx_langchain_faiss.py` → memória **persistente** com FAISS.
   * `.env.example` + `.env` → chaves de API.
   * `docker-compose.yml` → serviços prontos para cada módulo.
3. **Rodamos com Compose**:

   ```bash
   docker compose build
   docker compose run --rm agentx-langchain           # curto prazo
   docker compose run --rm agentx-langchain-faiss     # persistente
   ```

---

## 💡 Mini‑projeto aplicado

* **AgentX com histórico de sessão** (curto prazo) para conversas mais coerentes.
* **AgentX com FAISS** (persistente) para lembrar fatos entre execuções.

---

## 📄 Código adicionado/alterado

### `src/agentx_langchain.py` — Memória de curto prazo

```python
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
        print(resp.content)
```

### `src/agentx_langchain_faiss.py` — Memória persistente (FAISS)

```python
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
```

### `.env.example`

```dotenv
# Copie para .env e preencha com suas chaves reais
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SERPER_API_KEY=serper_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### `docker-compose.yml`

```yaml
version: "3.9"

services:
  agentx:
    build: .
    env_file:
      - .env
    tty: true
    stdin_open: true
    command: ["python", "src/main.py"]

  agentx-agno:
    build: .
    env_file:
      - .env
    tty: true
    stdin_open: true
    command: ["python", "src/agentx_agno.py"]

  agentx-langchain:
    build: .
    env_file:
      - .env
    tty: true
    stdin_open: true
    command: ["python", "src/agentx_langchain.py"]

  agentx-langchain-faiss:
    build: .
    env_file:
      - .env
    tty: true
    stdin_open: true
    volumes:
      - ./data:/app/data
    command: ["python", "src/agentx_langchain_faiss.py"]

  agentx-crewai:
    build: .
    env_file:
      - .env
    tty: true
    stdin_open: true
    command: ["python", "src/agentx_crewai.py"]
```

---

## 🧪 Como testar (Compose)

```bash
docker compose build

docker compose run --rm agentx-langchain           # curto prazo
# Exemplo:
# > Oi, eu sou a Maria
# > Qual é o meu nome?

/docker compose run --rm agentx-langchain-faiss     # persistente
# Diga algo para persistir, saia e rode de novo: o agente deve lembrar
```

---

## 📝 Exercícios de fixação

1. Guardar **apenas fatos importantes** no FAISS (ex.: “meu nome é…”, “meu e-mail é…”).
2. Adicionar um comando `exportar_memoria` que compacte a pasta `data/`.
3. Trocar o FAISS por **Chroma** e comparar.

---

## 🔄 Revisão rápida

* Removemos depreciações do LangChain.
* Implementamos memória de **curto prazo** e **persistente**.
* Padronizamos execução com **`.env` + Docker Compose**.

---

## 🚀 Próximo passo

Integrar ferramentas ao pipeline do LangChain (web, arquivos, banco de dados) e conectar a memória com ações reais — preparando o Módulo 5 (Integrações e Automação).
