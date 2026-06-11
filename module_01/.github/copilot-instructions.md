<!--
Guidance for GitHub Copilot / AI coding agents working in this repository.
Keep this file concise and focused on discoverable, project-specific patterns.
-->
# Copilot instructions for Module 1 (AI Agents — Logistics)

Quick context
- This folder contains teaching materials for Module 1: building agent-callable functions for Innovate Logistics. Key folders: `screencasts/`, `activities/`, `solutions/`.

What to prioritize
- Preserve the educational patterns: the "What-Why-How" comment style, explicit type hints, and standardized return contract used by functions.
- Prefer minimal, well-tested changes: update `activities/*` starter files only when asked; prefer `solutions/*` examples when reproducing patterns.

Key project conventions (do not deviate)
- Standardized return: all agent-callable functions return the shape: `{"success": bool, "result": Any, "error": Optional[str], "error_type": Optional[str]}`. See `screencasts/1_1_shipping_tool.py` and `solutions/1_3_SOLUTION_logistics_tools.py`.
- Validation ordering: check parameter types first, then format, then business rules. See tests in `activities/1_3_START_function_tests.py` and `screencasts/1_1_test_shipping_tool.py`.
- Commenting: maintain the "What-Why-How" comment blocks every ~3-5 lines when editing instructor-facing code.
- Decorator usage: cross-cutting concerns (logging, error handling, timing) are implemented via the production decorator pattern. See `activities/1_7_START_production_wrapper.py` and `solutions/1_7_SOLUTION_logistics_tools.py`.

Developer workflows (explicit commands)
- Run the module test suites (from `module_01`):
```bash
cd module_01
pytest screencasts/1_1_test_shipping_tool.py -v
pytest activities/1_3_START_function_tests.py -v
pytest activities/1_7_START_test_logistics.py -v
```
- Run demos that require an API key (set `OPENAI_API_KEY` in your environment):
```bash
export OPENAI_API_KEY=your_key_here
python screencasts/1_9_demo_agent_integration.py
python solutions/1_10_SOLUTION_agent_integration.py
```

Files to inspect when implementing changes
- Function patterns & specs: `screencasts/1_1_shipping_spec.json`, `screencasts/1_1_shipping_tool.py`.
- Starter activity code: `activities/1_3_START_naive_tools.py`, `activities/1_3_START_function_tests.py`.
- Production decorator: `activities/1_7_START_production_wrapper.py`.
- Hardened activity implementation: `activities/logistics_tools.py` (applies `@production_agent_function`).

- Environment: `activities/.env` contains a placeholder `OPENAI_API_KEY` (do NOT commit real keys).
- Full solutions for reference: `solutions/1_3_SOLUTION_logistics_tools.py`, `solutions/1_7_SOLUTION_logistics_tools.py`, `solutions/1_10_SOLUTION_agent_integration.py`.

Integration points & dependencies
- OpenAI agent integration uses the Responses/Chat exemplar in `screencasts/1_9_demo_agent_integration.py` and `solutions/1_10_SOLUTION_agent_integration.py`.
- Tests assume `pytest` is installed. No other heavy dependencies are required for core exercises.

Behavioural rules for AI edits
- Make minimal, reversible changes. For exercises, do not overwrite `solutions/*` unless explicitly asked.
- Favor making edits in `activities/*` when producing starter code; run the provided test files after changes.
- Preserve file-level structure and educational comments; do not remove or shorten the "What-Why-How" blocks.

Examples (copyable patterns)
- Standard return on success:
```python
return {"success": True, "result": 3, "error": None}
```
- Validation error:
```python
return {"success": False, "result": None, "error": "SKU must be 3 letters followed by 4 digits", "error_type": "validation"}
```

If you need clarification
- Ask the repo owner which target to modify: `activities/` (starter) vs `solutions/` (reference). Prefer small PRs and include test changes with `pytest` runs.

End of file
