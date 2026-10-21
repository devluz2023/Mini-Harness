import os

class ClaudeModel:
    """Adaptador para o LLM Real da Anthropic."""
    def __init__(self, model=None):
        import anthropic
        self.client = anthropic.Anthropic()
        self.model = model or os.environ.get("CLAUDE_MODEL", "claude-3-5-sonnet-latest")

    def decide(self, system, messages, tools):
        reply = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=system,
            tools=tools,
            tool_choice={"type": "auto", "disable_parallel_tool_use": True},
            messages=messages,
        )
        for block in reply.content:
            if block.type == "tool_use":
                return {"id": block.id, "name": block.name, "input": block.input}
        text = " ".join(b.text for b in reply.content if b.type == "text")
        return {"id": "no_tool", "name": "finish", "input": {"summary": text}}
