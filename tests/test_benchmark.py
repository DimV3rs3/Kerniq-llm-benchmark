"""Benchmark matches the folder-tool plugins. Its command is configurable, not offered to the model."""

from __future__ import annotations

import asyncio
from pathlib import Path

from Kerniq.plugins.base import PluginContext
from Kerniq.plugins.manager import PluginManager
from Kerniq.tools.registry import ToolRegistry


def test_benchmark_discovers_without_exposing_the_tool():
    plugins_root = Path(__file__).resolve().parents[2]
    registry = ToolRegistry()
    manager = PluginManager(
        lambda: PluginContext(logger=None, config=None, event_bus=None, tool_registry=registry)
    )

    async def run():
        await manager.discover_and_load(plugins_root)
        return manager.plugins.get("llm-benchmark")

    plugin = asyncio.run(run())
    assert plugin is not None
    slots = {(row.get("slot"), row.get("id")) for row in plugin.contributions()}
    assert ("settings", "benchmark") in slots
    assert ("panel", "benchmark") not in slots
    tool = registry.get_tool("benchmark_run")
    assert tool is not None
    assert tool.agent_visible is False
    assert all(item.name != "benchmark_run" for item in registry.agent_tools())
