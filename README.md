# 🤖 AgentX — Curso de IA e Agentes Inteligentes

## 📚 Sobre o Projeto

Este repositório acompanha o curso **"Do Zero ao Avançado em IA e Agentes Inteligentes"**, onde construímos passo a passo o AgentX: um agente conversacional inteligente em Python, com integração a frameworks modernos de IA, memória e automação.

---

## 📦 Módulos Concluídos

### **Módulo 1 — Fundamentos de IA, Python e Docker**

* Estrutura inicial do projeto.
* Dockerfile e requirements.txt.
* Execução do "Hello World" com Python dentro do container.

### **Módulo 2 — Criando seu Primeiro Agente em Python**

* `main.py` com entrada/saída no terminal.
* Estrutura modular para evolução futura.
* Execução local e via Docker.

### **Módulo 3 — Frameworks de Agentes: Agno e CrewAI**

* **Agno**: agente simples com ferramentas e memória.
* **CrewAI**: orquestração de agentes com papéis e tarefas.
* Docker adaptado para cada agente.

### **Módulo 4 — LangChain e Memória de Agentes**

* **Memória de curto prazo** com `RunnableWithMessageHistory`.
* **Memória persistente** com FAISS.
* Atualização para evitar classes deprecadas no LangChain.
* Padronização com `.env` e `docker-compose.yml` para rodar qualquer módulo facilmente.

---

## 🚀 Como Rodar

### 1. Preparar ambiente

```bash
cp .env.example .env
# edite o .env e insira suas chaves
```

No `.env`:

```dotenv
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SERPER_API_KEY=serper_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### 2. Build da imagem

```bash
docker compose build
```

---

### 3. Executar cada módulo

**CLI básico (Módulo 2)**

```bash
docker compose run --rm agentx
```

**Agno (Módulo 3.1)**

```bash
docker compose run --rm agentx-agno
```

**CrewAI (Módulo 3.2)**

```bash
docker compose run --rm agentx-crewai
```

**LangChain — memória curta (Módulo 4.1)**

```bash
docker compose run --rm agentx-langchain
```

**LangChain + FAISS — memória persistente (Módulo 4.2)**

```bash
docker compose run --rm agentx-langchain-faiss
```

---

## 📂 Estrutura do Projeto

```
agentx/
 ├── src/
 │    ├── main.py
 │    ├── agentx_agno.py
 │    ├── agentx_crewai.py
 │    ├── agentx_langchain.py
 │    ├── agentx_langchain_faiss.py
 ├── requirements.txt
 ├── Dockerfile
 ├── docker-compose.yml
 ├── .env.example
 ├── .gitignore
 └── data/
      └── .gitkeep
```

---

## 📌 Próximos Passos

* **Módulo 5 — Integrações e Automação**

  * Conectar agentes a APIs externas.
  * Automação de tarefas com dados da internet e sistemas internos.
