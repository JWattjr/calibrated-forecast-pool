# Test matrix

**112 parameter-expanded cases passed** for the current local source, SHA-256 `686e0530f616fee0794686f14c16ccafc0d73dfa22aa2915dc17aacfc128ca9a`. GenVM lint ran first and passed; the complete suite ran second. Exact output is in verification/lint.txt and verification/tests.txt; commands/tool versions are in verification/checks.json; expanded results are in verification/tests.xml.

These are mocked direct-mode tests, including explicit execution of captured validator callbacks. They establish local behavior under the approved fact-agreement/quote-selection design, not live consensus or finality. The exact source was subsequently pushed and freshly deployed under user authorization; separate live evidence is recorded below. No Portal action occurred.

| Invariant or behavior | Coverage |
|---|---|
| Per-source HOLDS / CONTRADICTED / UNCLEAR; code derives outcome | All nine two-source label combinations; missing classifications default UNCLEAR; every determinate source needs its own quote |
| Same headline with changed facts disagrees | Internally valid different source label with unchanged UNRESOLVABLE is rejected; changed label and consistent changed outcome are rejected |
| Different valid quote choices agree | Captured validator accepts an alternate genuine supporting passage against identical fetched evidence and source labels |
| Fabricated evidence is rejected | Forged quote rejected for determinate and UNCLEAR candidates; malformed quote schemas/bounds rejected; wrong case, short, unknown-source and missing support cannot authorize determinate labels |
| Quote filtering preserves other support | Invalid membership quotes dropped individually; same-source valid support keeps HOLDS/YES; only unsupported sources downgrade; only-invalid quotes are not stored |
| Canonical quote storage | Whitespace normalized and `(url, line)` sorted; unsorted or non-normalized leader records rejected; full-candidate equality across models is not required |
| Complete required evidence | Exact 5000-byte source can resolve; truncated source cannot resolve YES or NO even with retained valid support; any required truncated source skips the model and refunds revealed/unrevealed stakes |
| UTF-8 and source integrity | Exact cap, over cap, three-/four-byte cut, complete multibyte boundary; forged counts/status/digests/prefixes rejected even with rebound outer hashes |
| Unavailable evidence and failed consensus preserve state | Non-200, empty/whitespace, invalid UTF-8, network exceptions, one failed required source, simulated consensus failure; deadline refunds remain available |
| Sealed forecast domains and permissions | Sender/question/contract-bound commitments; copied and altered reveals fail; one commit/reveal; own entitlement only; public resolution, expiry and settlement |
| Deadline liveness | Strict constructor ordering; exact boundary behavior; early expiry and late resolution fail; permissionless expiry refunds both revealed and unrevealed stakes |
| Conserved deterministic payouts | 172/128/0 and reverse NO example; highest-score/address dust; unrevealed forfeiture; UNRESOLVABLE, empty, no-reveal and zero-score refunds; one withdrawal including zero |
| Frozen verified complete-source example | 667-byte pinned distutils snapshot and SHA-256 checked; HOLDS mock -> code-derived YES -> 172/128/0 -> zero held units |
| Input/model limits | Participant cap, stake/probability/salt/domain/URL/text/time bounds; unknown/duplicate source IDs and labels; model cannot supply outcome |

## Expanded results

