"""Configurable LLM provider registry (local/demo implementations)."""

from __future__ import annotations

from collections.abc import Callable


def provider_echo(query: str, contexts: list[str], config: dict) -> str:
    if not contexts:
        return "I could not find relevant context for your question."
    context = "\n".join(f"- {chunk}" for chunk in contexts[:3])
    return f"Answer based on retrieved context for '{query}':\n{context}"


def provider_template(query: str, contexts: list[str], config: dict) -> str:
    template = config.get("template", "Q: {query}\nContext:\n{context}\nA: {answer_hint}")
    context = "\n".join(f"- {chunk}" for chunk in contexts[:3]) if contexts else "- no context"
    return template.format(query=query, context=context, answer_hint="Use retrieved facts only.")


def provider_extractive(query: str, contexts: list[str], config: dict) -> str:
    del query, config
    return contexts[0] if contexts else "No answer found in retrieved chunks."


PROVIDERS: dict[str, Callable[[str, list[str], dict], str]] = {
    "echo": provider_echo,
    "template": provider_template,
    "extractive": provider_extractive,
}
