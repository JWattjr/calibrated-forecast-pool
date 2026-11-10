# Proposed StudioNet demo — not run

Status: proposal only. No deployment or runtime transaction was made. Dates in `examples/constructor.json` are local placeholders; choose ordered future deadlines before a separately authorized deployment and freeze them permanently. Use the existing separate StudioNet environment with `genlayer-py==0.18.0` for any future runtime call; direct tests require 0.19.0rc2.

## Settled question and criterion

Question: **Did CPython 3.12 stop including distutils in its standard library?**

Criterion: YES if the frozen CPython 3.12 release documentation explicitly establishes that distutils was removed from the standard library. NO if it explicitly establishes that distutils remained included in that release. Otherwise UNRESOLVABLE. Interpret equivalent wording in the supplied text; do not infer unstated facts or use outside knowledge.

The question uses “stop including”; the source states removal in release-summary prose with reStructuredText module markup. The model interprets those equivalent meanings against the frozen criterion and emits a normalized outcome. No particular literal answer string is required by the criterion. The quote checker establishes source membership after whitespace normalization; it does not perform the semantic decision. Expected YES is a proposal expectation, not an on-chain result.

## Anonymous source verification

| Frozen evidence URL | HTTP status | Original bytes | Kept bytes | Check |
|---|---:|---:|---:|---|
| [CPython 3.12 What's New, commit-pinned raw source](https://raw.githubusercontent.com/python/cpython/0fb18b02c8ad56299d6a2910be0bab8ad601ef24/Doc/whatsnew/3.12.rst) | 200 | 101514 | 5000 | Anonymous GET; no cookies or Authorization |

Checked at `2026-11-10T21:26:15.528655+00:00` (UTC), on 2026-11-10 Africa/Lagos. The exact CPython commit is `0fb18b02c8ad56299d6a2910be0bab8ad601ef24`, originally resolved from the official `v3.12.0` release tag. Full response SHA-256: `4a0da7af729f2ba5d6f34d257f440d1700245531aad9cb2bf18bb78af24cfab9`. Kept-prefix SHA-256: `2e61bdf2af142db75084d4999be463e1180ae47278f90434c071c44571bf473d`.

Supporting statement, quoted from the raw source:

```text
Of note, the :mod:`!distutils` package has been removed from the standard library.
```

Its byte span is [2307, 2389) (zero-based UTF-8 offsets), entirely inside the first 5,000 bytes. The response is oversized, so the contract records status `truncated`, original byte_count=101514, kept_byte_count=5000 and available=true. Only the retained prefix enters resolution. There is one proposed frozen evidence URL, and it returned anonymous HTTP 200.

See [machine-readable record](../verification/demo-source-checks.json). Reproduce the read-only check with `..\.venv\Scripts\python.exe -B verification/check_demo_sources.py`. Current anonymous availability does not establish future validator-side retrieval.

## Proposed sequence and expected deterministic result

1. Separately authorize deployment; freeze this question, criterion, one URL, stake 100 and four ordered future deadlines: commit < reveal < resolve-after < resolution-deadline. Record the deployed source/commit identity without exposing wallet secrets.
2. Three accounts privately calculate independent salted commitments for 10000, 5000 and 0 basis points, each recording exactly 100 synthetic stake units.
3. After commit closes, all reveal by reveal deadline. Demonstrate that changing a committed probability fails without affecting accounting.
4. After resolve-after and through resolution-deadline, attempt resolution. Stop and record any unexpected live judgment; do not retry an accepted UNRESOLVABLE outcome. A fetch/consensus failure preserves state and permits retry within the window. After the final deadline, resolution must revert and anyone can expire the OPEN question, then settle for full refunds without fetching evidence.
5. If YES finalizes, save get_decision/get_sources, including supporting quotation, original/kept counts, truncation status and digest. Settle: scores 100000000, 75000000, 0; pot 300; payouts **172, 128, 0**, with one dust unit assigned to the highest score. Stake and forecaster count are unchanged from the worked example.
6. Each participant withdraws once. Verify stakes_in=300, paid_units=300, refunded_units=0, held_units=0 and conserved=true. In a terminal UNRESOLVABLE/expiry branch, verify three full 100-unit refunds instead. These are synthetic accounting effects, not asset transfers.

## Evidence for a future authorized run

Record and verify the direct GenLayer Explorer URL for the deployed contract address as a separate evidence entry on the correct network. Select **GenLayer Explorer Contract** when evidence types are supported. Transaction/source/repository links are additional evidence and do not replace the contract-address link. This local project has no deployed address. This plan does not authorize deployment, submission or repository visibility changes.
