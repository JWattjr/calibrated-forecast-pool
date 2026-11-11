# Submission draft

Category: **Intelligent Contracts** (Builder, type 52). Contribution date: **2026-11-10** (work completion date; also the Portal's current UTC date maximum). Draft prepared on **2026-11-11 Africa/Lagos**. Status: public repository created and pushed with explicit approval; seven GitHub evidence links verified anonymously. **Held for design confirmation; not submitted**.

## Title

Calibrated Forecast Pool — sealed probabilities and conserved Brier payouts

## Portal note (951/1000 characters)

Forecasters seal identity/question/contract-bound probabilities and equal synthetic stakes, then reveal. Validators independently fetch frozen sources and interpret a binary criterion; integer Brier scores deterministically split the pot, with dust ordering, unrevealed-stake forfeiture and one-shot withdrawals. Permissionless deadline expiry refunds unresolved pools. Two source-matched StudioNet demos: CPython distutils removal resolved YES and paid 172/128/0 from 300 units; expiry refunded both revealed and unrevealed 100-unit stakes. All 24 transactions finalized: 20 successes, 4 expected rollbacks; zero units held. 85 direct tests and lint/SDK validation pass. Local comparisons disclose shared commit-reveal and evidence-resolution plumbing; the distinction is sealed-probability scoring with conserved allocation. Limits: synthetic ledger, no native/token custody; normalized pooled payouts do not guarantee truthful-reporting incentives.

## Evidence entries

The first two entries are separate direct contract-address Explorer links on StudioNet chain 61999, verified in Chrome against the displayed contract and matching finalized deployment transactions. Select **GenLayer Explorer Contract** for each. Transaction and repository links do not replace these entries.

- **GenLayer Explorer Contract** — [Scoring contract — StudioNet](https://explorer-studio.genlayer.com/address/0xc74acBa3E9f5733680a8f6245717DFD70C8f7e93)
- **GenLayer Explorer Contract** — [Expiry-refund contract — StudioNet](https://explorer-studio.genlayer.com/address/0xE908f2670Ee24C13346cf2e754001Ad20F2f825A)
- **GitHub Repository** — [Public repository](https://github.com/JWattjr/calibrated-forecast-pool)
- **GitHub File** — [Exact deployed contract source](https://github.com/JWattjr/calibrated-forecast-pool/blob/6cc6b4f32b486dc41fb23d11b7b7b40e004af510/contracts/calibrated_forecast_pool.py)
- **GitHub File** — [Live release manifest](https://github.com/JWattjr/calibrated-forecast-pool/blob/317bc7ce8f58d429274f7949eb7133236d16fb48/deployments/studionet-release-2026-11-10.json)
- **GitHub File** — [Live results and transaction classification](https://github.com/JWattjr/calibrated-forecast-pool/blob/317bc7ce8f58d429274f7949eb7133236d16fb48/docs/LIVE_DEMO.md)
- **GitHub File** — [85-case test matrix](https://github.com/JWattjr/calibrated-forecast-pool/blob/317bc7ce8f58d429274f7949eb7133236d16fb48/docs/TEST_MATRIX.md)
- **GitHub File** — [Design and incentive limitation](https://github.com/JWattjr/calibrated-forecast-pool/blob/6cc6b4f32b486dc41fb23d11b7b7b40e004af510/docs/DESIGN.md)
- **GitHub File** — [Local distinctiveness comparison](https://github.com/JWattjr/calibrated-forecast-pool/blob/317bc7ce8f58d429274f7949eb7133236d16fb48/docs/DISTINCTIVENESS.md)
- **Other** — [Finalized YES resolution](https://explorer-studio.genlayer.com/tx/0xf2163890548a0274d2c9314f429ce6796e455d092dc4d550940c134b0d37a8ab)
- **Other** — [Finalized deadline expiry](https://explorer-studio.genlayer.com/tx/0x1d678975dcd1d2137defb9585876b6e10bdb967680beebf62b721bc3735eba30)

## Reviewer guide

The deployed source is frozen at `6cc6b4f32b486dc41fb23d11b7b7b40e004af510`; live evidence is pinned to `317bc7ce8f58d429274f7949eb7133236d16fb48`. The source blob is identical in both deployed instances. The initial release manifest and its local-only repository status describe the live-run capture on November 10, before this separately authorized publication. Current publication access passed anonymous verification; see verification/public-access-checks-2026-11-11.json.

Start with LIVE_DEMO.md for the 24 classified transactions and final balances, DESIGN.md for the scoring/dust/refund rules and incentive caveat, TEST_MATRIX.md for the 85 mocked direct-mode cases, and DISTINCTIVENESS.md for the local comparator review. The distinction is the sealed-probability scoring/allocation mechanism, not web resolution or commit-reveal alone. No ecosystem-wide originality claim is made.

## Final review

- Confirm both direct Explorer contract links open the expected contracts on StudioNet and retain their own evidence entries/type.
- Confirm repository and pinned files are readable anonymously after publication.
- Verify title, note, date and every evidence URL/type match verification/portal-fields.json.
- Review the completed Portal draft. CAPTCHA and final submission are separate from this prepared draft; Portal submission has not occurred.

## Current Portal state and review hold

The prior four-entry draft read-back is historical. That tab is no longer present and the open submission form is blank at contribution-type selection. The seven GitHub links above are public and verified, but have not been entered into a replacement form. CAPTCHA and final submission were not performed. Resolve the technical gaps in [the November 11 review](docs/SUBMISSION_REVIEW_2026-11-11.md) before preparing a replacement submission.
