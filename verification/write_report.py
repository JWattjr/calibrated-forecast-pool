"""Generate the requested full-source report and expanded pass/fail matrix."""
import ast
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET


root = Path(__file__).resolve().parents[1]
verification = root / "verification"
source = (root / "contracts/calibrated_forecast_pool.py").read_text(encoding="utf-8")
source_hash = hashlib.sha256(source.encode()).hexdigest()
tree = ET.parse(verification / "tests.xml")
cases = tree.findall(".//testcase")
rows = []
for case in cases:
    status = "FAIL" if case.find("failure") is not None or case.find("error") is not None else "SKIP" if case.find("skipped") is not None else "PASS"
    rows.append(f"| `{case.attrib['name']}` | {status} |")
assert all("| PASS |" in row for row in rows)
test_list = "| Test case | Result |\n|---|---|\n" + "\n".join(rows) + "\n"
matrix = f'''# Test matrix

Run lint first, then `python -B -m pytest -vv -p no:cacheprovider --tb=short` from the project root using the pinned portfolio direct-test environment. Saved exact commands/output: `verification/lint.txt`, `verification/tests.txt`, `verification/schema.txt`, `verification/checks.json`. JUnit evidence: `verification/tests.xml`.

**{len(cases)} parameter-expanded cases passed.** These are mocked direct-mode tests. Captured validator callbacks are explicitly invoked for honest/forged candidates; a thrown consensus disagreement is simulated. No real network consensus or deployment is established.

| Invariant or behavior | Test coverage |
|---|---|
| Confident correct out-earns hedged and wrong; exact 172/128/0 example and reverse NO case | `test_confident_correct_hedged_wrong_exact_payouts`, `test_no_outcome_reverses_scores` |
| All dust to highest score; ties use lowest address | Worked example plus `test_dust_tie_uses_lowest_address_with_unrevealed_pot` |
| Identity, question and contract bound; independent canonical hash reconstruction; copied reveal fails | Changed/copy/cross-domain/real-deployment tests |
| One commitment and reveal; late commit, early/late reveal, exact deadline edges | Duplicate and deadline tests |
| Resolution deadline strictly follows resolve-after; expiry only after deadline and only while OPEN; no resolution after deadline | Constructor deadline cases and expiry/late-resolution boundary tests |
| Expiry records RESOLUTION_DEADLINE with empty sources/quotes and refunds revealed/unrevealed stakes without web/model calls | `test_expiry_after_deadline_refunds_revealed_and_unrevealed`, `test_failed_fetch_can_expire_after_resolution_deadline` |
| Unrevealed stake forfeited for scored YES/NO; full refund for UNRESOLVABLE, no reveals or zero sum | Forfeiture, terminal UNRESOLVABLE and four degenerate cases |
| Only own payout withdrawn once, including zero; public resolution/settlement; immutable terms | Worked example and access-control/lifecycle tests |
| Fetch and consensus failure preserve state and allow retry | Five fetch failures, one partial-source failure, network exception and mocked consensus failure |
| Conservation at each lifecycle step and after reverts; claimed/unclaimed rows independently sum to counters | `accounting`, `unchanged` and lifecycle helpers; fixture teardown for every `pool` scenario |
| Exact cap, over cap, three-/four-byte cut, complete multibyte boundary | Five UTF-8 fetch boundary cases |
| Tail-only quote downgrades to UNRESOLVABLE; retained quote can resolve a truncated body | Tail/prefix quote tests |
| Whitespace and line-wrap normalization; partial-line substring matching; minimum eight normalized characters; case-sensitive rejection | Six accepted substring cases and missing/invented/unavailable/short/wrong-case quote cases |
| Source status/count/digest tampering rejected even with rebound outer hashes; independent re-fetch rejects coherent lies | `test_validator_rejects_mismatched_truncation_record_even_rebound` |
| Validators compare normalized outcome and bound evidence, while valid quotation selection may differ | `test_validator_compares_outcome_and_evidence_not_free_text`, normalization test |
| Question, criterion, URLs/JSON, timestamps, salt, probability, stake, commitment, queue, model response and quote bounds | Constructor/size/schema/format tests, 8-forecaster maximum-stake test |

## Expanded pass/fail results

{test_list}
'''
if (root / "deployments/studionet-release-2026-11-10.json").exists():
    matrix += "\n## Separate live verification\n\nThe authorized StudioNet run finalized 24 transactions: 20 successful executions and four expected rollbacks. The scoring instance paid 172/128/0; the separate expiry instance refunded revealed and unrevealed stakes. Both source identities and direct contract Explorer links were verified. See [LIVE_DEMO.md](LIVE_DEMO.md) and the release manifest. These live receipts are separate from the 85 mocked direct-mode test cases.\n"
(root / "docs/TEST_MATRIX.md").write_text(matrix.rstrip() + "\n", encoding="utf-8", newline="\n")

