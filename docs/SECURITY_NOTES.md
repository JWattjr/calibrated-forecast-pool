# Security notes

## Trust and authority

- The deployment sender freezes one question and all terms. There are no setters or privileged withdrawal rights.
- Forecaster identity is the normalized transaction sender. The commitment domain also binds question and contract. Salts must be generated privately off-chain and kept secret until reveal.
- Source text, questions and criteria are untrusted model data. Validators independently fetch the same URLs and resolve the same frozen criterion. Exact quotation membership is enforced in code; semantic entailment still requires correct consensus judgment.
- Resolution/settlement are public triggers. Only a committed forecaster can withdraw their own allocation. Zero allocations also have one-shot withdrawal flags.

## Limits and failure behavior

- Stakes and payouts are synthetic ledger values, with no native/token custody, external balance debit or transfer. Real staking/payment rails are deliberately absent.
- HTTPS/public-DNS syntax validation matches the auction. It does not authenticate publishers, prove truth, resolve DNS safely against all rebinding scenarios, or police every redirect.
- Kept text is bounded to 5,000 bytes per URL, but the SDK fetches the whole response before slicing. Source records preserve original byte counts. Invalid UTF-8 in the retained prefix is unavailable; an incomplete character at the cut is removed without substitution.
- Any unavailable frozen source aborts resolution. Nothing from a failed attempt persists. Persistent outages can hold units indefinitely because no cancellation, timeout refund or recovery authority was requested.
- Valid UNRESOLVABLE is terminal. Unsupported quotations conservatively produce UNRESOLVABLE and full refunds; this cannot prove that the world event itself is undecidable.
- Malformed candidate/model output and consensus failures revert. Direct-mode validator mutation tests do not establish live malicious-validator behavior or network finality.
- Pool-normalized scores do not establish truthful-reporting incentives. Equal stakes and one commitment per address do not prevent Sybil participation or collusion.
- No deployment, wallet integration, live consensus test, formal verification or production security audit has been performed.
