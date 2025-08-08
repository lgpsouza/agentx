# 📘 Módulo 1 — Fundamentos de IA, Python e Docker

## 🎯 Objetivo
Construir a **base do ambiente de desenvolvimento** e criar a **primeira versão executável** do nosso agente inteligente, com estrutura organizada e pronta para evoluir.

---

## 📚 Conceitos-chave
1. **Organização de um projeto Python**
   - Estrutura de pastas (`src/`, `requirements.txt`, `Dockerfile`, `README.md`).
   - Separação de código por responsabilidade (`main.py`, `config.py`, `utils.py`).

2. **Controle de versão com Git e GitHub**
   - Criamos um repositório local.
   - Sincronizamos com um repositório remoto no GitHub.
   - Lidamos com a branch `main` e configurações iniciais do Git.

3. **Primeiro contato com Docker**
   - Criamos um `Dockerfile` para empacotar e rodar o agente em qualquer ambiente.

4. **Fundamentos de Python aplicados à IA**
   - Funções (`agentx_hello()`).
   - Módulos (`import`).
   - Uso de `config.py` para centralizar variáveis globais.

---

## 🛠 Passos práticos (80/20)
1. Criamos a estrutura do **AgentX** do zero.
2. Configuramos o ambiente para rodar localmente com:
   ```bash
   python src/main.py
   ```
3. Configuramos para rodar no Docker:
   ```bash
   docker build -t agentx .
   docker run --rm agentx
   ```
4. Subimos tudo para o GitHub para versionar e compartilhar.

---

## 💡 Mini-projeto aplicado
Montar o esqueleto do nosso agente inteligente com:
- Código executável em Python.
- Configuração Docker para portabilidade.
- Controle de versão no GitHub.

---

## 📝 Exercícios de fixação
1. Alterar o `agentx_hello()` para exibir também o **nome do agente** vindo do `config.py`.
2. Criar uma função `utils.greet_user(nome)` que imprima uma saudação personalizada.
3. Rodar o agente **localmente** e via **Docker**.

---

## 🔄 Revisão rápida
- Temos um **esqueleto funcional** do agente.
- Sabemos rodar localmente e em containers.
- Estamos versionando no GitHub.

---

## 🚀 Próximo passo — Módulo 2
No próximo módulo, vamos **ensinar o AgentX a receber comandos de texto e executar tarefas simples**, primeiro passo para torná-lo realmente inteligente.
