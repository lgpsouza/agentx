# 🤖 AgentX — Agente Inteligente Modular

AgentX é um projeto de aprendizado progressivo para criar, orquestrar e implantar agentes inteligentes usando Python, Docker e frameworks modernos de IA.

---

## 📅 Roadmap de Módulos

### ✅ Módulo 1 — Fundamentos de IA, Python e Docker
- Estrutura inicial do projeto.
- Controle de versão com Git/GitHub.
- Execução local e em container Docker.
- **Mini-projeto:** Esqueleto do AgentX funcional.

### ✅ Módulo 2 — Criando seu Primeiro Agente em Python (CLI)
- Loop interativo (REPL) para receber comandos.
- Comandos: `hora`, `buscar <termo>` (Wikipédia), `ajuda`, `sair`.
- Estrutura modular (`agent.py`, `main.py`, `utils.py`).
- **Mini-projeto:** AgentX-CLI interativo.

### ✅ Módulo 3 — Frameworks de Agentes: Agno (Parte 1)
- Integração com **Agno**.
- Uso de modelos LLM (GPT-4o-mini via OpenAI).
- Ferramenta customizada de busca na web usando `duckduckgo-search`.
- **Mini-projeto:** AgentX com LLM + ferramenta de busca.

### ⏳ Módulo 3 — Frameworks de Agentes: CrewAI (Parte 2)
- Próxima etapa: criar agente com **CrewAI** para colaboração entre múltiplos papéis.

### 🔜 Módulo 4 — LangChain e Memória de Agentes
- Adicionar memória de curto e longo prazo.
- Contexto persistente entre interações.

### 🔜 Módulo 5 — Integrações e Automação
- Conexão com APIs externas.
- Execução de automações reais.

### 🔜 Módulo 6 — Orquestração, Multi-Agentes e Implantação
- Orquestração entre múltiplos agentes.
- Deploy em servidor/nuvem.

---

## 📂 Estrutura Atual do Projeto
```
agentx/
│
├── src/
│   ├── main.py             # Entrada do agente CLI
│   ├── agent.py            # Lógica do agente CLI
│   ├── agentx_agno.py      # Lógica do agente com Agno
│   ├── config.py           # Configurações globais
│   ├── utils.py            # Funções auxiliares
│   └── __init__.py
│
├── requirements.txt        # Dependências
├── Dockerfile              # Configuração de build
├── README.md               # Documentação
└── modulo_XX_resumo.md     # Resumos de cada módulo
```

---

## 🚀 Como Rodar
### Localmente
```bash
python src/main.py
```
ou
```bash
python src/agentx_agno.py
```

### Docker
```bash
docker build -t agentx .
docker run --rm agentx
```

Para rodar a versão Agno com chave OpenAI:
```bash
docker run -it --rm -e OPENAI_API_KEY=$OPENAI_API_KEY agentx python src/agentx_agno.py
```

---
