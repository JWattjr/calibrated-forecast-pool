# Historical StudioNet demonstration — previous source only

Historical evidence only: addresses 0xc74acBa3E9f5733680a8f6245717DFD70C8f7e93 and 0xE908f2670Ee24C13346cf2e754001Ad20F2f825A prove only the previous source. Both instances use exact deployed source commit `6cc6b4f32b486dc41fb23d11b7b7b40e004af510` (Git blob `c803084a5cce74da4b9bbfd53b37b36526d20bba`, SHA-256 `25194904bc324510dbae2614adc982cdbd56bb5af64fde0ec125d8ef3ad49677`). Deployed bytes were independently fetched from chain-61999 RPC and matched the committed source exactly. Calls used the installed `genlayer-py==0.18.0` runtime; no package upgrade occurred.

## Separate contract evidence

| Evidence type | Instance | Verified direct contract URL |
|---|---|---|
| GenLayer Explorer Contract | Scoring | [Scoring contract](https://explorer-studio.genlayer.com/address/0xc74acBa3E9f5733680a8f6245717DFD70C8f7e93) |
| GenLayer Explorer Contract | Expiry | [Expiry contract](https://explorer-studio.genlayer.com/address/0xE908f2670Ee24C13346cf2e754001Ad20F2f825A) |

Both links opened the correct contract and matching finalized deployment transaction in Chrome on GenLayer Studio Explorer. Direct HTTP returned a browser challenge; the rendered verification is recorded separately in `verification/studionet-explorer-2026-11-10.json`. Transaction links below are additional evidence, not replacements for these contract-address links.

## Scoring result

Three independent forecasters each committed 100 synthetic units and revealed probabilities 10000, 5000 and 0. An intentionally changed reveal reverted. The sole live nondeterministic judgment resolved **YES** for CPython 3.12 removing distutils from the standard library. The on-chain source record is **truncated**, available=true, original bytes **101514**, kept bytes **5000**. Its exact kept-text digest and normalized supporting quotation were verified against final state.

Integer scores were 100000000, 75000000 and 0. The 300-unit pot allocated **172 / 128 / 0**, including one unit of dust to the highest score. All three allocations, including the zero allocation, were withdrawn once. A second withdrawal reverted. Final accounting: stakes_in=300, paid_units=300, refunded_units=0, held_units=0, conserved=true.

## Expiry result

A separate instance collected two equal 100-unit commitments; Alice revealed and Bob did not. Expiry before the frozen deadline reverted. A resolution attempt after the deadline reverted. Permissionless expiry then recorded **UNRESOLVABLE**, reason **RESOLUTION_DEADLINE**, empty sources and empty quotes, without a model call. Settlement refunded both original stakes in full. Final accounting: stakes_in=200, paid_units=0, refunded_units=200, held_units=0, conserved=true.

## Transactions

All **24** transactions finalized: **20** successful executions and **4** explicitly expected rollbacks. Acceptance/finality and leader execution are stored separately, along with consensus results, vote counts/types and SDK transaction records.

| Operation | Receipt link | Lifecycle | Leader execution | Classification |
|---|---|---|---|---|
| `score_deploy` | [transaction](https://explorer-studio.genlayer.com/tx/0xacd8fecbc631531fed7e8839f04286f85cc55121e607cfef2edc536301e0f3a5) | FINALIZED | SUCCESS | SUCCESS |
| `score_commit_alice` | [transaction](https://explorer-studio.genlayer.com/tx/0xf2e3b8d1a04e7dca0a6ec373732556ca0d6ccb053497892b7f11347ca9b14fc3) | FINALIZED | SUCCESS | SUCCESS |
| `score_commit_bob` | [transaction](https://explorer-studio.genlayer.com/tx/0x87af4eed3cd79ae80789234966eb27c4531115eae9c3d6442dfe02779cc2126d) | FINALIZED | SUCCESS | SUCCESS |
| `score_commit_charlie` | [transaction](https://explorer-studio.genlayer.com/tx/0x941801168e883af6e09cdb4d5ed43c80c41003bcd095770be4a01854c36cd589) | FINALIZED | SUCCESS | SUCCESS |
| `score_forged_reveal` | [transaction](https://explorer-studio.genlayer.com/tx/0x0ac97eafd776af435c59367f3aef350155fc4db7c2781a6a31053dc8a4d4cb87) | FINALIZED | ERROR | EXPECTED ROLLBACK: reveal does not match |
| `score_reveal_alice` | [transaction](https://explorer-studio.genlayer.com/tx/0x6bdb6b21eff07a0fb76bc76f97b0689f70afeb8ef4b8c2b37e711b1f1821f051) | FINALIZED | SUCCESS | SUCCESS |
| `score_reveal_bob` | [transaction](https://explorer-studio.genlayer.com/tx/0x46273d26cdea696084777989fe07c11646c6fbcfde0d5c417fab58d6a4cee8a1) | FINALIZED | SUCCESS | SUCCESS |
| `score_reveal_charlie` | [transaction](https://explorer-studio.genlayer.com/tx/0x4d725ac2d9a56b35ff79d10e6bb940493fc4ea66e261d8d97bea3be2692dfec1) | FINALIZED | SUCCESS | SUCCESS |
| `score_resolve` | [transaction](https://explorer-studio.genlayer.com/tx/0xf2163890548a0274d2c9314f429ce6796e455d092dc4d550940c134b0d37a8ab) | FINALIZED | SUCCESS | SUCCESS |
| `score_settle` | [transaction](https://explorer-studio.genlayer.com/tx/0xf3d915d0c8000c86a29c0cab93f6318f1c2b459b9a248fb4c185b2066b236aa9) | FINALIZED | SUCCESS | SUCCESS |
| `score_withdraw_alice` | [transaction](https://explorer-studio.genlayer.com/tx/0x3164f1b4bbc3afe02459be91453a9ae1924c4d07b61a0dec7c3f743d8240375e) | FINALIZED | SUCCESS | SUCCESS |
| `score_withdraw_bob` | [transaction](https://explorer-studio.genlayer.com/tx/0xe0c7e4266fc3fe7b946ab5eaf6ebb8a8efb361b9c942993a11a13e01eb5b7ebf) | FINALIZED | SUCCESS | SUCCESS |
| `score_withdraw_charlie` | [transaction](https://explorer-studio.genlayer.com/tx/0xc6fe27607f5175606cb356b39da837839c18d89b6156148febe897ef446d4c4d) | FINALIZED | SUCCESS | SUCCESS |
| `score_duplicate_withdraw` | [transaction](https://explorer-studio.genlayer.com/tx/0x638521350397fb997292e06b386171df3a083a729a437796a21aa55f59bac128) | FINALIZED | ERROR | EXPECTED ROLLBACK: already been withdrawn |
| `expiry_deploy` | [transaction](https://explorer-studio.genlayer.com/tx/0x148f9677dd928bb860c058cb46ae87713b0177443933a670dd697165e4e66fc2) | FINALIZED | SUCCESS | SUCCESS |
| `expiry_commit_alice` | [transaction](https://explorer-studio.genlayer.com/tx/0xba32a11c3aa3eb4bc0751ab32c15ddd431fbae3566b4043830f74c8c68f45a0b) | FINALIZED | SUCCESS | SUCCESS |
| `expiry_commit_bob` | [transaction](https://explorer-studio.genlayer.com/tx/0x5e7ba8afcef686dc7cd40dbbd894e59a73025086a46870fc319526798c36963d) | FINALIZED | SUCCESS | SUCCESS |
| `expiry_reveal_alice` | [transaction](https://explorer-studio.genlayer.com/tx/0xcb2b84535e50f6797dfe19624334a2e67a6e4a7247e04cf1686f38ec1bcdd720) | FINALIZED | SUCCESS | SUCCESS |
| `expiry_too_early` | [transaction](https://explorer-studio.genlayer.com/tx/0x3eb47f9e83dc8ba463e1c35ceb566e4a5a6627449da82b2e086dfc2db0f21d87) | FINALIZED | ERROR | EXPECTED ROLLBACK: resolution deadline has not passed |
| `expiry_late_resolution` | [transaction](https://explorer-studio.genlayer.com/tx/0x2857e96d4720bb0e3cb3d4889d775ca5cd4f418e0e701ecd0638d6babc645e05) | FINALIZED | ERROR | EXPECTED ROLLBACK: resolution deadline has passed |
| `expiry_expire` | [transaction](https://explorer-studio.genlayer.com/tx/0x1d678975dcd1d2137defb9585876b6e10bdb967680beebf62b721bc3735eba30) | FINALIZED | SUCCESS | SUCCESS |
| `expiry_settle` | [transaction](https://explorer-studio.genlayer.com/tx/0xf308270cd3c07bacccf308bf60bc2d60e56e13f7aed635b103a775332a7729ca) | FINALIZED | SUCCESS | SUCCESS |
| `expiry_withdraw_alice` | [transaction](https://explorer-studio.genlayer.com/tx/0x15aa47bab302ec3d2775a2c6d6f0ec3f696fce6ab9df78bb984e2f9ec5bc2270) | FINALIZED | SUCCESS | SUCCESS |
| `expiry_withdraw_bob` | [transaction](https://explorer-studio.genlayer.com/tx/0xb5d9afe1b2cbf61d1afe2ff79c4a46c80e307e2aec6bbc4bf36629d513a1dee2) | FINALIZED | SUCCESS | SUCCESS |

## Recovery and limits

The background scoring run continued while a tool approval review hit a usage limit. The proposed driver adjustment was not executed. A later read-back hit HTTP 502 after the nonzero withdrawals had finalized. Recovery resumed from captured hashes and final state; recorded transactions were not rebroadcast. A zero-unit withdrawal and duplicate-withdrawal check completed before the expiry scenario. Exact frozen deadlines, transaction times and per-step read-backs are in the [release manifest](../deployments/studionet-release-2026-11-10.json).

These are synthetic ledger units, not native/token transfers. One successful semantic judgment and deterministic expiry evidence do not establish adversarial consensus robustness, formal security, or truthful-reporting incentives for pot-normalized scores. The repository remains local, no source/evidence was pushed, and the Portal was not used.
