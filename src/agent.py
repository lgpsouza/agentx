# src/agent.py
from datetime import datetime
import requests
from utils import log

class AgentX:
    def __init__(self, name: str):
        self.name = name
        self._commands = {
            "hora": self.cmd_hora,
            "buscar": self.cmd_buscar,
            "ajuda": self.cmd_ajuda,
            "sair": self.cmd_sair,
        }
        self._running = True

    # Loop principal
    def run(self):
        log(f"{self.name} pronto. Digite 'ajuda' para ver comandos.")
        while self._running:
            try:
                cmdline = input("> ").strip()
                if not cmdline:
                    continue
                self.dispatch(cmdline)
            except (KeyboardInterrupt, EOFError):
                print()
                self._running = False
                log("Encerrando...")

    # Roteador de comandos
    def dispatch(self, cmdline: str):
        parts = cmdline.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        handler = self._commands.get(cmd)
        if handler:
            handler(args)
        else:
            log(f"Comando desconhecido: '{cmd}'. Digite 'ajuda'.")

    # Comando: hora
    def cmd_hora(self, _: str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🕒 Agora: {now}")

    # Comando: buscar na Wikipédia
    def cmd_buscar(self, termo: str):
        if not termo:
            log("Uso: buscar <termo>")
            return
        try:
            url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(termo)}"
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                log(f"Não encontrei resumo para: {termo}")
                return
            data = resp.json()
            title = data.get("title", termo)
            extract = data.get("extract", "(sem resumo)")
            print(f"🔎 {title}\n{extract}\n")
        except Exception as e:
            log(f"Erro ao buscar '{termo}': {e}")

    # Comando: ajuda
    def cmd_ajuda(self, _: str):
        print(
            "📖 Comandos disponíveis:\n"
            "  hora                 → mostra a hora atual\n"
            "  buscar <termo>       → resumo da Wikipédia (pt)\n"
            "  ajuda                → mostra esta ajuda\n"
            "  sair                 → encerra o agente\n"
        )

    # Comando: sair
    def cmd_sair(self, _: str):
        self._running = False
        log("Até mais! 👋")
