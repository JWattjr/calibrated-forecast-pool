# Current StudioNet release — November 11

Source commit: `32bcc75839a09de2dfb55bda4a52f61c3adbe395`; Git blob `83f82f4a0ee7eea4a14c09ba78abc0191cc5700f`; SHA-256 `686e0530f616fee0794686f14c16ccafc0d73dfa22aa2915dc17aacfc128ca9a`. Remote main matched this commit before deployment, anonymous raw source returned 200, and fetched on-chain bytes matched the pushed file exactly. Runtime calls used genlayer-py **0.18.0**, chain **61999**, and pinned runner `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`.

## Separate Explorer contract evidence

**Evidence type: GenLayer Explorer Contract** — [Current scoring contract](https://explorer-studio.genlayer.com/address/0x4e510d9f62d2632892BB84A52557b4573A94a2D6)

The rendered StudioNet Explorer page was checked against the full address and finalized deployment transaction. See verification/studionet-explorer-2026-11-11.json. Transaction and source links are additional evidence, not replacements for this direct contract entry. No Portal interaction or submission occurred.

## Live result and final views

Three 100-unit commitments and three successful reveals recorded probabilities 10000, 5000 and 0. A deliberately changed reveal reverted without state changes. The single resolution attempt classified the complete **667-byte** distutils source **HOLDS**; code derived **YES**. Source status is fetched, original=kept=667, digest `sha256:8c44b643a8a70ff7bd1c479b5b0b53088ece62f0c73e02bd6668af118a156076`.

Settlement scores are 100000000, 75000000 and 0. The pot is 300, with one dust unit assigned to the highest score: payouts **172/128/0**. Each allocation, including zero, was withdrawn once. A duplicate withdrawal reverted without state changes.

Final accounting: **stakes_in=300, paid_units=300, refunded_units=0, held_units=0, conserved=true**. All seven view methods were read at the end: question, accounting, decision, sources, settlement, all three forecast records and commitment-hash checks under each forecaster identity. Exact values are in the release manifest.

## Every transaction

All **14** transactions finalized: **12 SUCCESS**, **2 expected ERROR**. Acceptance/finality and leader execution results are stored separately, with votes, consensus results, full receipts and read-backs.

| Operation | Explorer transaction | Finality | Leader execution | Result |
|---|---|---|---|---|
| score_deploy | [transaction](https://explorer-studio.genlayer.com/tx/0x0c7dcdea2fd9dbe3acfa398c0105be74bd4c968b57c2f9faf3d2f53da1bd432c) | FINALIZED | SUCCESS | SUCCESS |
| score_commit_alice | [transaction](https://explorer-studio.genlayer.com/tx/0xe7fce14553202fb40dac4fe6c647a33934f0c51e5771f726e4246e47234b92e8) | FINALIZED | SUCCESS | SUCCESS |
| score_commit_bob | [transaction](https://explorer-studio.genlayer.com/tx/0x3edbc6d36ee7e98f8efca1af1c3f41879ef12923f4c962ad7aaf61c4e7920688) | FINALIZED | SUCCESS | SUCCESS |
| score_commit_charlie | [transaction](https://explorer-studio.genlayer.com/tx/0x5d77d7d6b4f99d4ccfb110f31617e6474833ca34b3ab237e97e0fc9d372af0e9) | FINALIZED | SUCCESS | SUCCESS |
| score_forged_reveal | [transaction](https://explorer-studio.genlayer.com/tx/0x73012d2812688f2d9871da0df0899434f64d3b05c182097bd2dd3ec27369802f) | FINALIZED | ERROR | EXPECTED ROLLBACK: reveal does not match |
| score_reveal_alice | [transaction](https://explorer-studio.genlayer.com/tx/0x5b0ce9d6ebd05af816b63f49cf803b0cdf4d401fb8861a51e314db8f9f9a03e5) | FINALIZED | SUCCESS | SUCCESS |
| score_reveal_bob | [transaction](https://explorer-studio.genlayer.com/tx/0x9bce962008aa201fe3c752070732b4ba1e74c204d450eca9efa031e5bb5bd923) | FINALIZED | SUCCESS | SUCCESS |
| score_reveal_charlie | [transaction](https://explorer-studio.genlayer.com/tx/0x2e9f2fdf1443f063484d9a6604e482779271f4963985cef0d0bc66f1f20715df) | FINALIZED | SUCCESS | SUCCESS |
| score_resolve | [transaction](https://explorer-studio.genlayer.com/tx/0x22d0aac3aa594bba53de420fa9f6b17b050b0f76ee5ecb549627d29b485c4411) | FINALIZED | SUCCESS | SUCCESS |
| score_settle | [transaction](https://explorer-studio.genlayer.com/tx/0x631d8c0cf86d2ebff72f152283e54e27556ac52f59a2d4b31be8caea6f6dce54) | FINALIZED | SUCCESS | SUCCESS |
| score_withdraw_alice | [transaction](https://explorer-studio.genlayer.com/tx/0xc4646f4b71d9edf8c0181a0c3d0cd956a52a0d03a3ccb5fbf0c952a37e18d185) | FINALIZED | SUCCESS | SUCCESS |
| score_withdraw_bob | [transaction](https://explorer-studio.genlayer.com/tx/0xaef089ce6a05ab5bea2aca5038cc4b30135f4958c6b130d91a276adaba2a0647) | FINALIZED | SUCCESS | SUCCESS |
| score_withdraw_charlie | [transaction](https://explorer-studio.genlayer.com/tx/0xe7092f64bbd5946044d5085a61b9ea906698f83deba0857cd21d29ec2bf3f38e) | FINALIZED | SUCCESS | SUCCESS |
| score_duplicate_withdraw | [transaction](https://explorer-studio.genlayer.com/tx/0xfb114a15398b46b8dae4fc2c22dfc30f0a21e0918b545b2b68f8c12778be92fd) | FINALIZED | ERROR | EXPECTED ROLLBACK: already been withdrawn |

## Historical evidence and limits

The old scoring address `0xc74acBa3E9f5733680a8f6245717DFD70C8f7e93` and old expiry address `0xE908f2670Ee24C13346cf2e754001Ad20F2f825A` are **historical evidence for previous source commit 6cc6b4f only**. Their old receipts do not prove the new source. See LIVE_DEMO.md and the November 10 manifest for historical details. No fresh expiry deployment is claimed in this release.

The live run proves the observed honest-network semantic judgment, conservation and two guards. It does not establish adversarial consensus security, a formal audit, real token custody or truthful-reporting incentives for normalized pooled Brier payouts. All units are synthetic.
