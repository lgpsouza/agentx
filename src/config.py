# Configurações globais do agente

AGENT_NAME = "AgentX"
VERSION = "0.1"
DEBUG = True
# src/utils.py
def log(msg: str):   print(f"[AgentX] {msg}")
def warn(msg: str):  print(f"[!] {msg}")
def error(msg: str): print(f"[x] {msg}")
