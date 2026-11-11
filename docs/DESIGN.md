# Design

Current local revision: user-approved November 11 design with fact agreement and independently validated, normalized quotations. This source has not been pushed or deployed. Historical StudioNet evidence proves only source commit `6cc6b4f`.


## Boundary and frozen state

One deployment is one question, matching the auction's one-deployment/one-auction layout. The deployment sender is the question owner. Constructor-only configuration freezes the ID, question, criterion, URLs, stake, and four deadlines. There are no update, owner-cancellation, privileged resolution, or third-party withdrawal methods. Anyone can expire an unresolved question after its frozen resolution deadline. The owner may forecast on the same terms as everyone else.

User action → frozen source URLs → bounded web fetch and independent validator judgment → terminal YES/NO/UNRESOLVABLE → deterministic pot allocation → one synthetic withdrawal per forecaster.

An off-chain client owns private salt generation, local commitment calculation, UI, indexing and non-authoritative previews. The contract owns commitment checks, frozen inputs, consensus result validation, deadline/state transitions, scoring, settlement and accounting. External publishers own the evidence; fetched content is untrusted input and is not assumed authentic or fresh.

## Reference patterns

The runner header, `_text`, bounded JSON parsing, timezone-aware time parsing/canonicalization, block-time access through `gl.message_raw`, HTTPS/public-DNS checks, URL list handling, `_canonical`, `_digest` and model-object parsing are copied from the auction (only the URL-list error message changes from bid to question). Storage uses class-annotated `Address`, `u256`, `TreeMap[str,str]` JSON records and `DynArray[str]`. Sender and contract addresses use the auction's lowercase normalization. The consensus wrapper uses its independent `leader_fn`, `validator_fn`, exact candidate schema, snapshot binding, `run_nondet_unsafe` and classified-error handling. The Windows/legacy-SDK direct-test compatibility fixture is copied verbatim.

The domain-specific transition and ledger replace bids/one award with sealed probabilities/equal stakes/multiple allocations. As in the auction, all units are synthetic bookkeeping numbers. Committing adds the exact frozen stake to `stakes_in`; it does not debit an external balance. Withdrawal changes accounting and returns units, without a token transfer or native payment. No faucet or new payment API was invented.

## Commitment encoding

Hash the following object with sorted keys, compact separators `(',', ':')`, ASCII escaping (`ensure_ascii=True`), then UTF-8. Prefix the lowercase SHA-256 hex digest with `sha256:`:

```json
{"contract_address":"lowercase deployed address","forecaster":"lowercase sender address","probability_bps":7000,"question_id":"release-1","salt":"private-random-salt-at-least-16-characters"}
```

The implementation matches the auction's canonical JSON hashing, rather than concatenating ambiguous strings. Probability, salt, forecaster, question and contract are all bound. Tests reconstruct the hash independently and reject copied hashes from another identity, question or deployment. Use a cryptographically random salt off-chain; the contract enforces 16–128 characters, not entropy. The view helper is public and does not provide privacy if used through a public RPC or publicly logged client.

## Deadlines

Timestamps require timezone offsets and are normalized to UTC seconds, exactly as in the auction. Ordering is commit < reveal < resolve-after < resolution-deadline. Commit requires `now < commit`; reveal requires `commit < now <= reveal`; resolve requires `resolve-after < now <= resolution-deadline`. Permissionless expiry requires status OPEN and `now > resolution-deadline`. At the exact commit timestamp neither commitment nor reveal is accepted. A reveal at the exact reveal deadline is accepted. Resolution at the exact final deadline is accepted; expiry at that timestamp reverts. After the final deadline resolution reverts, and `expire_unresolved()` records a deterministic UNRESOLVABLE outcome with top-level reason `RESOLUTION_DEADLINE`, empty sources and empty quotes. It uses the normal input/evidence digests over an empty evidence list, performs no fetch or model call, and sets status RESOLVED. The unchanged settlement path then refunds every original stake, revealed or unrevealed. Already resolved/settled questions cannot expire. All time decisions use block time. No new policy requiring future constructor deadlines is added: the auction only enforces ordering.

## Source records and the approved truncation deviation

