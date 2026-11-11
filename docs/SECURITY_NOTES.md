# Security notes

## Trust and authority

- The deployment sender freezes one question and all terms. There are no setters or privileged withdrawal rights.
- Forecaster identity is the normalized transaction sender. The commitment domain also binds question and contract. Salts must be generated privately off-chain and kept secret until reveal.
- Source text, questions and criteria are untrusted model data. Validators independently fetch the same URLs and classify each source; code derives the outcome. They compare all source labels and evidence bytes/digests, while validating every canonical stored leader quote separately. Different valid quote selection is accepted to preserve liveness; fabricated evidence is rejected. Case-sensitive quotation membership after whitespace normalization is enforced in code; semantic entailment still requires correct consensus judgment.
- Resolution/settlement are public triggers. Only a committed forecaster can withdraw their own allocation. Zero allocations also have one-shot withdrawal flags.

## Limits and failure behavior

- Stakes and payouts are synthetic ledger values, with no native/token custody, external balance debit or transfer. Real staking/payment rails are deliberately absent.
- HTTPS/public-DNS syntax validation matches the auction. It does not authenticate publishers, prove truth, resolve DNS safely against all rebinding scenarios, or police every redirect.
- Kept text is bounded to 5,000 bytes per URL, but the SDK fetches the whole response before slicing. Source records preserve original byte counts. Invalid UTF-8 in the retained prefix is unavailable; an incomplete character at the cut is removed without substitution.
- Any truncated required source forces terminal UNRESOLVABLE without calling the model, including when the retained prefix contains valid support. This rule applies only to this forecast pool.
- Any unavailable frozen source aborts resolution. Nothing from a failed attempt persists. After the frozen resolution deadline, anyone can call `expire_unresolved()` and then `settle()` for full refunds. This timeout requires no source availability, model call or owner authority; participants must still trigger expiry/settlement and their withdrawals.
- Valid UNRESOLVABLE is terminal. Unsupported quotations conservatively produce UNRESOLVABLE and full refunds; this cannot prove that the world event itself is undecidable.
- Malformed candidate/model output and consensus failures revert. Direct-mode validator mutation tests do not establish live malicious-validator behavior or network finality.
- Pool-normalized scores do not establish truthful-reporting incentives. Equal stakes and one commitment per address do not prevent Sybil participation or collusion.
- Historical source `6cc6b4f` has two StudioNet demo instances, including one successful real-source consensus judgment and deterministic expiry refunds. Native/token wallet integration, adversarial live consensus testing, formal verification and production security audit remain unverified.

The current local classification revision has not been pushed or deployed. Historical live receipts establish only the prior source, not this revision.
