# 📘 Módulo 4 — Criando seu Primeiro Agente em Python (CLI)

## 🎯 Objetivo
Ensinar o **AgentX** a receber comandos em texto e executar ações simples, criando a base para um agente interativo.

---

## 📚 Conceitos-chave
1. **REPL (Read–Eval–Print–Loop)**  
   - Estrutura de loop para ler comandos, processar e responder.
2. **Roteamento de comandos**  
   - Mapeamento de strings para funções (handlers).
3. **Boas práticas de organização**  
   - Separar a lógica do agente (`agent.py`) da interface (`main.py`) e utilitários (`utils.py`).
4. **Uso de APIs externas**  
   - Consulta à Wikipédia via API REST.

---

## 🛠 Passos práticos (80/20)
1. Criamos o arquivo `agent.py` com:
   - Loop de execução interativo.
   - Tratamento de interrupções (CTRL+C, CTRL+D).
   - Comandos:
     - `hora` → Mostra data/hora atual.
     - `buscar <termo>` → Retorna resumo da Wikipédia em português.
     - `ajuda` → Lista comandos.
     - `sair` → Finaliza o agente.
2. Ajustamos `main.py` para iniciar o agente com `AgentX.run()`.
3. Melhoramos `utils.py` com funções de log.
4. Rodamos no Docker com `-it` para entrada interativa.

---

## 💡 Mini-projeto aplicado
Implementação de um **Agente CLI** com suporte a múltiplos comandos, capaz de interagir com a web e processar entradas do usuário em tempo real.

---

## 📝 Exercícios de fixação
1. Criar comando `eco <texto>` que repete o texto informado.
2. Criar comando `versao` que exibe `AGENT_NAME` e `VERSION` do `config.py`.
3. Tratar buscas com acentos e frases longas (já suportado, mas testar).
4. Adicionar histórico de comandos em `~/.agentx_history.log`.

---

## 🔄 Revisão rápida
- O AgentX agora é interativo.
- Entende e executa múltiplos comandos.
- Consegue buscar informações na web.
- Estrutura modular preparada para expansão.

---

## 🚀 Próximo passo — Módulo 3
No próximo módulo, vamos integrar frameworks como **Agno** ou **CrewAI** para dar mais estrutura, memória e capacidades de automação ao nosso agente.