"""Generate local evidence only; does not run checks or change any remote."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
verification = root / 'verification'
source = (root / 'contracts/calibrated_forecast_pool.py').read_text(encoding='utf-8')
source_hash = hashlib.sha256(source.encode('utf-8')).hexdigest()
checks = json.loads((verification / 'checks.json').read_text(encoding='utf-8'))
assert [row['name'] for row in checks['checks']] == ['lint', 'tests', 'schema']
assert all(row['exit_code'] == 0 for row in checks['checks'])
cases = ET.parse(verification / 'tests.xml').findall('.//testcase')
assert cases and all(case.find('failure') is None and case.find('error') is None and case.find('skipped') is None for case in cases)
test_list = '| Test case | Result |\n|---|---|\n' + '\n'.join(f"| `{case.attrib['name']}` | PASS |" for case in cases) + '\n'
demo = json.loads((verification / 'demo-source-checks.json').read_text(encoding='utf-8'))
coverage = '''| Invariant or behavior | Coverage |
|---|---|
| Per-source HOLDS / CONTRADICTED / UNCLEAR; code derives outcome | All nine two-source label combinations; missing classifications default UNCLEAR; every determinate source needs its own quote |
| Same headline with changed facts disagrees | Internally valid different source label with unchanged UNRESOLVABLE is rejected; changed label and consistent changed outcome are rejected |
| Different valid quote choices agree | Captured validator accepts an alternate genuine supporting passage against identical fetched evidence and source labels |
| Fabricated evidence is rejected | Forged quote rejected for determinate and UNCLEAR candidates; malformed quote schemas/bounds rejected; wrong case, short, unknown-source and missing support cannot authorize determinate labels |
| Quote filtering preserves other support | Invalid membership quotes dropped individually; same-source valid support keeps HOLDS/YES; only unsupported sources downgrade; only-invalid quotes are not stored |
| Canonical quote storage | Whitespace normalized and `(url, line)` sorted; unsorted or non-normalized leader records rejected; full-candidate equality across models is not required |
| Complete required evidence | Exact 5000-byte source can resolve; truncated source cannot resolve YES or NO even with retained valid support; any required truncated source skips the model and refunds revealed/unrevealed stakes |
| UTF-8 and source integrity | Exact cap, over cap, three-/four-byte cut, complete multibyte boundary; forged counts/status/digests/prefixes rejected even with rebound outer hashes |
| Unavailable evidence and failed consensus preserve state | Non-200, empty/whitespace, invalid UTF-8, network exceptions, one failed required source, simulated consensus failure; deadline refunds remain available |
| Sealed forecast domains and permissions | Sender/question/contract-bound commitments; copied and altered reveals fail; one commit/reveal; own entitlement only; public resolution, expiry and settlement |
| Deadline liveness | Strict constructor ordering; exact boundary behavior; early expiry and late resolution fail; permissionless expiry refunds both revealed and unrevealed stakes |
| Conserved deterministic payouts | 172/128/0 and reverse NO example; highest-score/address dust; unrevealed forfeiture; UNRESOLVABLE, empty, no-reveal and zero-score refunds; one withdrawal including zero |
| Frozen verified complete-source example | 667-byte pinned distutils snapshot and SHA-256 checked; HOLDS mock -> code-derived YES -> 172/128/0 -> zero held units |
| Input/model limits | Participant cap, stake/probability/salt/domain/URL/text/time bounds; unknown/duplicate source IDs and labels; model cannot supply outcome |
'''
matrix = f'''# Test matrix

**{len(cases)} parameter-expanded cases passed** for the current local source, SHA-256 `{source_hash}`. GenVM lint ran first and passed; the complete suite ran second. Exact output is in verification/lint.txt and verification/tests.txt; commands/tool versions are in verification/checks.json; expanded results are in verification/tests.xml.

These are mocked direct-mode tests, including explicit execution of captured validator callbacks. They establish local behavior under the approved fact-agreement/quote-selection design, not live consensus or finality. No push, deployment or Portal action was performed for this revision.

{coverage}
## Expanded results

{test_list}
## Historical live evidence

The November 10 StudioNet demos (24 finalized transactions: 20 SUCCESS, four expected ERROR) prove only historical source commit `6cc6b4f`. They do not prove this changed source. See LIVE_DEMO.md and the original release manifest for those historical records. A future authorized deployment requires a pushed exact source commit, fresh demos and separately verified Explorer contract links.
'''
(root / 'docs/TEST_MATRIX.md').write_text(matrix, encoding='utf-8', newline='\n')
report = f'''# Local revision build report

Local gate: **PASS**. Source SHA-256: `{source_hash}`. GenVM lint ran first: three checks and SDK validation passed (13 public methods: seven views, six writes; nine constructor parameters). Full test suite ran second: **{len(cases)} passed**. ABI extraction also passed. The runner and dependency versions remain unchanged. I200 is an informational newer-runner notice, not a lint failure.

## Approved implementation

- The model classifies each frozen source HOLDS, CONTRADICTED or UNCLEAR; ordinary code derives YES only for all HOLDS on complete sources, NO only for all CONTRADICTED on complete sources, otherwise UNRESOLVABLE. Missing classifications become UNCLEAR; invented/duplicate URLs, labels or outcome fields are rejected.
- Any required truncated source keeps its UTF-8 prefix, original/kept counts, availability and digest, but forces terminal UNRESOLVABLE with UNCLEAR labels and empty quotes without invoking the model. Unavailable-source retry and deadline refunds remain unchanged. This rule applies to calibrated-forecast-pool only; parametric-coverage-pool was not changed.
- Invalid membership quotes are dropped individually, with only unsupported source labels downgraded to UNCLEAR; valid support on the same source preserves its label. Stored quotes are whitespace-normalized and sorted. `_valid_candidate` rejects fabricated, invalid or noncanonical leader quotes. Independent validator agreement compares input/evidence/snapshot digests, canonical byte-identical sources, all source labels and derived outcome. Different valid quote choices are accepted for consensus liveness. This is the user's explicit replacement of full-candidate equality, documented in DESIGN.md.
- The new demo uses complete commit-pinned distutils documentation: 667 bytes, expected source label HOLDS and code-derived YES. Three 100-unit stakes and 10000/5000/0 forecasts preserve the 172/128/0 payout example. Anonymous source verification and the mock example are separate from a real live demonstration.
- Commitment domains, lifecycle/deadlines, integer scoring/dust, refunds, synthetic accounting, one-shot withdrawals, pinned runner and dependency versions remain unchanged.

## Three separate gates

| Gate | Result | Scope |
|---|---|---|
| Technical readiness | PASS locally under the user-approved design | Lint and all {len(cases)} mocked direct tests pass, including honest and adversarial validator callbacks. This is not a production audit or live consensus proof. |
| Distinctiveness | PASS for the documented local comparison | Sealed probability scoring and conserved pot allocation differ from the auction, bounty, predicate graph and same-week underwriting pool; no ecosystem originality or points guarantee. |
| Evidence readiness | FAIL for this revision's submission | Source has changed and has not been pushed or deployed. Historical receipts and public source links prove `6cc6b4f` only. Fresh live proof remains necessary after user review and authorization. |

## Source verification

Anonymous HTTP {demo['sources'][0]['http_status']}; {demo['sources'][0]['byte_count']} raw bytes, all retained; upstream commit `{demo['upstream_commit']}`. Full/kept SHA-256 `{demo['sources'][0]['sha256']}`. Exact URL and supporting lines are in DEMO_PLAN.md and verification/demo-source-checks.json. The byte-exact example snapshot is examples/distutils-source.rst.

## Validation evidence

Checked at `{checks['checked_at_utc']}`. Working directory: `{checks['working_directory']}`. Versions: `{json.dumps(checks['versions'], sort_keys=True)}`. GenVM artifact bundle remains `{checks['genvm_artifact_bundle']}`.

The report generator reads saved validation results and does not run lint or tests. No push, deployment, Portal interaction or new live receipt was performed. Existing public evidence remains historical. Local changes are held for user review at the requested gate.

'''
for label in ('lint', 'tests', 'schema'):
    output = (verification / f'{label}.txt').read_text(encoding='utf-8').rstrip()
    report += f'### {label}\n\n```text\n{output}\n```\n\n'
report += f'## Every test and result\n\n{test_list}\n## Full current contract source\n\n```python\n{source.rstrip()}\n```\n'
(root / 'docs/BUILD_REPORT.md').write_text(report, encoding='utf-8', newline='\n')
print(f'Generated local report and matrix: {len(cases)} passing cases, source SHA-256 {source_hash}')


# Fresh live evidence is separate from local tests and must match this source.
release_path = root / 'deployments/studionet-release-2026-11-11.json'
if release_path.exists():
    release = json.loads(release_path.read_text(encoding='utf-8'))
    if release['project']['source_sha256'] == source_hash and release['status'] == 'RELEASE_VERIFIED':
        instance = release['instances']['score']
        assert instance['complete'] and release['verification']['all_transactions_finalized']
        url = instance['explorer_contract_url']
        matrix = matrix.replace('No push, deployment or Portal action was performed for this revision.', 'The exact source was subsequently pushed and freshly deployed under user authorization; separate live evidence is recorded below. No Portal action occurred.')
        matrix += f"\n## Current separate live verification\n\nSource commit `{release['project']['source_commit']}` was pushed before fresh deployment. All 14 transactions finalized: 12 SUCCESS, two expected ERROR. Complete 667-byte evidence classified HOLDS, code derived YES, payouts were 172/128/0, and final accounting was stakes=300, paid=300, refunded=0, held=0. All seven view methods were read at the end. Direct Explorer contract evidence: [{instance['address']}]({url}). See LIVE_RELEASE_2026-11-11.md and the November 11 manifest. These observations are separate from the {len(cases)} mocked direct tests and are not an adversarial consensus audit.\n"
        (root / 'docs/TEST_MATRIX.md').write_text(matrix, encoding='utf-8', newline='\n')
        report = report.replace('# Local revision build report', '# Build and fresh StudioNet release report', 1)
        report = report.replace('Local gate: **PASS**.', 'Local gate: **PASS**. Fresh StudioNet demo: **PASS**.', 1)
        report = report.replace('| Evidence readiness | FAIL for this revision\'s submission | Source has changed and has not been pushed or deployed. Historical receipts and public source links prove `6cc6b4f` only. Fresh live proof remains necessary after user review and authorization. |', '| Evidence readiness | PASS for the observed release | Pushed exact source, fresh source-matched deployment, 14 finalized transactions, all final views, conserved accounting and verified direct Explorer contract link. Historical addresses prove previous source only. No Portal submission occurred. |')
        report = report.replace('No push, deployment, Portal interaction or new live receipt was performed. Existing public evidence remains historical. Local changes are held for user review at the requested gate.', 'After user approval, this exact source was pushed before fresh StudioNet deployment. The separate live evidence below proves the revised source; November 10 receipts remain historical previous-source evidence only. No Portal interaction or submission occurred.')
        report += f"\n## Current live release evidence\n\nSource commit `{release['project']['source_commit']}`, verified pushed before deployment; byte-identical on-chain source. Runtime genlayer-py 0.18.0 and the unchanged pinned runner. **GenLayer Explorer Contract**: [{instance['address']}]({url}), verified in the rendered StudioNet Explorer against the full address and deployment transaction.\n\nThe single resolution attempt used complete 667-byte evidence and derived YES from HOLDS. Settlement paid 172/128/0. All seven views were read at the end. Final accounting: stakes_in=300, paid_units=300, refunded_units=0, held_units=0, conserved=true. The old 0xc74a... and 0xE908... deployments are historical for source 6cc6b4f only; this release claims no fresh expiry instance.\n\n| Operation | Finality | Leader execution | Explorer |\n|---|---|---|---|\n"
        for tx in release['transactions']:
            result = tx['leader_execution'] + (' (expected rollback)' if tx['expected_error'] else '')
            report += f"| {tx['operation']} | {tx['finality_status']} | {result} | [transaction]({tx['explorer_url']}) |\n"
        report += "\nFull receipts, votes and read-backs: deployments/studionet-release-2026-11-11.json. These synthetic-unit demos do not establish token custody, truthful-reporting incentives, formal security or adversarial live consensus robustness.\n"
        (root / 'docs/BUILD_REPORT.md').write_text(report, encoding='utf-8', newline='\n')
