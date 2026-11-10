# Calibrated Forecast Pool

`CalibratedForecastPool` runs one frozen yes/no forecasting question per deployment. Forecasters commit address-, question-, and contract-bound hashes of sealed probabilities, recording equal synthetic stakes, then reveal during the frozen window. GenLayer resolves only the literal frozen-source criterion. Deterministic integer Brier scores divide the entire pot, including unrevealed stakes, with a published dust rule.

This is an independent, bounded demo-unit ledger, following specification-bid-auction. A stake records nominal synthetic units; no wallet balance is debited. Withdrawals record paid/refunded units and return a number; they do not transfer native value or tokens. There is no real asset custody or payment integration.

## Toolchain

The first source line pins exactly the auction's working runner:
`py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`.
Use the existing portfolio Python 3.14.2 environment without upgrading it. `requirements.txt` matches the auction's direct-test pins: `genlayer-test==0.30.0rc2`, `genlayer-py==0.19.0rc2`, `genvm-linter==0.11.1rc2`, `pytest==9.1.1`.

From this directory, run lint before tests:

```powershell
$env:GENVM_VERSION = 'v0.6.0-rc5'
..\.venv\Scripts\python.exe -B -c 'from genvm_linter.cli import cli; cli()' check contracts/calibrated_forecast_pool.py --json
..\.venv\Scripts\python.exe -B -m pytest -vv -p no:cacheprovider --tb=short
```

`verification/run_checks.py` runs those gates in order, extracts `contracts/abi.json`, and saves exact commands, output, tool versions and JUnit results. It pins the already cached GenVM artifact bundle to `v0.6.0-rc5`, matching the auction's direct-test SDK, to avoid automatic artifact updates. Use `..\.venv\Scripts\python.exe -B verification/run_checks.py` to reproduce it. These tests mock web and model calls, explicitly exercise the captured validator callback, and simulate a consensus failure. They do not prove live consensus or finality.

Any future StudioNet runtime calls must use a separate existing environment pinned to `genlayer-py==0.18.0` (`requirements-studionet.txt`), rather than the direct-test environment. The authorized StudioNet demos used the installed global Python runtime with `genlayer-py==0.18.0`; exact execution details are in the live release manifest.

## Lifecycle

1. The question owner deploys with a question ID, question, literal resolution criterion, 1–3 source URLs, exact stake units and four strictly ordered deadlines: commit, reveal, resolve-after and resolution deadline. No edit or ownership bypass exists.
2. Each forecaster computes a commitment privately using canonical JSON and SHA-256 as described in [DESIGN.md](docs/DESIGN.md), then calls `commit_forecast(hash, stake_units)` once before the commit deadline. The helper `get_commitment_hash` is a view, intended for local/off-chain use; do not submit a probability or salt as a public write before reveal.
3. After the commit deadline and through the reveal deadline, the same sender calls `reveal_forecast(probability_bps, salt)`. Probabilities are integers 0–10,000.
4. After the resolve-after time and through the resolution deadline, anyone calls `resolve_question()`. Every source must be fetched successfully. Source records bind original/kept byte counts, retained UTF-8 text, availability, status and digest into the judged result. Only retained text reaches the model. Quotes must be case-sensitive substrings of retained source text after collapsing whitespace on both sides, with at least eight normalized characters. Missing, invented or too-short quotes force UNRESOLVABLE. Fetch, parsing and consensus failures revert without changing state and permit retry through the resolution deadline. After that deadline, anyone may call `expire_unresolved()` to record terminal UNRESOLVABLE with reason `RESOLUTION_DEADLINE`, empty sources/quotes and full refunds via `settle()`.
5. Anyone calls `settle()`. YES/NO uses integer scores and the entire pot. UNRESOLVABLE, no reveals, or zero total score refunds every stake. Resolution is terminal, including UNRESOLVABLE.
6. Each forecaster calls `withdraw()` once for their own allocation, including a zero allocation. `get_accounting()` exposes stakes in, payouts, refunds and held units throughout.

## API

The constructor has nine parameters, including `resolution_deadline_iso` strictly after `resolve_after_iso`; see [examples/constructor.json](examples/constructor.json). Writes are `commit_forecast`, `reveal_forecast`, `resolve_question`, `expire_unresolved`, `settle`, and `withdraw`. Views are `get_commitment_hash`, `get_question`, `get_forecast`, `get_decision`, `get_sources`, `get_settlement`, and `get_accounting`. See the generated [ABI](contracts/abi.json).

## Documentation and limitations

- [Design, exact scoring example and auction deviation](docs/DESIGN.md)
- [Test matrix and per-case results](docs/TEST_MATRIX.md)
- [Local distinctiveness comparison](docs/DISTINCTIVENESS.md)
- [StudioNet demo proposal and anonymous source checks](docs/DEMO_PLAN.md)
- [Security notes](docs/SECURITY_NOTES.md)
- [Local example sequence](examples/demo_sequence.md)
- [StudioNet live demo results](docs/LIVE_DEMO.md)
- [StudioNet release manifest and receipts](deployments/studionet-release-2026-11-10.json)
- [Historical local-build manifest](deployments/local-only.json)

Two StudioNet instances were deployed from exact source commit `6cc6b4f`: the scoring demo paid 172/128/0, and the deadline-expiry demo refunded both revealed/unrevealed stakes. All 24 transactions finalized with 20 successes and four expected rollbacks. See the live evidence above. The repository remains local; nothing was pushed or submitted to the Portal. Literal entailment remains the nondeterministic judgment; quotation membership checks cannot independently prove that a quote establishes a criterion. Brier scores are proper as a standalone scoring rule; normalizing them into shares of a rival-dependent pot does not establish truthful-reporting incentives. See DESIGN.md for this economic limitation.
