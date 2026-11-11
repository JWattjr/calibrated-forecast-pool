# Submission draft — current release only

Category: **Builder → Intelligent Contracts (type 52)**. Contribution date: **2026-11-11 (Africa/Lagos)**. Status: local submission payload prepared for user review. **The Portal was not opened or submitted for this task.**

## Title

Calibrated Forecast Pool — sealed probabilities and conserved Brier payouts

## Note (840/1000 characters)

Forecasters seal identity/question/contract-bound probabilities with equal synthetic stakes, then reveal. Validators independently fetch frozen sources and classify each HOLDS / CONTRADICTED / UNCLEAR; code derives YES / NO / UNRESOLVABLE and conserved integer Brier payouts. Truncated required evidence fails closed to UNRESOLVABLE. The complete 667-byte pinned distutils source produced HOLDS and code-derived YES on StudioNet. All 14 transactions finalized: 12 SUCCESS, 2 expected rollbacks (changed reveal and double withdrawal). Three 100-unit stakes paid 172/128/0 from 300; 0 held. Lint and 112 direct tests pass. Deadline-expiry refunds are covered by direct tests, not this deployment's live run. Limits: synthetic units, no native/token custody or transfers; pool-normalized payouts do not guarantee truthful-reporting incentives.

## Evidence list in submission order

The first entry is the separately verified direct contract-address URL on StudioNet, chain 61999. Select **GenLayer Explorer Contract**. The full address and matching deployment transaction were verified in the rendered Explorer during release verification; the proof is recorded in verification/studionet-explorer-2026-11-11.json at evidence commit `5beb647993c7a4a9c2ba727b20a8d5ef09b185b0`. Repository, source and transaction links do not replace this contract entry.

1. **GenLayer Explorer Contract** — [Current contract — StudioNet](https://explorer-studio.genlayer.com/address/0x4e510d9f62d2632892BB84A52557b4573A94a2D6)
2. **GitHub Repository** — [Public repository](https://github.com/JWattjr/calibrated-forecast-pool)
3. **GitHub File** — [Exact deployed source](https://github.com/JWattjr/calibrated-forecast-pool/blob/32bcc75839a09de2dfb55bda4a52f61c3adbe395/contracts/calibrated_forecast_pool.py)
4. **GitHub File** — [Release manifest](https://github.com/JWattjr/calibrated-forecast-pool/blob/5beb647993c7a4a9c2ba727b20a8d5ef09b185b0/deployments/studionet-release-2026-11-11.json)
5. **GitHub File** — [LIVE results — all 14 transactions](https://github.com/JWattjr/calibrated-forecast-pool/blob/5beb647993c7a4a9c2ba727b20a8d5ef09b185b0/docs/LIVE_RELEASE_2026-11-11.md)
6. **GitHub File** — [112-test matrix](https://github.com/JWattjr/calibrated-forecast-pool/blob/5beb647993c7a4a9c2ba727b20a8d5ef09b185b0/docs/TEST_MATRIX.md)
7. **GitHub File** — [Design and incentive limitation](https://github.com/JWattjr/calibrated-forecast-pool/blob/5beb647993c7a4a9c2ba727b20a8d5ef09b185b0/docs/DESIGN.md)
8. **GitHub File** — [Local distinctiveness comparison](https://github.com/JWattjr/calibrated-forecast-pool/blob/5beb647993c7a4a9c2ba727b20a8d5ef09b185b0/docs/DISTINCTIVENESS.md)
9. **Other** — [Resolve (YES)](https://explorer-studio.genlayer.com/tx/0x22d0aac3aa594bba53de420fa9f6b17b050b0f76ee5ecb549627d29b485c4411)
10. **Other** — [Settle](https://explorer-studio.genlayer.com/tx/0x631d8c0cf86d2ebff72f152283e54e27556ac52f59a2d4b31be8caea6f6dce54)
11. **Other** — [Withdrawal — Alice, 172 units](https://explorer-studio.genlayer.com/tx/0xc4646f4b71d9edf8c0181a0c3d0cd956a52a0d03a3ccb5fbf0c952a37e18d185)
12. **Other** — [Changed reveal (EXPECTED FAILURE)](https://explorer-studio.genlayer.com/tx/0x73012d2812688f2d9871da0df0899434f64d3b05c182097bd2dd3ec27369802f)
13. **Other** — [Double withdrawal (EXPECTED FAILURE)](https://explorer-studio.genlayer.com/tx/0xfb114a15398b46b8dae4fc2c22dfc30f0a21e0918b545b2b68f8c12778be92fd)

## Reviewer guide

The exact deployed source is pinned to `32bcc75839a09de2dfb55bda4a52f61c3adbe395`. The manifest, LIVE results, TEST_MATRIX, DESIGN and DISTINCTIVENESS are pinned to `5beb647993c7a4a9c2ba727b20a8d5ef09b185b0`. These pinned evidence files remain unchanged by this draft update.

Start with LIVE_RELEASE_2026-11-11.md and the manifest for the 14 classified transactions and final views. The source was pushed before deployment and the on-chain bytes matched the source commit exactly. DESIGN.md explains per-source labels, deterministic outcome/payout derivation, truncation fail-closed behavior, and consensus agreement on facts while different valid normalized quote selections may agree. TEST_MATRIX.md covers 112 mocked direct cases, including deadline-expiry refunds; this deployment did not run an expiry demonstration. DISTINCTIVENESS.md is a local comparison, including the same-week underwriting pool, not an ecosystem originality or points claim. November 10 deployments are historical evidence for the previous source only and are excluded from this evidence list.

The five transaction entries above are all FINALIZED. Resolve, settlement and the selected 172-unit withdrawal executed SUCCESS; changed reveal and double withdrawal executed ERROR as deliberately expected failures, with unchanged-state read-backs. Final synthetic accounting is stakes_in=300, paid_units=300, refunded_units=0, held_units=0, conserved=true. All seven view methods were read at the end.

## Anonymous access verification

All **13 evidence URLs returned HTTP 200 anonymously** during this rewrite. Each request used a fresh session without cookies, Authorization, account login or ambient proxy credentials. Exact per-URL status, final URL and UTC timestamp are recorded in verification/portal-fields.json. No Portal URL was requested.

## Handoff boundary

The title, note, evidence order/types and release pins in this file match verification/portal-fields.json. These are local files only; no fields were entered into a Portal form, no CAPTCHA was completed and no submission was made.
