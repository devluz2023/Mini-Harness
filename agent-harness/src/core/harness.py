import os
import sys
import json
import subprocess
from pathlib import Path
from src.core.exceptions import PermissionDenied
from src.tools.specs import TOOL_SPECS

class Harness:
    READ_ONLY = ("tests/", "AGENTS.md")

    def __init__(self, workspace, model, max_steps=8, max_output_chars=600, approve=None):
        self.ws = Path(workspace).resolve()
        self.model = model
        self.max_steps = max_steps
        self.max_output_chars = max_output_chars
        self.approve = approve or (lambda tool, args: True)
        self.steps = []

    def resolve(self, rel, write=False):
        path = (self.ws / rel).resolve()
        if path != self.ws and self.ws not in path.parents:
            raise PermissionDenied("path is outside the workspace")
        name = path.relative_to(self.ws).as_posix()
        if write and name.startswith(self.READ_ONLY):
            raise PermissionDenied(f"{name} is read-only")
        return path

    def clip(self, text):
        text = text.replace(str(self.ws), "<workspace>")
        extra = len(text) - self.max_output_chars
        if extra > 0:
            text = text[:self.max_output_chars] + f"\n...[{extra} more chars]"
        return text

    def list_files(self):
        files = [
            p.relative_to(self.ws).as_posix()
            for p in sorted(self.ws.rglob("*"))
            if p.is_file() and ".harness" not in p.parts and "__pycache__" not in p.parts
        ]
        return "\n".join(files)

    def read_file(self, path):
        return self.resolve(path).read_text()

    def write_file(self, path, content):
        target = self.resolve(path, write=True)
        if not self.approve("write_file", {"path": path}):
            raise PermissionDenied("a person declined this change")
        target.write_text(content)
        return f"wrote {path}"

    def run_tests(self):
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
            cwd=self.ws,
            capture_output=True,
            text=True,
            timeout=20,
            env={**os.environ, "PYTHONPATH": str(self.ws), "PYTHONDONTWRITEBYTECODE": "1"},
        )
        return proc.returncode == 0, proc.stdout + proc.stderr

    def execute(self, name, args):
        try:
            if name == "run_tests":
                return "ok", self.run_tests()[1]
            if name in ("list_files", "read_file", "write_file"):
                return "ok", getattr(self, name)(**args)
            return "error", f"unknown tool: {name}"
        except PermissionDenied as err:
            return "blocked", f"DENIED: {err}"
        except Exception as err:
            return "error", f"ERROR: {err}"

    def save_state(self, task, status):
        folder = self.ws / ".harness"
        folder.mkdir(exist_ok=True)
        (folder / "state.json").write_text(
            json.dumps({"task": task, "status": status, "steps": self.steps}, indent=2)
        )

    def log(self, step, text):
        print(f"[step {step}] {text}")

    def run(self, task):
        system = (
            "You are a coding agent in a small Python project. "
            "Use the tools to inspect, edit, and test. "
            "Call finish only when you are done.\n\n"
            + (self.ws / "AGENTS.md").read_text()
        )
        messages = [{"role": "user", "content": task}]

        for step in range(1, self.max_steps + 1):
            action = self.model.decide(system, messages, TOOL_SPECS)
            name, args = action["name"], action["input"]
            shown = json.dumps(args)
            self.log(step, f"model -> {name} {shown[:50]}")

            if name == "finish":
                passed, output = self.run_tests()
                if passed:
                    self.log(step, "check: tests pass, finish accepted")
                    self.steps.append({"step": step, "tool": name, "outcome": "accepted"})
                    self.save_state(task, "done")
                    return "done"
                outcome = "rejected"
                result = "REJECTED: tests still fail.\n" + self.clip(output)
                self.log(step, "check: tests FAIL, finish rejected")
            else:
                outcome, result = self.execute(name, args)
                result = self.clip(result)
                if outcome != "ok":
                    self.log(step, result[:60])

            self.steps.append({"step": step, "tool": name, "outcome": outcome})
            self.save_state(task, "running")

            messages.append({"role": "assistant", "content": [{"type": "tool_use", "id": action["id"], "name": name, "input": args}]})
            messages.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": action["id"], "content": result}]})

        self.log(self.max_steps, "step limit reached, stopping")
        self.save_state(task, "stopped: step limit")
        return "stopped: step limit"