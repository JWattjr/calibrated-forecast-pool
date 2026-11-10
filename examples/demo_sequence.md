# Reproducible local sequence

Run `test_confident_correct_hedged_wrong_exact_payouts` in `tests/test_forecast_pool.py`. All web and model calls are mocked.

1. Owner deploys the frozen question using the nine-parameter constructor shape in `constructor.json`, including the final resolution deadline. The proposed live question asks whether CPython 3.12 stopped including distutils in its standard library; its pinned release documentation states the removal using different wording.
2. Three accounts commit equal 100-unit stakes with probabilities 10000, 5000 and 0, using distinct private random salts in a real client.
3. After the commit deadline, all reveal their own probabilities/salts by the reveal deadline.
4. After resolve-after and through resolution-deadline, anyone resolves the question. The local model mock returns YES with a quotation found in retained source text after whitespace normalization. If resolution never succeeds before the final deadline, anyone can expire the question and settle for full refunds instead.
5. Anyone settles. Scores 100000000, 75000000, 0 allocate floor payouts 171, 128, 0; the highest-score account gets the one-unit dust, producing 172, 128, 0.
6. Accounts withdraw their own allocations once. Accounting becomes stakes_in=300, paid_units=300, refunded_units=0, held_units=0. Repeated withdrawals fail.

For a future live proposal, see `docs/DEMO_PLAN.md`. The local example does not establish real source availability or validator consensus.
