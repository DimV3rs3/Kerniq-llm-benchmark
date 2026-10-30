# LLM benchmark

Kerniq plugin. This folder is the whole plugin. It is not part of the Kerniq install. Publish this folder as its own repository. Kerniq loads it only after it is installed into `plugins/`.

Runs every chat model of the provider currently selected in Kerniq, one after another. Iterations, response timeout, temperature, max tokens, auto Plan/Act, and "build a plan" come from Kerniq's own settings. Only the task prompts and the analyzer prompts live in this plugin. If every task is empty, the first task is "Describe the workspace in five sentences. If it is empty, say so."

The command is `tools/` inside this folder. It loads with the plugin and is not an agent command. `manifest.toml` sets `expose_to_agent = false`. Run it from the Web UI, not by asking the model to call it.

The Web UI allows the slots `settings` and `panel`. This plugin uses only `settings`. You get a Benchmark item in settings. Open console there: the run log is a modal, not a separate window. Closing the page does not stop a run that already started.

Models are ordered by weight (LM Studio `size_bytes`, or an estimate from the parameter count), then by maximum context, then by name. A model stays loaded for the configured number of tasks (three by default). It is then unloaded. The next model is loaded only after the catalog confirms that nothing is still loaded, including a model the user had loaded.

Anonymous analyzers are drawn from that list after the lightest 10% and the heaviest 10% are removed. How many of them run is a gaussian draw around the middle of what remains. The final analyzer is the heaviest model with the largest context. There is no mock result if the provider does not answer.

## Output

```
workspace/benchmarks/<stamp>/<model>/slot-N/result.md
workspace/benchmarks/<stamp>/FULL_BENCHMARK_REPORT.md
workspace/benchmarks/<stamp>/analysis/anonymous-N.md
workspace/benchmarks/<stamp>/analysis/report.md
workspace/benchmarks/<stamp>/state.json
workspace/benchmarks/active.json
```

`key.json` maps output labels back to model names. The ranking text does not. `benchmarks/active.json` is the file the UI reads so you can leave the page and come back.
