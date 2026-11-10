# Design

## Boundary and frozen state

One deployment is one question, matching the auction's one-deployment/one-auction layout. The deployment sender is the question owner. Constructor-only configuration freezes the ID, question, criterion, URLs, stake, and three deadlines. There are no update, cancellation, privileged resolution, or third-party withdrawal methods. The owner may forecast on the same terms as everyone else.

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

Timestamps require timezone offsets and are normalized to UTC seconds, exactly as in the auction. Ordering is commit < reveal < resolve-after. Commit requires `now < commit`; reveal requires `commit < now <= reveal`; resolve requires `now > resolve-after`. At the exact commit timestamp neither commitment nor reveal is accepted. A reveal at the exact reveal deadline is accepted. All time decisions use block time. No new policy requiring future constructor deadlines is added: the auction only enforces ordering.

## Source records and the approved truncation deviation

The user explicitly approved replacing the auction's oversized-body rejection with retained-prefix truncation, and directed that per-source records/validation follow research-novelty-bounty. This is the sole fetch-pattern exception; the cap remains 5,000 bytes.

Each source record has exactly `url`, `available`, `status`, `byte_count`, `kept_byte_count`, `content_digest`, and `text`:

| Status | Rule |
|---|---|
| fetched | HTTP 200, nonempty/non-whitespace valid UTF-8 body, 1–5,000 original bytes; kept bytes equal original bytes; available=true. |
| truncated | HTTP 200 body exceeds 5,000 bytes; retain its first 5,000 bytes, then remove only an incomplete UTF-8 character at the end; available=true. |
| unavailable | Network/HTTP failure, absent/non-byte body, empty small body, or invalid UTF-8 in the retained prefix; kept bytes=0, text empty, available=false. |

For truncation, a final partial UTF-8 character may remove at most three bytes. No replacement characters are invented and invalid interior bytes are not silently discarded. Original `byte_count` is preserved even when larger than the cap. `content_digest` is `sha256:` plus SHA-256 of the kept text's exact UTF-8 bytes (not canonical JSON). The digest of unavailable kept text is SHA-256 of the empty byte string. A successful oversized all-whitespace body remains a truncated available body, as directed; it cannot supply a nonempty supporting line. The SDK materializes the HTTP body before contract truncation: this bounds retained/prompted/stored text, not transport memory use.

Validation checks the exact source schema/order/URL, flags, statuses, integer counts, count ranges, kept UTF-8 length and digest. `truncated` with `byte_count <= 5000` is invalid. `fetched` requires original=kept<=5000. The independent validator re-fetches and re-derives the same truncation record, text and digest. Comparison binds the complete record, preventing a self-consistent but false count/prefix/digest from being accepted merely because the attacker recomputed the outer hashes.

Any unavailable source aborts the entire attempt before state is written, even if another source was fetched. Failed-attempt availability is transient, not persisted; `get_sources()` exposes records from a finalized resolution only. This preserves the requested unchanged-state retry behavior. There is no `oversized` status.

## Single nondeterministic judgment

The model sees only the frozen question/criterion and kept text, never probability-based payout instructions. It must emit the strict `{outcome, quotes:[{url,line}]}` schema. Outcomes normalize by stripping whitespace and uppercasing, then must be YES, NO or UNRESOLVABLE. Unknown fields, malformed values and bounds violations revert for retry. Only literal evidence settles the criterion; inference, ambiguity and conflict require UNRESOLVABLE.

Every quoted line must be a complete nonempty line appearing verbatim in the kept text of its cited available source. A missing quote for YES/NO, partial line, fabricated line, unavailable URL or tail-only quote deterministically downgrades to UNRESOLVABLE and removes the unsupported quotations. There is no free-form explanation in state.

The input digest binds all frozen terms, contract address and sorted forecast records. The evidence digest binds the input digest plus complete source records, including availability and retained text. The judged snapshot digest binds input and evidence digests. Validators validate the leader candidate, independently repeat fetching and resolution, and compare normalized outcome plus bound evidence/snapshot fields. They do not require identical choices of exact supporting lines. Quotations must independently pass verbatim checks against the identical retained evidence. This is not a deterministic proof of semantic entailment; substantive correctness depends on independent validator judgment.

Failed fetch, invalid model result and failed consensus do not change status, stored evidence, balances or allocations. An accepted UNRESOLVABLE result is terminal and cannot be retried. Settlement remains a separate permissionless deterministic action.

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

Limits: 8 forecasters, 1–3 distinct HTTPS URLs of at most 500 characters, 64-character question ID, normalized question/criterion each up to 2,000 characters, bounded JSON input (2,500 characters for URLs), 64-character timestamp inputs, 16–128-character salt, stake 1..10^12, probability 0..10,000, 5,000 kept bytes per source, 6 quoted lines of 1..1,000 characters, model JSON text at most 8,000 characters, bounded outcome string. Maximum pot is 8*10^12; integer multiplication/division stays far below u256 limits. Input normalization bounds follow the auction exactly.
