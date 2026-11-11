# New local revision: complete-source demo plan

Status: **executed successfully under explicit release authorization on November 11**. Source commit 32bcc75839a09de2dfb55bda4a52f61c3adbe395 was pushed before the fresh deployment; see LIVE_RELEASE_2026-11-11.md and deployments/studionet-release-2026-11-11.json. The original staged plan below is historical. The November 10 demos in LIVE_DEMO.md and the release manifest prove the historical source at `6cc6b4f`, which allowed positive resolution from a truncated prefix. They do not prove this revised source. The user subsequently reviewed local results and explicitly authorized the release and one scoring demonstration. No fresh expiry instance was requested for this release. The Portal was not used.

## Question, classification and supporting evidence

Question: **Did CPython 3.12 stop including distutils in its standard library?**

Criterion: HOLDS if this source explicitly establishes that distutils was removed from the Python standard library in Python 3.12. CONTRADICTED if it explicitly establishes that distutils remained included in that release. Otherwise UNCLEAR. Interpret equivalent wording; use no unstated facts or outside knowledge.

The source says the module is no longer part of the standard library and identifies removal in Python 3.12. The model interprets that wording relative to the question; it returns HOLDS for this source, while code derives YES. It never selects the final outcome or payout.

Pinned URL: https://raw.githubusercontent.com/python/cpython/0ada998ebbf392238719358432cd723a622fcd5e/Doc/library/distutils.rst

Anonymous HTTP **200**, raw **667 bytes**, all 667 retained, source status **fetched**. SHA-256 of both full and kept text: `8c44b643a8a70ff7bd1c479b5b0b53088ece62f0c73e02bd6668af118a156076`. Verification timestamp: `2026-11-11T13:38:02.231571+00:00`; recheck with `verification/check_demo_sources.py`. A byte-exact local snapshot is in `examples/distutils-source.rst`.

Exact supporting lines, entirely inside the complete 667-byte source:

```text
This module is no longer part of the Python standard library.
It was :ref:`removed in Python 3.12 <whatsnew312-removed-distutils>` after
```

The source's module heading identifies distutils. Its wording differs from the question. Source membership is checked in code; semantic interpretation still depends on independently agreeing source classifications. Anonymous availability now does not prove future GenVM retrieval.

## Sequence for a separately authorized fresh live run

1. After user review of local gates and separate live authorization, push the exact source commit first, then deploy with this question, criterion, URL, stake 100 and strictly ordered future deadlines. Preserve the existing pinned runner and StudioNet client environment. Compare deployed bytes against that pushed commit's Git blob.
2. Three forecasters seal probabilities 10000, 5000 and 0 with separate private random salts, each recording 100 synthetic units. After commit closes, all reveal. Record a deliberately forged reveal as an expected failure and verify unchanged state.
3. Anyone resolves during the resolution window. Expected source label is HOLDS and code-derived outcome YES; stop on an unexpected judgment. Save sources, classifications, canonical quotes, counts and digests. For this authorized release, any consensus failure or UNRESOLVABLE result requires stopping without retry or redesign. A reverted call preserves state, but this run does not retry resolution.
4. Deterministic settlement uses scores 100000000, 75000000 and 0, pot 300 and one unit of dust. Payouts remain **172/128/0**. Withdraw each entitlement once, including zero; record duplicate withdrawal as an expected failure. Final accounting: stakes=300, paid=300, refunded=0, held=0.
5. A fresh expiry instance must prove early-expiry rejection, late-resolution rejection, then permissionless expiry and full refunds for revealed and unrevealed stakes. Truncated evidence is separately covered by local regression tests and cannot resolve this revision to YES or NO.

Record FINALIZED and leader SUCCESS/ERROR separately, read-backs, expected-failure labels, deployed source identity and the release manifest. Add each new contract's direct GenLayer Explorer address URL as its own evidence entry on the correct network, typed **GenLayer Explorer Contract**. Historical addresses remain historical evidence and must not be presented as deployments of this revision. This plan authorizes no push, deployment or submission.
