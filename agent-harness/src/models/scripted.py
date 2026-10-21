class ScriptedModel:
    """Modelo de simulação para rodar offline e testar o Harness."""
    def __init__(self, actions):
        self.actions = actions
        self.i = 0

    def decide(self, system, messages, tools):
        name, args = self.actions[min(self.i, len(self.actions) - 1)]
        self.i += 1
        return {"id": f"toolu_{self.i}", "name": name, "input": args}
