# Test matrix

November 11 review: the existing deployed behavior and recorded 85-test result are unchanged. Submission is held pending design confirmation for complete stored-field comparison, fail-closed truncated evidence and per-source classification with code-derived outcomes. See [the review and proposed design](SUBMISSION_REVIEW_2026-11-11.md). The public repository and anonymous-access verification are now available; historical build/live records below describe their original capture.

Run lint first, then `python -B -m pytest -vv -p no:cacheprovider --tb=short` from the project root using the pinned portfolio direct-test environment. Saved exact commands/output: `verification/lint.txt`, `verification/tests.txt`, `verification/schema.txt`, `verification/checks.json`. JUnit evidence: `verification/tests.xml`.

**85 parameter-expanded cases passed.** These are mocked direct-mode tests. Captured validator callbacks are explicitly invoked for honest/forged candidates; a thrown consensus disagreement is simulated. No real network consensus or deployment is established.

| Invariant or behavior | Test coverage |
|---|---|
| Confident correct out-earns hedged and wrong; exact 172/128/0 example and reverse NO case | `test_confident_correct_hedged_wrong_exact_payouts`, `test_no_outcome_reverses_scores` |
| All dust to highest score; ties use lowest address | Worked example plus `test_dust_tie_uses_lowest_address_with_unrevealed_pot` |
| Identity, question and contract bound; independent canonical hash reconstruction; copied reveal fails | Changed/copy/cross-domain/real-deployment tests |
| One commitment and reveal; late commit, early/late reveal, exact deadline edges | Duplicate and deadline tests |
| Resolution deadline strictly follows resolve-after; expiry only after deadline and only while OPEN; no resolution after deadline | Constructor deadline cases and expiry/late-resolution boundary tests |
| Expiry records RESOLUTION_DEADLINE with empty sources/quotes and refunds revealed/unrevealed stakes without web/model calls | `test_expiry_after_deadline_refunds_revealed_and_unrevealed`, `test_failed_fetch_can_expire_after_resolution_deadline` |
| Unrevealed stake forfeited for scored YES/NO; full refund for UNRESOLVABLE, no reveals or zero sum | Forfeiture, terminal UNRESOLVABLE and four degenerate cases |
| Only own payout withdrawn once, including zero; public resolution/settlement; immutable terms | Worked example and access-control/lifecycle tests |
| Fetch and consensus failure preserve state and allow retry | Five fetch failures, one partial-source failure, network exception and mocked consensus failure |
| Conservation at each lifecycle step and after reverts; claimed/unclaimed rows independently sum to counters | `accounting`, `unchanged` and lifecycle helpers; fixture teardown for every `pool` scenario |
| Exact cap, over cap, three-/four-byte cut, complete multibyte boundary | Five UTF-8 fetch boundary cases |
| Tail-only quote downgrades to UNRESOLVABLE; retained quote can resolve a truncated body | Tail/prefix quote tests |
| Whitespace and line-wrap normalization; partial-line substring matching; minimum eight normalized characters; case-sensitive rejection | Six accepted substring cases and missing/invented/unavailable/short/wrong-case quote cases |
| Source status/count/digest tampering rejected even with rebound outer hashes; independent re-fetch rejects coherent lies | `test_validator_rejects_mismatched_truncation_record_even_rebound` |
| Validators compare normalized outcome and bound evidence, while valid quotation selection may differ | `test_validator_compares_outcome_and_evidence_not_free_text`, normalization test |
| Question, criterion, URLs/JSON, timestamps, salt, probability, stake, commitment, queue, model response and quote bounds | Constructor/size/schema/format tests, 8-forecaster maximum-stake test |

## Expanded pass/fail results

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
| `test_outcome_normalization` | PASS |
| `test_network_exception_is_retryable_without_state_changes` | PASS |
| `test_model_response_text_limit_reverts_without_state_changes` | PASS |
| `test_valid_quote_in_kept_prefix_can_resolve_oversized_body` | PASS |
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


## Separate live verification

The authorized StudioNet run finalized 24 transactions: 20 successful executions and four expected rollbacks. The scoring instance paid 172/128/0; the separate expiry instance refunded revealed and unrevealed stakes. Both source identities and direct contract Explorer links were verified. See [LIVE_DEMO.md](LIVE_DEMO.md) and the release manifest. These live receipts are separate from the 85 mocked direct-mode test cases.