The user explicitly approved replacing the auction's oversized-body rejection with retained-prefix truncation, and directed that per-source records/validation follow research-novelty-bounty. The cap remains 5,000 bytes. In the November 11 forecast-pool revision, truncation metadata is preserved but **any truncated required source forces terminal UNRESOLVABLE**, even if a valid supporting passage is inside the retained prefix. This contract-specific rule does not change parametric-coverage-pool.

Each source record has exactly `url`, `available`, `status`, `byte_count`, `kept_byte_count`, `content_digest`, and `text`:

| Status | Rule |
|---|---|
| fetched | HTTP 200, nonempty/non-whitespace valid UTF-8 body, 1–5,000 original bytes; kept bytes equal original bytes; available=true. |
| truncated | HTTP 200 body exceeds 5,000 bytes; retain its first 5,000 bytes, then remove only an incomplete UTF-8 character at the end; available=true. |
| unavailable | Network/HTTP failure, absent/non-byte body, empty small body, or invalid UTF-8 in the retained prefix; kept bytes=0, text empty, available=false. |

For truncation, a final partial UTF-8 character may remove at most three bytes. No replacement characters are invented and invalid interior bytes are not silently discarded. Original `byte_count` is preserved even when larger than the cap. `content_digest` is `sha256:` plus SHA-256 of the kept text's exact UTF-8 bytes (not canonical JSON). The digest of unavailable kept text is SHA-256 of the empty byte string. A successful oversized all-whitespace body remains a truncated available body, as directed; it forces UNRESOLVABLE, as does every truncated required source. The SDK materializes the HTTP body before contract truncation: this bounds retained/prompted/stored text, not transport memory use.

Validation checks the exact source schema/order/URL, flags, statuses, integer counts, count ranges, kept UTF-8 length and digest. `truncated` with `byte_count <= 5000` is invalid. `fetched` requires original=kept<=5000. The independent validator re-fetches and re-derives the same truncation record, text and digest. Comparison binds the complete record, preventing a self-consistent but false count/prefix/digest from being accepted merely because the attacker recomputed the outer hashes.

Any unavailable source aborts the entire attempt before state is written, even if another source was fetched. Failed-attempt availability is transient, not persisted; `get_sources()` exposes records from a finalized resolution only. This preserves the requested unchanged-state retry behavior. There is no `oversized` status.

## Per-source classification and deterministic outcome

The model sees only the frozen question/criterion and complete fetched text, never probability-based payout instructions. It emits exactly `{classifications:[{url,label}], quotes:[{url,line}]}`. It cannot supply an outcome field. The allowed labels are HOLDS, CONTRADICTED and UNCLEAR. HOLDS means the cited source explicitly establishes the affirmative proposition; CONTRADICTED establishes the negative; missing support, ambiguity or internal conflict requires UNCLEAR. Labels are stripped and uppercased. Unknown fields, invented or duplicate URLs, unknown labels and bounds violations revert for retry. Missing source classifications become UNCLEAR. Stored classifications contain one record per frozen URL and are sorted by URL.

Code derives YES only when every required source is complete (`fetched`) and every label is HOLDS; NO only when every required source is complete and every label is CONTRADICTED. All other combinations derive UNRESOLVABLE, including disagreement between sources and missing labels. A determinate label needs a valid supporting quote from its own URL; otherwise that label becomes UNCLEAR. Any unavailable required source aborts the attempt without changing state. Any truncated required source records all labels as UNCLEAR, empty quotes and UNRESOLVABLE without calling the model. The text/count/digest truncation rules above remain independently verified.

For quotation matching, collapse whitespace runs to one space and strip both quote and source text. Each normalized quote must contain at least eight characters and be a case-sensitive substring of the normalized text of its cited available source. Partial-line quotations and line wrapping differences are accepted. Raw quote length remains bounded to 1000 characters, with at most six quotes total. Stored quote lines are normalized and records sorted by `(url, line)`. Invalid, fabricated, too-short, unavailable-source or discarded-tail quotations are dropped individually. Only valid remaining quotes enter `supported` and storage. A source label becomes UNCLEAR only when its source has no remaining valid quote; a valid quote plus an invalid quote for the same source therefore preserves HOLDS and can derive YES. Structural schema, type and size violations still revert under the existing bounds. Truncation still overrides all classifications to UNCLEAR and derives UNRESOLVABLE. An adversarial stored candidate containing those quotations is rejected rather than silently repaired, because `_valid_candidate` requires the supplied resolution to equal its revalidated canonical form. Non-normalized or unsorted leader quote records are likewise rejected.

