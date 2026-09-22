from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


@dataclass
class Memory:
    facts: list[str] = field(default_factory=list)
    log: list[dict] = field(default_factory=list)
    path: Path = field(default_factory=lambda: Path.home() / ".aether" / "memory.json")

    def load(self) -> None:
        if self.path.exists():
            data = json.loads(self.path.read_text())
            self.facts = data.get("facts", [])
            self.log = data.get("log", [])

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({"facts": self.facts, "log": self.log[-200:]}, indent=2))

    def remember(self, fact: str) -> None:
        self.facts.append(fact)
        self.save()

    def note(self, role: str, text: str) -> None:
        self.log.append({"t": datetime.now(timezone.utc).isoformat(), "role": role, "text": text})
        self.save()


class Aether:
    """The OS you talk to. Linux still runs underneath."""

    name = "Aether"

    def __init__(self) -> None:
        self.memory = Memory()
        self.memory.load()
        self.tools: dict[str, Callable[[str], str]] = {
            "help": self._help,
            "who": self._who,
            "remember": self._remember,
            "facts": self._facts,
            "ls": self._ls,
            "ps": self._ps,
            "uname": self._uname,
            "plan": self._plan,
            "sh": self._sh,
        }

    def reply(self, line: str) -> str:
        line = line.strip()
        self.memory.note("you", line)
        if not line:
            return ""
        cmd, _, rest = line.partition(" ")
        cmd = cmd.lower()
        if cmd in self.tools:
            out = self.tools[cmd](rest.strip())
        else:
            out = self._think(line)
        self.memory.note("aether", out)
        return out

    def _help(self, _: str) -> str:
        return (
            "Aether commands:\n"
            "  who          what this OS is\n"
            "  remember X   persist a fact\n"
            "  facts        list memory\n"
            "  ls [path]    list files (host)\n"
            "  ps           processes\n"
            "  uname        kernel still underneath\n"
            "  plan         replacement roadmap\n"
            "  sh <cmd>     run a host command (lab only)\n"
        )

    def _who(self, _: str) -> str:
        return (
            f"I am {self.name}. I am the operating system you talk to. "
            "Linux still owns hardware. I own intent, memory, and policy. "
            f"I remember {len(self.memory.facts)} facts."
        )

    def _remember(self, fact: str) -> str:
        if not fact:
            return "remember what?"
        self.memory.remember(fact)
        return f"kept: {fact}"

    def _facts(self, _: str) -> str:
        if not self.memory.facts:
            return "empty memory"
        return "\n".join(f"- {f}" for f in self.memory.facts)

    def _ls(self, path: str) -> str:
        p = Path(path or ".")
        try:
            names = sorted(os.listdir(p))[:80]
        except OSError as e:
            return str(e)
        return "\n".join(names) or "(empty)"

    def _ps(self, _: str) -> str:
        try:
            out = subprocess.check_output(["ps", "-o", "pid,comm"], text=True)
        except Exception as e:
            return str(e)
        return "\n".join(out.splitlines()[:40])

    def _uname(self, _: str) -> str:
        return os.uname().sysname + " " + os.uname().release + " — still Linux. Aether is above it."

    def _plan(self, _: str) -> str:
        return (
            "1. You talk only to Aether (done when this REPL is your shell).\n"
            "2. Push Aether into a rooted AVD as a daemon.\n"
            "3. Replace launcher / adb shell with Aether.\n"
            "4. Optional: KernelSU / eBPF policy.\n"
            "5. Do not delete the kernel."
        )

    def _sh(self, cmd: str) -> str:
        if not cmd:
            return "sh <command>"
        try:
            out = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT, timeout=15)
        except subprocess.CalledProcessError as e:
            return e.output or str(e)
        except Exception as e:
            return str(e)
        return out[-4000:] or "(ok)"

    def _think(self, line: str) -> str:
        low = line.lower()
        if "linux" in low and ("replace" in low or "delete" in low):
            return self._plan("")
        if any(w in low for w in ("who are you", "what are you", "what is this")):
            return self._who("")
        return (
            f"heard: {line}\n"
            "I am a small kernel. Use `help`. For a real model, wire an API later; "
            "the OS contract stays the same."
        )
