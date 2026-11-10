"""Run the pinned installed tools, lint first, preserving exact output and commands."""
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone


root = Path(__file__).resolve().parents[1]
out = root / "verification"
commands = [
    ("lint", [sys.executable, "-B", "-c", "from genvm_linter.cli import cli; cli()", "check", "contracts/calibrated_forecast_pool.py", "--json"]),
    ("tests", [sys.executable, "-B", "-m", "pytest", "-vv", "-p", "no:cacheprovider", "--tb=short", "--junitxml=verification/tests.xml"]),
    ("schema", [sys.executable, "-B", "-c", "from genvm_linter.cli import cli; cli()", "schema", "contracts/calibrated_forecast_pool.py", "--output", "contracts/abi.json"]),
]
results = []
check_env = os.environ.copy()
check_env["GENVM_VERSION"] = "v0.6.0-rc5"
for label, argv in commands:
    display = "$env:GENVM_VERSION = 'v0.6.0-rc5'\n& " + " ".join("'" + arg.replace("'", "''") + "'" for arg in argv)
    result = subprocess.run(argv, cwd=root, env=check_env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
    output = result.stdout + result.stderr
    (out / f"{label}.txt").write_text(display + "\n\n" + output, encoding="utf-8")
    print(display, flush=True)
    print(output, flush=True)
    results.append({"name": label, "argv": argv, "powershell_command": display, "exit_code": result.returncode})
    if result.returncode:
        raise SystemExit(result.returncode)
(out / "checks.json").write_text(json.dumps({
    "checked_at_utc": datetime.now(timezone.utc).isoformat(), "working_directory": str(root),
    "python_version": sys.version,
    "genvm_artifact_bundle": "v0.6.0-rc5 (already cached; matches direct-test SDK)",
    "versions": {name: importlib.metadata.version(name) for name in ("genlayer-test", "genlayer-py", "genvm-linter", "pytest")},
    "checks": results,
}, indent=2) + "\n", encoding="utf-8")
