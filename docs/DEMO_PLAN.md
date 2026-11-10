# Proposed StudioNet demo — not run

Status: proposal only. No deployment or runtime transaction was made. Dates in `examples/constructor.json` are local placeholders; set ordered future deadlines before a separately authorized deployment, then freeze them permanently. Use the separate StudioNet `genlayer-py==0.18.0` environment for any future runtime call; direct tests require 0.19.0rc2.

## Question and literal criterion

Question: Does the CPython 3.12.0 final release-news file explicitly state the release date 2023-10-02?

Criterion: YES only if the frozen CPython 3.12.0 release-news text explicitly states '.. release date: 2023-10-02'. NO only if it explicitly states a different release date for that release. Otherwise UNRESOLVABLE; use no inference or outside knowledge.

This asks about the literal release-date metadata, avoiding an inference about delivery, publication infrastructure or historical event timing. The expected YES is a proposal expectation, not an on-chain result.

## Anonymous source verification

| Frozen evidence URL | HTTP status | Original bytes | Kept bytes | Check |
|---|---:|---:|---:|---|
| [https://raw.githubusercontent.com/python/cpython/0fb18b02c8ad56299d6a2910be0bab8ad601ef24/Misc/NEWS.d/3.12.0.rst](https://raw.githubusercontent.com/python/cpython/0fb18b02c8ad56299d6a2910be0bab8ad601ef24/Misc/NEWS.d/3.12.0.rst) | 200 | 1422 | 1422 | Anonymous GET; no cookies or Authorization |

Checked at `2026-11-10T20:38:35.375374+00:00` (UTC), on 2026-11-10 Africa/Lagos. Full response SHA-256: `106c380d13387bdf6c74bd84e6b20b32f13a8c847ffb9c6bc98aef1617d896e5`. The URL pins the exact CPython commit `0fb18b02c8ad56299d6a2910be0bab8ad601ef24`, obtained by dereferencing the official `v3.12.0` release tag. The exact supporting line is `.. release date: 2023-10-02`; it is in the retained prefix. There is only one proposed frozen evidence URL, and it returned HTTP 200. The full 1,422-byte body fits below the cap, so this proposed demo does not rely on truncation.

See [machine-readable record](../verification/demo-source-checks.json). Reproduce the read-only anonymous check with `..\.venv\Scripts\python.exe -B verification/check_demo_sources.py`. A future check may differ if network availability changes. Current anonymous availability does not prove validator-side retrieval.

## Proposed sequence and expected deterministic result

1. Separately authorize a deployment; freeze this question, one source URL, stake 100 and ordered future deadlines. Record the deployed source/commit identity without exposing wallet secrets.
2. Use three distinct accounts and independent random salts. Privately calculate commitments for 10000, 5000 and 0 basis points. Each account commits exactly 100 synthetic units.
3. After commit closes, reveal all three probabilities before reveal closes. Demonstrate a changed probability reveal fails, without altering accounting.
4. After resolve-after, trigger one resolution. If the source cannot be fetched or consensus fails, stop and record the unchanged state. Do not call an unresolved attempt a successful demo. If UNRESOLVABLE finalizes, record terminal full refunds rather than claiming YES.
5. If YES finalizes, save get_decision/get_sources, including exact quote, counts and kept-text digest. Settle: scores 100000000, 75000000, 0; pot 300; payouts 172, 128, 0 after one dust unit to the highest score.
6. Each participant withdraws once. Verify stakes_in=300, paid_units=300, refunded_units=0, held_units=0 and conserved=true. A second withdrawal must fail. These are synthetic accounting effects, not asset transfers.

## Evidence for a future authorized run

Record the direct GenLayer Explorer URL for the deployed contract address as a separate evidence entry and verify that it opens the correct contract on the correct network. Select **GenLayer Explorer Contract** if evidence types are supported. Deployment/resolve transaction links and source/repository links are additional evidence and cannot replace the contract-address link. There is no deployed address or Explorer evidence for this local project today. A plan does not authorize deployment, submission or repository visibility changes.