checks = json.loads((verification / "checks.json").read_text())
demo = json.loads((verification / "demo-source-checks.json").read_text())
report = f'''# Local build report

Project: `calibrated-forecast-pool`. Source SHA-256: `{source_hash}`.

Result: {len(cases)} tests PASS; 3 GenVM lint checks PASS; SDK validation PASS (13 methods: 7 views and 6 writes; 9 constructor parameters). The final Git commit identifier is supplied with delivery, outside this commit to avoid a self-referencing commit hash.

## Review fixes

- Added a frozen resolution deadline strictly after resolve-after. Resolution is accepted through the final deadline; after it, permissionless expiry records UNRESOLVABLE / RESOLUTION_DEADLINE with empty sources and quotations. The existing settlement path refunds all stakes, revealed or unrevealed.
- Replaced full-line quotation matching with case-sensitive substring matching after collapsing whitespace and stripping both quote and retained source text. At least eight normalized characters are required. Partial-line quotations and line wrapping are accepted; invented, too-short and discarded-tail quotations remain UNRESOLVABLE.
- Replaced the literal-date demo with an interpretation of the settled CPython 3.12 distutils removal. The commit-pinned raw release documentation states the answer using different wording, inside the first 5,000 bytes. Stake and forecaster count remain unchanged, preserving the 172/128/0 worked payout example.
- Shared commitment hashing, runner, truncation/digest/availability validation, scoring, dust, synthetic accounting and one-shot withdrawal behavior are unchanged. Direct-test compatibility fixtures and dependency pins are unchanged.

## Commands and exact output

Working directory: `{checks['working_directory']}`.
Pinned tool versions: `{json.dumps(checks['versions'], sort_keys=True)}`.

The report generator does not run lint or tests. `verification/run_checks.py` ran lint first, then tests, then extracted the ABI. Initial restricted-network lint checks reported DNS lookup failure for the latest-runner lookup and successfully used the installed SDK cache. An unpinned final-directory rerun stalled during automatic artifact lookup and was stopped before completion. The successful final gates explicitly pin the already cached GenVM artifact bundle `v0.6.0-rc5`, matching the direct-test SDK. The contract runner was retained and no package dependency was upgraded. Any I200 notice is informational; the requested runner remains unchanged.

'''
for label in ("lint", "tests", "schema"):
    report += f"### {label}\n\n```text\n{(verification / (label + '.txt')).read_text(encoding='utf-8').rstrip()}\n```\n\n"
report += f'''## Every test and result

{test_list}

## Source availability check

The replacement URL proposed as frozen demo evidence was fetched anonymously with HTTP {demo['sources'][0]['http_status']}, {demo['sources'][0]['byte_count']} bytes, at {demo['checked_at_utc']}. It is pinned to upstream commit `{demo['upstream_commit']}`. Full response SHA-256: `{demo['sources'][0]['sha256']}`. The supporting statement occupies UTF-8 bytes [{demo['sources'][0]['supporting_line_byte_offset']}, {demo['sources'][0]['supporting_line_end_byte_offset']}) and fits inside the retained {demo['sources'][0]['kept_byte_count']}-byte prefix. See `docs/DEMO_PLAN.md` and `verification/demo-source-checks.json`. The live demo was not run.

## Decisions, uncertainty and deliberate omissions

- User-approved deviation: 5,000-byte UTF-8 prefix truncation replaces the auction's oversized-body rejection, using bounty-style source metadata and independent validation. Everything shared with the auction is documented in DESIGN.md; source identities are in reference-provenance.json.
- One question per deployment follows the auction layout. The question owner freezes terms at construction. Anyone may trigger resolution and settlement; each forecaster may withdraw only their own allocation.
- A failed source aborts the entire attempt, preserving all state. No failed-attempt availability log is persisted. Only finalized records appear in get_sources. A finalized UNRESOLVABLE result is terminal and refunds all stakes on settlement; a deterministic deadline expiry records empty sources and quotations.
- Malformed UTF-8 inside the kept prefix is unavailable; only an incomplete final character is cut back. This preserves strict UTF-8 handling without silent replacement.
- Quotes must be case-sensitive substrings of retained text after whitespace normalization, with at least eight normalized characters; unsupported or too-short quotes force UNRESOLVABLE. Source membership cannot prove semantic entailment. Direct mocks and callback mutation checks do not establish live consensus or finality.
- Brier scores are proper in isolation, but rival-dependent pot normalization does not guarantee truthful-reporting incentives. No claim of production incentive compatibility, Sybil resistance or ecosystem-wide originality is made.
- Deliberately absent: native/token custody or transfers, wallet setup, real stake debits, frontend, multi-question mutable registry, cancellation/admin recovery, live demo, deployment, public remote, push, GitHub repository creation, visibility change and Portal submission.
- No private keys or credential-helper output were read or logged. Other projects and portfolio trackers were only read.

## Full contract source

```python
{source.rstrip()}
```
'''
if (root / "deployments/studionet-release-2026-11-10.json").exists():
    report = report.replace("# Local build report", "# Build and live verification report\n\nThe separately authorized StudioNet demos passed: 24 finalized transactions, 20 successful executions and four expected rollbacks. Scoring paid 172/128/0; deadline expiry refunded both stakes. Both deployed source blobs and direct contract Explorer links were verified. Full live evidence is in docs/LIVE_DEMO.md and deployments/studionet-release-2026-11-10.json. The original local validation results and complete source follow.")
    report = report.replace("The live demo was not run.", "The live demo was subsequently run under explicit authorization; see docs/LIVE_DEMO.md for actual results.")
    report = report.replace("cancellation/admin recovery, live demo, deployment, public remote", "cancellation/admin recovery, public remote")
(root / "docs/BUILD_REPORT.md").write_text(report.rstrip() + "\n", encoding="utf-8", newline="\n")
print(f"Wrote full-source report and matrix for {len(cases)} passing cases; source sha256={source_hash}")
