# November 11 submission guidance review

Status: **design confirmation pending; do not submit**. This reviews the existing deployed source at `6cc6b4f32b486dc41fb23d11b7b7b40e004af510`. No contract, tests, ABI, dependencies or deployed behavior changed during this review. The user's guidance is learned review guidance, not official criteria or a promise of points.

## Three separate gates

| Gate | Result against the November 11 guidance | Evidence and limits |
|---|---|---|
| Technical readiness | **FAIL** | The recorded 85 direct tests and three lint checks pass for the approved build. However, `_status_vector` excludes stored quotes; `_resolution` allows determinate outcomes from truncated retained text; and the model supplies the final YES/NO/UNRESOLVABLE directly. Those behaviors fail the new stricter checklist. |
| Distinctiveness | **PASS, local comparison only** | Sealed probabilities from competing forecasters feed an integer quadratic allocation of their common pot, with deterministic dust, forfeiture, refunds and once-only withdrawals. This differs from eligibility/lowest-price awards, novelty-registry rewards, predicate graphs and shared underwriting capital. See DISTINCTIVENESS.md, including the same-week parametric pool. This is not an ecosystem originality finding or a scoring guarantee. |
| Evidence readiness | **FAIL for the proposed stricter revision** | Current revision has two source-matched StudioNet instances, 24 finalized transactions (20 SUCCESS, four expected ERROR), zero held units, verified contract Explorer pages and anonymous public GitHub links. But its positive demo uses truncated evidence, and deployment preceded the first public push under the earlier no-push instruction. These receipts prove the existing source only, not an unimplemented revision or deployment from a previously pushed commit. |

A passing local distinctiveness comparison does not compensate for either failing gate.

## Proposed design for confirmation

The mechanism remains one immutable forecasting question: an owner freezes terms, up to eight forecasters seal equal-stake probabilities and then reveal, anyone resolves or expires, deterministic code settles, and each forecaster withdraws once. States remain OPEN -> RESOLVED -> SETTLED. The pot conservation invariant and existing scoring, dust and refund rules remain unchanged. GenLayer interprets what frozen external evidence establishes; arithmetic alone cannot establish that semantic relationship.

1. Replace the model's final outcome field with one bounded classification per frozen source: HOLDS, CONTRADICTED or UNCLEAR, plus supporting quotes. Reject unknown source IDs and labels; missing classifications become UNCLEAR. Code derives YES only when every required source is complete and HOLDS, NO only when every required source is complete and CONTRADICTED, otherwise UNRESOLVABLE. Conflicting classifications therefore cannot authorize a scored settlement.
2. Keep the existing UTF-8 truncation metadata and 5000-byte cap, but make any truncated required source force UNRESOLVABLE. Unavailable evidence continues to fail closed and cannot authorize YES/NO; retriable fetch failures retain the deadline refund escape. This explicitly changes the earlier approved rule allowing retained text of truncated sources to resolve the question.
3. Retain case-sensitive whitespace-normalized substring quotation matching and the eight-character minimum. Normalize and sort stored quote records and source classifications, then compare the entire canonical stored candidate against the independent evaluation. A leader returning the same headline with different stored quote data must be rejected. Independently selecting different valid quotes may reduce consensus liveness; permissionless deadline expiry remains the refund escape.
4. Use the complete source below for a fresh positive demo. After approval: implement the revision, run lint first and then the full tests, stop and report at that gate. Any later authorized live run must start from a pushed source commit and produce fresh source-matched deployments, receipts, read-backs and Explorer contract entries. Existing receipts remain historical evidence for `6cc6b4f`.

No contract edits or new deployments are authorized merely by this proposal. Confirm the design before implementation, as requested in section 8 of the user's supplied guidance and the workspace AGENTS.md.

## Verified proposed source (not deployed)

Question: Did CPython 3.12 stop including distutils in its standard library?

Pinned URL: https://raw.githubusercontent.com/python/cpython/0ada998ebbf392238719358432cd723a622fcd5e/Doc/library/distutils.rst

Anonymous HTTP **200**; raw **667 bytes**; SHA-256 **8c44b643a8a70ff7bd1c479b5b0b53088ece62f0c73e02bd6668af118a156076**. Entire source fits the cap. Exact supporting text:

> This module is no longer part of the Python standard library.
> It was :ref:`removed in Python 3.12 <whatsnew312-removed-distutils>` after

The source's module heading identifies distutils. The question and the source use different wording. Verification is recorded in `verification/proposed-source-2026-11-11.json`. Earlier attempted paths at the old CPython commit returned 404 and were discarded; they are not proposed evidence.

## Publication and Portal state

Public repository: https://github.com/JWattjr/calibrated-forecast-pool

The full intended Git history was audited for generated signer keys, credential patterns, sensitive JSON fields and secret-bearing filenames before the authorized publication. All seven planned GitHub evidence pages returned anonymous HTTP 200. The public raw source is 27237 bytes and matches the deployed commit blob, SHA-256 `25194904bc324510dbae2614adc982cdbd56bb5af64fde0ec125d8ef3ad49677`. See `verification/public-access-checks-2026-11-11.json`.

The earlier four-entry browser draft is preserved only as a historical local read-back. Its tab is no longer present; the currently open submission form is blank at contribution-type selection. No new entries were entered, CAPTCHA completed or final submission performed during this review. The local title, note and planned evidence remain in SUBMISSION_DRAFT.md and verification/portal-fields.json. Rebuild the form only after resolving the technical gate.