## Agreement on facts, with quote-selection freedom

The validator first runs `_valid_candidate` on the leader result, then independently fetches every frozen URL and reruns classification. Agreement compares the input snapshot digest, judged snapshot digest, evidence digest, canonical complete source records (including byte-identical text, original/kept byte counts and digests), canonical per-source labels, and the code-derived outcome. A different label disagrees even when both results derive UNRESOLVABLE. An inconsistent supplied outcome is rejected by deterministic derivation; an independently consistent different outcome still disagrees.

**Quote choice is deliberately excluded from agreement for consensus liveness.** Two independent models can establish the same source facts using different genuine supporting passages; requiring the same selected passage would create avoidable disagreements. Both quote sets must be canonical and individually pass the same substring/source checks, and both models must agree on every source label and the derived outcome. The stored leader's quotes are therefore source-backed even when the validator chooses other valid quotes. This explicit user-approved exception does not permit fabricated evidence: `_valid_candidate` rejects fabricated, wrong-case, short, unknown-source and noncanonical stored quotations before comparison. Quotation membership alone does not prove semantic entailment; independent classification remains the substantive semantic check. No free-form rationale is stored.

Failed fetch, invalid model result and failed consensus preserve all state and permit retry only through the resolution deadline. An accepted UNRESOLVABLE, including truncated evidence, is terminal and refunds all stakes through settlement. Permissionless deadline expiry retains the full-refund escape and records empty sources, classifications and quotes. Settlement remains a separate deterministic action.

## Scoring, dust and worked example

For each revealed forecast, with integer basis-point probability `p`:

```text
target = 10000 for YES, 0 for NO
score = 10000**2 - (p - target)**2
pot = number of commitments * frozen stake
payout = (pot * score) // sum_of_revealed_scores
```

Unrevealed forecasts have no score and receive zero in scored settlement; their stakes remain in the pot. All floor-division dust goes to the highest-score revealed forecaster, breaking ties by lowest lowercase address. Addresses are fixed-width hexadecimal, so this is also numeric address order. The rule applies even when dust is zero; `dust_recipient` records the deterministic candidate.

Example: three forecasters each stake 100 and reveal 10,000, 5,000 and 0. For YES their scores are 100,000,000; 75,000,000; and 0. The pot is 300, total score is 175,000,000 and floor payouts are 171, 128 and 0. One dust unit goes to the 10,000 forecast: final payouts are **172, 128, 0**. For NO the endpoint scores reverse, producing **0, 128, 172**. If two equal-score forecasters share a three-unit pot, floors are 1 and 1 and the lower address receives the final unit.

UNRESOLVABLE, no revealed forecasts, or zero total score refunds all original stakes, including unrevealed ones. Empty pools settle to an empty allocation. Scored payout zero is still withdrawable once, then a second call reverts. Settlement itself can occur only once.

The quadratic score is a proper scoring rule in isolation. Payouts here normalize that score against other forecasters' scores and a fixed pot; this generally changes strategic incentives and does not guarantee that truthful probabilities maximize expected monetary payout. Equal stakes do not prevent Sybil participation or collusion. This implements the specified pooled Brier allocation; it makes no strict incentive-compatibility or real-world calibration-performance claim.

## Conservation and bounds

At every point:

```text
stakes_in = paid_units + refunded_units + held_units
held_units = stakes_in - paid_units - refunded_units
```

Settlement allocates exactly the pot but does not count unwithdrawn entitlements as paid. Withdrawals move only the caller's entitlement from held to paid or refunded, once. Tests independently sum all settled rows and split claimed/unclaimed entitlements to check the view's counters, rather than relying only on its `conserved` boolean.

Limits: 8 forecasters, 1–3 distinct HTTPS URLs of at most 500 characters, 64-character question ID, normalized question/criterion each up to 2,000 characters, bounded JSON input (2,500 characters for URLs), 64-character timestamp inputs, 16–128-character salt, stake 1..10^12, probability 0..10,000, 5,000 kept bytes per source, 6 quotations of at most 1,000 raw characters, each requiring at least 8 normalized characters for a determinate outcome, model JSON text at most 8,000 characters, bounded outcome string. Maximum pot is 8*10^12; integer multiplication/division stays far below u256 limits. Input normalization bounds follow the auction exactly.
