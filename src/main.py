# src/main.py
from config import AGENT_NAME
from agent import AgentX

def agentx_start():
    print(f"🤖 {AGENT_NAME} inicializado!")
    AgentX(AGENT_NAME).run()

if __name__ == "__main__":
    agentx_start()
