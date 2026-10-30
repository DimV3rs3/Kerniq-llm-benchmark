"""Benchmark command. Loaded from this folder. Not offered to the model unless the manifest says so."""

from __future__ import annotations

import logging
from typing import Any, Dict

from Kerniq.interfaces.tools import Tool, ToolResult

logger = logging.getLogger(__name__)


class BenchmarkRunTool(Tool):
    """Starts a benchmark. The plugin owns the run; this tool only collects arguments."""

    def __init__(self, plugin: "PluginImpl") -> None:
        self._plugin = plugin

    @property
    def tool_id(self) -> str:
        return "benchmark_run"

    @property
    def name(self) -> str:
        return "benchmark_run"

    @property
    def description(self) -> str:
        return (
            "Benchmark every model of the selected provider on the same task, in sequence. "
            "Writes reports under the workspace benchmarks folder. "
            "Optional task overrides the plugin setting for this run only."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "Task override. Empty uses the plugin settings.",
                },
            },
        }

    @property
    def risk_level(self) -> str:
        return "medium"

    @property
    def category(self) -> str:
        return "benchmark"

    def settings_schema(self):
        from Kerniq.interfaces.settings_schema import SettingsSchema

        return SettingsSchema(
            component_id=self.tool_id,
            component_type="tool",
            title=self.name,
            fields=[],
        )

    @property
    def display_phrase(self) -> str:
        return "benchmarks"

    def plan_membership_default(self) -> bool:
        return False

    async def execute(self, arguments: Dict[str, Any], context: Any) -> ToolResult:
        call_id = str(arguments.get("tool_call_id") or "")
        override = str(arguments.get("task") or "").strip()
        try:
            report = await self._plugin.run_benchmark(context, task_override=override)
        except Exception as exc:
            logger.exception("benchmark failed")
            return ToolResult(
                tool_call_id=call_id,
                tool_id=self.tool_id,
                status="error",
                success=False,
                error=str(exc),
                human_readable=f"Benchmark failed: {exc}",
            )
        folder = str(report.get("folder") or "")
        lines = [f"Benchmark written to {folder}"]
        for row in report.get("runs") or []:
            lines.append(
                f"- {row.get('model')}: {row.get('status')} ({row.get('seconds')}s)"
            )
        return ToolResult(
            tool_call_id=call_id,
            tool_id=self.tool_id,
            status="success",
            output=report,
            human_readable="\n".join(lines),
        )


def create_tools(plugin):
    return [BenchmarkRunTool(plugin)]