| Test case | Result |
|---|---|
| `test_confident_correct_hedged_wrong_exact_payouts` | PASS |
| `test_no_outcome_reverses_scores` | PASS |
| `test_dust_tie_uses_lowest_address_with_unrevealed_pot` | PASS |
| `test_unrevealed_stake_is_forfeited` | PASS |
| `test_unresolvable_refunds_revealed_and_unrevealed_terminally` | PASS |
| `test_degenerate_pots_refund_in_full[nobody-revealed]` | PASS |
| `test_degenerate_pots_refund_in_full[zero-sum-YES]` | PASS |
| `test_degenerate_pots_refund_in_full[zero-sum-NO]` | PASS |
| `test_degenerate_pots_refund_in_full[empty-pool]` | PASS |
| `test_changed_salt_probability_duplicate_commit_reveal` | PASS |
| `test_copied_reveal_cannot_be_used_by_another_address` | PASS |
| `test_cross_question_and_cross_contract_reveal_reverts[question_id-another-question]` | PASS |
| `test_cross_question_and_cross_contract_reveal_reverts[contract_address-0x3434343434343434343434343434343434343434]` | PASS |
| `test_real_deployments_have_distinct_commitment_domains` | PASS |
| `test_deadline_edges_late_commit_late_reveal_and_early_resolution` | PASS |
| `test_failed_fetch_changes_no_state_and_can_retry[http-error]` | PASS |
| `test_failed_fetch_changes_no_state_and_can_retry[empty]` | PASS |
| `test_failed_fetch_changes_no_state_and_can_retry[whitespace]` | PASS |
| `test_failed_fetch_changes_no_state_and_can_retry[invalid-utf8]` | PASS |
| `test_failed_fetch_changes_no_state_and_can_retry[invalid-interior-at-limit]` | PASS |
| `test_one_failed_source_aborts_entire_resolution` | PASS |
| `test_fetch_boundaries_utf8_counts_and_digests[exactly-at-limit]` | PASS |
| `test_fetch_boundaries_utf8_counts_and_digests[over-limit]` | PASS |
| `test_fetch_boundaries_utf8_counts_and_digests[three-byte-cut]` | PASS |
| `test_fetch_boundaries_utf8_counts_and_digests[four-byte-cut]` | PASS |
| `test_fetch_boundaries_utf8_counts_and_digests[complete-multibyte-at-limit]` | PASS |
| `test_quote_only_past_cut_forces_unresolvable_refund` | PASS |
| `test_missing_invented_unavailable_short_or_wrong_case_quotes_are_unresolvable[quotes0]` | PASS |
| `test_missing_invented_unavailable_short_or_wrong_case_quotes_are_unresolvable[quotes1]` | PASS |
| `test_missing_invented_unavailable_short_or_wrong_case_quotes_are_unresolvable[quotes2]` | PASS |
| `test_missing_invented_unavailable_short_or_wrong_case_quotes_are_unresolvable[quotes3]` | PASS |
| `test_missing_invented_unavailable_short_or_wrong_case_quotes_are_unresolvable[quotes4]` | PASS |
| `test_missing_invented_unavailable_short_or_wrong_case_quotes_are_unresolvable[quotes5]` | PASS |
| `test_missing_invented_unavailable_short_or_wrong_case_quotes_are_unresolvable[quotes6]` | PASS |
| `test_missing_invented_unavailable_short_or_wrong_case_quotes_are_unresolvable[quotes7]` | PASS |
| `test_validator_rejects_mismatched_truncation_record_even_rebound` | PASS |
| `test_validator_compares_outcome_and_evidence_not_free_text` | PASS |
| `test_consensus_failure_changes_no_state_and_can_retry` | PASS |
| `test_malformed_model_result_reverts_unchanged[result0]` | PASS |
| `test_malformed_model_result_reverts_unchanged[result1]` | PASS |
| `test_malformed_model_result_reverts_unchanged[result2]` | PASS |
| `test_malformed_model_result_reverts_unchanged[result3]` | PASS |
| `test_malformed_model_result_reverts_unchanged[result4]` | PASS |
| `test_malformed_model_result_reverts_unchanged[result5]` | PASS |
| `test_malformed_model_result_reverts_unchanged[result6]` | PASS |
| `test_malformed_model_result_reverts_unchanged[result7]` | PASS |
| `test_access_control_lifecycle_and_frozen_terms` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides0-stake must]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides1-stake must]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides2-question ID length]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides3-question length]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides4-criterion length]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides5-bounded JSON]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides6-1-3 evidence]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides7-1-3 evidence]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides8-must be unique]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides9-bounded HTTPS]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides10-public DNS]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides11-bounded HTTPS]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides12-timezone offset]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides13-strictly ordered]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides14-strictly ordered]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides15-strictly ordered]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides16-strictly ordered]` | PASS |
| `test_frozen_input_size_and_schema_bounds[overrides17-timezone offset]` | PASS |
| `test_probability_and_salt_bounds[-1-private-test-salt-000001]` | PASS |
| `test_probability_and_salt_bounds[10001-private-test-salt-000001]` | PASS |
| `test_probability_and_salt_bounds[True-private-test-salt-000001]` | PASS |
| `test_probability_and_salt_bounds[5000-short]` | PASS |
| `test_probability_and_salt_bounds[5000-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx]` | PASS |
| `test_exact_stake_and_commitment_format_bounds` | PASS |
| `test_forecaster_cap_eight_and_max_stake` | PASS |
| `test_classification_normalization` | PASS |
| `test_network_exception_is_retryable_without_state_changes` | PASS |
| `test_model_response_text_limit_reverts_without_state_changes` | PASS |
| `test_valid_quote_in_kept_prefix_cannot_resolve_truncated_body[YES]` | PASS |
| `test_valid_quote_in_kept_prefix_cannot_resolve_truncated_body[NO]` | PASS |
| `test_whitespace_normalized_substring_quotes_are_accepted[quote-outer-whitespace]` | PASS |
| `test_whitespace_normalized_substring_quotes_are_accepted[source-outer-whitespace]` | PASS |
| `test_whitespace_normalized_substring_quotes_are_accepted[source-line-wrap]` | PASS |
| `test_whitespace_normalized_substring_quotes_are_accepted[quote-line-wrap]` | PASS |
| `test_whitespace_normalized_substring_quotes_are_accepted[partial-line]` | PASS |
| `test_whitespace_normalized_substring_quotes_are_accepted[eight-character-minimum]` | PASS |
| `test_expiry_before_or_at_resolution_deadline_reverts[2030-01-07T00:00:00Z]` | PASS |
| `test_expiry_before_or_at_resolution_deadline_reverts[2030-01-08T00:00:00Z]` | PASS |
| `test_expiry_after_deadline_refunds_revealed_and_unrevealed` | PASS |
| `test_resolution_after_deadline_reverts_without_fetch` | PASS |
| `test_resolution_at_final_deadline_is_allowed_and_cannot_expire_later` | PASS |
| `test_failed_fetch_can_expire_after_resolution_deadline` | PASS |
| `test_per_source_labels_deterministically_derive_outcome[labels0-YES]` | PASS |
| `test_per_source_labels_deterministically_derive_outcome[labels1-NO]` | PASS |
| `test_per_source_labels_deterministically_derive_outcome[labels2-UNRESOLVABLE]` | PASS |
| `test_per_source_labels_deterministically_derive_outcome[labels3-UNRESOLVABLE]` | PASS |
| `test_per_source_labels_deterministically_derive_outcome[labels4-UNRESOLVABLE]` | PASS |
| `test_per_source_labels_deterministically_derive_outcome[labels5-UNRESOLVABLE]` | PASS |
| `test_per_source_labels_deterministically_derive_outcome[labels6-UNRESOLVABLE]` | PASS |
| `test_per_source_labels_deterministically_derive_outcome[labels7-UNRESOLVABLE]` | PASS |
| `test_per_source_labels_deterministically_derive_outcome[labels8-UNRESOLVABLE]` | PASS |
| `test_missing_source_classifications_become_unclear[classifications0]` | PASS |
| `test_missing_source_classifications_become_unclear[classifications1]` | PASS |
| `test_each_determinate_source_needs_its_own_quote` | PASS |
| `test_validator_rejects_different_labels_even_with_same_unresolvable_outcome` | PASS |
| `test_validator_rejects_consistent_different_label_and_outcome` | PASS |
| `test_quotes_are_normalized_sorted_and_leader_must_be_canonical` | PASS |
| `test_fabricated_quote_is_rejected_even_for_unclear_leader` | PASS |
| `test_exactly_at_limit_complete_source_can_resolve` | PASS |
| `test_any_truncated_required_source_skips_model_and_refunds` | PASS |
| `test_verified_small_source_example_payouts` | PASS |
| `test_invalid_quote_dropped_while_same_source_valid_support_keeps_yes[False]` | PASS |
| `test_invalid_quote_dropped_while_same_source_valid_support_keeps_yes[True]` | PASS |
| `test_invalid_quotes_only_downgrade_unsupported_source` | PASS |
| `test_only_invalid_quotes_become_unclear_and_are_not_stored` | PASS |

## Historical live evidence

The November 10 StudioNet demos (24 finalized transactions: 20 SUCCESS, four expected ERROR) prove only historical source commit `6cc6b4f`. They do not prove this changed source. See LIVE_DEMO.md and the original release manifest for those historical records. A future authorized deployment requires a pushed exact source commit, fresh demos and separately verified Explorer contract links.

## Current separate live verification

Source commit `32bcc75839a09de2dfb55bda4a52f61c3adbe395` was pushed before fresh deployment. All 14 transactions finalized: 12 SUCCESS, two expected ERROR. Complete 667-byte evidence classified HOLDS, code derived YES, payouts were 172/128/0, and final accounting was stakes=300, paid=300, refunded=0, held=0. All seven view methods were read at the end. Direct Explorer contract evidence: [0x4e510d9f62d2632892BB84A52557b4573A94a2D6](https://explorer-studio.genlayer.com/address/0x4e510d9f62d2632892BB84A52557b4573A94a2D6). See LIVE_RELEASE_2026-11-11.md and the November 11 manifest. These observations are separate from the 112 mocked direct tests and are not an adversarial consensus audit.
