import hashlib
import importlib
import json
from contextlib import contextmanager

import pytest


SDK = "v0.6.0-rc5"
URL = "https://releases.example.org/v1.txt"
URL_B = "https://archive.example.org/v1.txt"
LINE = "Release 1.0 was published on 2024-01-01."
COMMIT = "2030-01-01T12:00:00Z"
REVEAL = "2030-01-03T00:00:00Z"
RESOLVE = "2030-01-07T00:00:00Z"
SALT = "private-test-salt-000001"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value):
    return "sha256:" + hashlib.sha256(canonical(value).encode()).hexdigest()


def key(address):
    return "0x" + address.hex() if isinstance(address, bytes) else str(address).lower()


def deploy(vm, deployer, owner, **overrides):
    args = dict(question_id="release-1", question="Was release 1.0 published before 2024-02-01?",
                criterion="YES only if the source explicitly dates release 1.0 before 2024-02-01; NO if it explicitly dates it on or after that date; otherwise UNRESOLVABLE.",
                source_urls_json=json.dumps([URL]), stake_units=100,
                commit_deadline_iso="2030-01-02T00:00:00Z", reveal_deadline_iso="2030-01-05T00:00:00Z",
                resolve_after_iso="2030-01-06T00:00:00Z")
    args.update(overrides)
    vm.sender = owner
    vm.warp(COMMIT)
    return deployer("contracts/calibrated_forecast_pool.py", *args.values(), sdk_version=SDK)


def accounting(c):
    a = c.get_accounting()
    assert a["conserved"]
    assert a["stakes_in"] == a["paid_units"] + a["refunded_units"] + a["held_units"]
    assert min(a["paid_units"], a["refunded_units"], a["held_units"]) >= 0
    assert a["stakes_in"] == c.get_question()["forecaster_count"] * c.get_question()["stake_units"]
    if c.get_question()["status"] == "SETTLED":
        settlement = c.get_settlement()
        assert sum(settlement["allocations"].values()) == a["stakes_in"]
        unpaid = 0
        paid = refunded = 0
        for address, amount in settlement["allocations"].items():
            record = c.get_forecast(address)
            assert record["payout_units"] == amount
            if not record["withdrawn"]:
                unpaid += amount
            elif record["payment_kind"] == "REFUND":
                refunded += amount
            else:
                paid += amount
        assert (unpaid, paid, refunded) == (a["held_units"], a["paid_units"], a["refunded_units"])
    return a


@pytest.fixture
def pool(direct_vm, direct_deploy, direct_owner):
    c = deploy(direct_vm, direct_deploy, direct_owner)
    accounting(c)
    yield c
    accounting(c)


def state(c, addresses=()):
    return (c.get_question(), c.get_decision(), c.get_settlement(), accounting(c),
            [c.get_forecast(key(a)) for a in addresses])


@contextmanager
def unchanged(vm, c, error, addresses=()):
    before = state(c, addresses)
    with vm.expect_revert(error):
        yield
    assert state(c, addresses) == before


def commit(c, vm, address, p, salt=SALT):
    with vm.prank(address):
        c.commit_forecast(c.get_commitment_hash(p, salt), c.get_question()["stake_units"])
    accounting(c)
    return address, p, salt


def reveal(c, vm, row):
    with vm.prank(row[0]):
        c.reveal_forecast(row[1], row[2])
    accounting(c)


def mocks(vm, outcome="YES", body=None, quotes=None):
    vm.clear_mocks()
    vm.mock_web(r".*", {"status": 200, "body": body if body is not None else LINE + "\n"})
    if quotes is None:
        quotes = [{"url": URL, "line": LINE}] if outcome != "UNRESOLVABLE" else []
    # Same double encoding as auction: mock decodes once, legacy SDK parses again.
    vm.mock_llm(r"CALIBRATED FORECAST POOL RESOLUTION", json.dumps(json.dumps({"outcome": outcome, "quotes": quotes})))


def finish(c, vm, outcome="YES", **kwargs):
    vm.warp(RESOLVE)
    mocks(vm, outcome, **kwargs)
    c.resolve_question()
    accounting(c)
    assert vm.run_validator()
    result = c.settle()
    accounting(c)
    return result


def withdraw(c, vm, address):
    with vm.prank(address):
        amount = c.withdraw()
    accounting(c)
    return amount


def test_confident_correct_hedged_wrong_exact_payouts(pool, direct_vm, direct_alice, direct_bob, direct_charlie):
    rows = [commit(pool, direct_vm, a, p) for a, p in zip((direct_alice, direct_bob, direct_charlie), (10000, 5000, 0))]
    direct_vm.warp(REVEAL)
    for row in rows:
        reveal(pool, direct_vm, row)
    result = finish(pool, direct_vm)
    assert result["score_sum"] == 175_000_000
    assert result["dust_units"] == 1
    assert result["dust_recipient"] == key(direct_alice)
    assert result["allocations"] == {key(direct_alice): 172, key(direct_bob): 128, key(direct_charlie): 0}
    assert [withdraw(pool, direct_vm, a) for a in (direct_alice, direct_bob, direct_charlie)] == [172, 128, 0]
    assert accounting(pool)["held_units"] == 0
    with direct_vm.prank(direct_alice), unchanged(direct_vm, pool, "already been withdrawn"):
        pool.withdraw()
    with direct_vm.prank(direct_charlie), unchanged(direct_vm, pool, "already been withdrawn"):
        pool.withdraw()


def test_no_outcome_reverses_scores(pool, direct_vm, direct_alice, direct_bob, direct_charlie):
    rows = [commit(pool, direct_vm, a, p) for a, p in zip((direct_alice, direct_bob, direct_charlie), (10000, 5000, 0))]
    direct_vm.warp(REVEAL)
    for row in rows:
        reveal(pool, direct_vm, row)
    result = finish(pool, direct_vm, "NO")
    assert result["allocations"] == {key(direct_alice): 0, key(direct_bob): 128, key(direct_charlie): 172}
    for a in (direct_alice, direct_bob, direct_charlie):
        withdraw(pool, direct_vm, a)


def test_dust_tie_uses_lowest_address_with_unrevealed_pot(direct_vm, direct_deploy, direct_owner, direct_alice, direct_bob, direct_charlie):
    c = deploy(direct_vm, direct_deploy, direct_owner, stake_units=1)
    a = commit(c, direct_vm, direct_alice, 5000)
    b = commit(c, direct_vm, direct_bob, 5000)
    commit(c, direct_vm, direct_charlie, 10000)
    direct_vm.warp(REVEAL)
    reveal(c, direct_vm, a)
    reveal(c, direct_vm, b)
    result = finish(c, direct_vm)
    winner = min(key(direct_alice), key(direct_bob))
    assert result["dust_units"] == 1 and result["dust_recipient"] == winner
    assert result["allocations"][winner] == 2
    assert result["allocations"][key(direct_charlie)] == 0
    for address in (direct_alice, direct_bob, direct_charlie):
        withdraw(c, direct_vm, address)


def test_unrevealed_stake_is_forfeited(pool, direct_vm, direct_alice, direct_bob):
    a = commit(pool, direct_vm, direct_alice, 10000)
    commit(pool, direct_vm, direct_bob, 10000)
    direct_vm.warp(REVEAL)
    reveal(pool, direct_vm, a)
    assert finish(pool, direct_vm)["allocations"] == {key(direct_alice): 200, key(direct_bob): 0}
    assert withdraw(pool, direct_vm, direct_alice) == 200
    assert withdraw(pool, direct_vm, direct_bob) == 0


def test_unresolvable_refunds_revealed_and_unrevealed_terminally(pool, direct_vm, direct_alice, direct_bob):
    a = commit(pool, direct_vm, direct_alice, 7000)
    commit(pool, direct_vm, direct_bob, 10000)
    direct_vm.warp(REVEAL)
    reveal(pool, direct_vm, a)
    result = finish(pool, direct_vm, "UNRESOLVABLE")
    assert result["refund"]
    assert result["allocations"] == {key(direct_alice): 100, key(direct_bob): 100}
    for address in (direct_alice, direct_bob):
        assert withdraw(pool, direct_vm, address) == 100
    assert accounting(pool)["refunded_units"] == 200
    with unchanged(direct_vm, pool, "already been resolved"):
        pool.resolve_question()
    with unchanged(direct_vm, pool, "not yet settled"):
        pool.settle()


@pytest.mark.parametrize("mode", ["nobody-revealed", "zero-sum-YES", "zero-sum-NO", "empty-pool"])
def test_degenerate_pots_refund_in_full(pool, direct_vm, direct_alice, direct_bob, mode):
    addresses = [] if mode == "empty-pool" else [direct_alice, direct_bob]
    p = 10000 if mode == "zero-sum-NO" else 0
    rows = [commit(pool, direct_vm, address, p) for address in addresses]
    direct_vm.warp(REVEAL)
    if mode.startswith("zero-sum"):
        for row in rows:
            reveal(pool, direct_vm, row)
    result = finish(pool, direct_vm, "NO" if mode == "zero-sum-NO" else "YES")
    assert result["refund"] and result["score_sum"] == 0
    for address in addresses:
        assert withdraw(pool, direct_vm, address) == 100
    assert accounting(pool)["held_units"] == 0


def test_changed_salt_probability_duplicate_commit_reveal(pool, direct_vm, direct_alice):
    row = commit(pool, direct_vm, direct_alice, 7000)
    with direct_vm.prank(direct_alice), unchanged(direct_vm, pool, "only once", [direct_alice]):
        pool.commit_forecast("sha256:" + "a" * 64, 100)
    direct_vm.warp(REVEAL)
    with direct_vm.prank(direct_alice):
        for p, salt in [(7001, SALT), (7000, "changed-secret-salt-0001")]:
            with unchanged(direct_vm, pool, "does not match", [direct_alice]):
                pool.reveal_forecast(p, salt)
    reveal(pool, direct_vm, row)
    with direct_vm.prank(direct_alice), unchanged(direct_vm, pool, "already been revealed", [direct_alice]):
        pool.reveal_forecast(7000, SALT)


def test_copied_reveal_cannot_be_used_by_another_address(pool, direct_vm, direct_alice, direct_bob, direct_charlie):
    with direct_vm.prank(direct_alice):
        h = pool.get_commitment_hash(7000, SALT)
        pool.commit_forecast(h, 100)
    with direct_vm.prank(direct_bob):
        pool.commit_forecast(h, 100)
    direct_vm.warp(REVEAL)
    with direct_vm.prank(direct_bob), unchanged(direct_vm, pool, "does not match", [direct_alice, direct_bob]):
        pool.reveal_forecast(7000, SALT)
    with direct_vm.prank(direct_charlie), unchanged(direct_vm, pool, "no commitment"):
        pool.reveal_forecast(7000, SALT)


@pytest.mark.parametrize("field,other", [("question_id", "another-question"), ("contract_address", "0x" + "34" * 20)])
def test_cross_question_and_cross_contract_reveal_reverts(pool, direct_vm, direct_alice, field, other):
    with direct_vm.prank(direct_alice):
        # Independent reconstruction of the auction-style commitment format.
        actual = pool.get_commitment_hash(7000, SALT)
        caddr = str(direct_vm._contract_address).lower()
        if isinstance(direct_vm._contract_address, bytes):
            caddr = key(direct_vm._contract_address)
        payload = dict(question_id="release-1", contract_address=caddr, forecaster=key(direct_alice), probability_bps=7000, salt=SALT)
        assert digest(payload) == actual
        payload[field] = other
        pool.commit_forecast(digest(payload), 100)
    direct_vm.warp(REVEAL)
    with direct_vm.prank(direct_alice), unchanged(direct_vm, pool, "does not match", [direct_alice]):
        pool.reveal_forecast(7000, SALT)


def test_real_deployments_have_distinct_commitment_domains(direct_vm, direct_deploy, direct_owner, direct_alice):
    first = deploy(direct_vm, direct_deploy, direct_owner)
    with direct_vm.prank(direct_alice):
        h = first.get_commitment_hash(7000, SALT)
    importlib.import_module("genlayer.gl.genvm_contracts").__known_contract__ = None
    second = deploy(direct_vm, direct_deploy, direct_owner, question_id="release-2")
    with direct_vm.prank(direct_alice):
        assert second.get_commitment_hash(7000, SALT) != h
        second.commit_forecast(h, 100)
    direct_vm.warp(REVEAL)
    with direct_vm.prank(direct_alice), unchanged(direct_vm, second, "does not match", [direct_alice]):
        second.reveal_forecast(7000, SALT)
    accounting(second)


def test_deadline_edges_late_commit_late_reveal_and_early_resolution(pool, direct_vm, direct_alice, direct_bob, direct_charlie):
    a = commit(pool, direct_vm, direct_alice, 7000)
    commit(pool, direct_vm, direct_bob, 8000)
    direct_vm.warp("2030-01-02T00:00:00Z")
    with direct_vm.prank(direct_charlie), unchanged(direct_vm, pool, "commitment deadline"):
        pool.commit_forecast("sha256:" + "a" * 64, 100)
    with direct_vm.prank(direct_alice), unchanged(direct_vm, pool, "phase has not opened"):
        pool.reveal_forecast(7000, SALT)
    direct_vm.warp("2030-01-05T00:00:00Z")
    reveal(pool, direct_vm, a)
    direct_vm.warp("2030-01-05T00:00:01Z")
    with direct_vm.prank(direct_bob), unchanged(direct_vm, pool, "reveal deadline has passed"):
        pool.reveal_forecast(8000, SALT)
    direct_vm.warp("2030-01-06T00:00:00Z")
    with unchanged(direct_vm, pool, "resolve-after time has not passed"):
        pool.resolve_question()
    direct_vm.warp("2030-01-06T00:00:01Z")
    mocks(direct_vm)
    pool.resolve_question()
    accounting(pool)


@pytest.mark.parametrize("response", [
    pytest.param({"status": 503, "body": b"outage"}, id="http-error"),
    pytest.param({"status": 200, "body": b""}, id="empty"),
    pytest.param({"status": 200, "body": b" \n"}, id="whitespace"),
    pytest.param({"status": 200, "body": b"\xff"}, id="invalid-utf8"),
    pytest.param({"status": 200, "body": b"a" * 4998 + b"\xffxxx"}, id="invalid-interior-at-limit"),
])
def test_failed_fetch_changes_no_state_and_can_retry(pool, direct_vm, direct_alice, response):
    commit(pool, direct_vm, direct_alice, 9000)
    direct_vm.warp(RESOLVE)
    direct_vm.mock_web(r".*", response)
    with unchanged(direct_vm, pool, "fetch failed", [direct_alice]):
        pool.resolve_question()
    assert pool.get_sources() == {"sources": []}
    finish(pool, direct_vm, "UNRESOLVABLE")
    assert withdraw(pool, direct_vm, direct_alice) == 100


def test_one_failed_source_aborts_entire_resolution(direct_vm, direct_deploy, direct_owner, direct_alice):
    c = deploy(direct_vm, direct_deploy, direct_owner, source_urls_json=json.dumps([URL, URL_B]))
    commit(c, direct_vm, direct_alice, 10000)
    direct_vm.warp(RESOLVE)
    direct_vm.mock_web(r"releases\.example", {"status": 200, "body": LINE})
    direct_vm.mock_web(r"archive\.example", {"status": 404, "body": "missing"})
    with unchanged(direct_vm, c, "fetch failed"):
        c.resolve_question()


@pytest.mark.parametrize("body,expected_status,kept", [
    pytest.param(b"a" * 5000, "fetched", 5000, id="exactly-at-limit"),
    pytest.param(b"a" * 5001, "truncated", 5000, id="over-limit"),
    pytest.param(b"a" * 4999 + "\u20ac".encode() + b"tail", "truncated", 4999, id="three-byte-cut"),
    pytest.param(b"a" * 4997 + "\U0001f642".encode() + b"tail", "truncated", 4997, id="four-byte-cut"),
    pytest.param(b"a" * 4998 + "\u00e9".encode() + b"tail", "truncated", 5000, id="complete-multibyte-at-limit"),
])
def test_fetch_boundaries_utf8_counts_and_digests(pool, direct_vm, body, expected_status, kept):
    direct_vm.warp(RESOLVE)
    mocks(direct_vm, "UNRESOLVABLE", body=body)
    pool.resolve_question()
    source = pool.get_sources()["sources"][0]
    assert source["status"] == expected_status and source["available"] is True
    assert source["byte_count"] == len(body)
    assert source["kept_byte_count"] == kept
    assert source["text"].encode() == body[:kept]
    assert source["content_digest"] == "sha256:" + hashlib.sha256(body[:kept]).hexdigest()
    assert direct_vm.run_validator()


def test_quote_only_past_cut_forces_unresolvable_refund(pool, direct_vm, direct_alice):
    a = commit(pool, direct_vm, direct_alice, 10000)
    direct_vm.warp(REVEAL)
    reveal(pool, direct_vm, a)
    result = finish(pool, direct_vm, body=("a" * 5000 + "\n" + LINE + "\n").encode())
    assert result["outcome"] == "UNRESOLVABLE" and result["refund"]
    assert pool.get_decision()["resolution"]["quotes"] == []
    assert withdraw(pool, direct_vm, direct_alice) == 100


@pytest.mark.parametrize("quotes", [[], [{"url": URL, "line": "invented line"}],
                                      [{"url": URL_B, "line": LINE}], [{"url": URL, "line": "published on 2024-01-01."}]])
def test_missing_invented_unavailable_or_partial_line_quotes_are_unresolvable(pool, direct_vm, quotes):
    assert finish(pool, direct_vm, quotes=quotes)["outcome"] == "UNRESOLVABLE"


def rebind(candidate):
    result = json.loads(json.dumps(candidate))
    evidence = {"input_snapshot_digest": result["input_snapshot_digest"], "evidence": result["sources"]}
    result["evidence_digest"] = digest(evidence)
    result["snapshot_digest"] = digest({"input_snapshot_digest": result["input_snapshot_digest"], "evidence_digest": result["evidence_digest"]})
    return result


def test_validator_rejects_mismatched_truncation_record_even_rebound(pool, direct_vm):
    direct_vm.warp(RESOLVE)
    mocks(direct_vm, "UNRESOLVABLE", body=b"a" * 5001)
    pool.resolve_question()
    honest = pool.get_decision()
    assert direct_vm.run_validator()
    for field, value in [("status", "fetched"), ("status", "oversized"), ("byte_count", 5000),
                         ("byte_count", 5002), ("kept_byte_count", 4999), ("available", False),
                         ("content_digest", "sha256:" + "0" * 64)]:
        forged = json.loads(json.dumps(honest))
        forged["sources"][0][field] = value
        assert direct_vm.run_validator(leader_result=rebind(forged)) is False
    # Internally coherent prefix/count/digest still fails independent re-fetch.
    forged = json.loads(json.dumps(honest))
    source = forged["sources"][0]
    source["text"] = "b" * 5000
    source["content_digest"] = "sha256:" + hashlib.sha256(source["text"].encode()).hexdigest()
    assert direct_vm.run_validator(leader_result=rebind(forged)) is False


def test_validator_compares_outcome_and_evidence_not_free_text(pool, direct_vm):
    direct_vm.warp(RESOLVE)
    mocks(direct_vm, body=LINE + "\nVersion 1.0 release date: 2024-01-01.\n")
    pool.resolve_question()
    honest = pool.get_decision()
    alternate = json.loads(json.dumps(honest))
    alternate["resolution"]["quotes"] = [{"url": URL, "line": "Version 1.0 release date: 2024-01-01."}]
    assert direct_vm.run_validator(leader_result=alternate)
    for mutation in ("outcome", "quote", "snapshot", "extra"):
        forged = json.loads(json.dumps(honest))
        if mutation == "outcome":
            forged["resolution"]["outcome"] = "NO"
        elif mutation == "quote":
            forged["resolution"]["quotes"][0]["line"] = "fabricated"
        elif mutation == "snapshot":
            forged["input_snapshot_digest"] = "sha256:" + "0" * 64
        else:
            forged["extra"] = "not permitted"
        assert direct_vm.run_validator(leader_result=forged) is False


def test_consensus_failure_changes_no_state_and_can_retry(pool, direct_vm, direct_alice, monkeypatch):
    commit(pool, direct_vm, direct_alice, 7000)
    direct_vm.warp(RESOLVE)
    mocks(direct_vm)
    legacy = importlib.import_module("genlayer.gl.vm")
    def no_consensus(*args, **kwargs):
        raise legacy.UserError("[TRANSIENT] mocked consensus disagreement")
    with monkeypatch.context() as local:
        local.setattr(legacy, "run_nondet_unsafe", no_consensus)
        with unchanged(direct_vm, pool, "consensus disagreement", [direct_alice]):
            pool.resolve_question()
    finish(pool, direct_vm)
    assert withdraw(pool, direct_vm, direct_alice) == 100


@pytest.mark.parametrize("result", [
    {"outcome": "MAYBE", "quotes": []}, {"outcome": "YES", "quotes": [], "extra": 1},
    {"outcome": "YES", "quotes": [{"url": URL, "line": "x" * 1001}]},
    {"outcome": "YES", "quotes": [{"url": URL, "line": LINE}] * 7},
    {"outcome": "YES", "quotes": [{"url": URL, "line": LINE, "extra": 1}]},
])
def test_malformed_model_result_reverts_unchanged(pool, direct_vm, result):
    direct_vm.warp(RESOLVE)
    direct_vm.mock_web(r".*", {"status": 200, "body": LINE})
    direct_vm.mock_llm(r".*", json.dumps(json.dumps(result)))
    with unchanged(direct_vm, pool, "LLM_ERROR"):
        pool.resolve_question()


def test_access_control_lifecycle_and_frozen_terms(pool, direct_vm, direct_owner, direct_alice, direct_bob):
    frozen = pool.get_question()
    a = commit(pool, direct_vm, direct_alice, 10000)
    with direct_vm.prank(direct_owner), unchanged(direct_vm, pool, "settlement is required"):
        pool.withdraw()
    with unchanged(direct_vm, pool, "must be resolved"):
        pool.settle()
    direct_vm.warp(REVEAL)
    # Owner cannot reveal for Alice or withdraw Alice's allocation.
    with direct_vm.prank(direct_owner), unchanged(direct_vm, pool, "no commitment"):
        pool.reveal_forecast(10000, SALT)
    reveal(pool, direct_vm, a)
    direct_vm.sender = direct_bob  # Resolution and settlement are permissionless.
    finish(pool, direct_vm)
    with direct_vm.prank(direct_owner), unchanged(direct_vm, pool, "no commitment"):
        pool.withdraw()
    assert pool.get_forecast(key(direct_alice))["withdrawn"] is False
    for field in ("owner", "question_id", "question", "criterion", "source_urls", "stake_units", "commit_deadline", "reveal_deadline", "resolve_after"):
        assert pool.get_question()[field] == frozen[field]
    assert withdraw(pool, direct_vm, direct_alice) == 100
    with unchanged(direct_vm, pool, "not open"):
        pool.commit_forecast("sha256:" + "a" * 64, 100)
    with unchanged(direct_vm, pool, "not open"):
        pool.reveal_forecast(10000, SALT)


@pytest.mark.parametrize("overrides,message", [
    ({"stake_units": 0}, "stake must"), ({"stake_units": 10**12 + 1}, "stake must"),
    ({"question_id": "x" * 65}, "question ID length"), ({"question": "x" * 2001}, "question length"),
    ({"criterion": "x" * 2001}, "criterion length"),
    ({"source_urls_json": "[" + " " * 2501 + "]"}, "bounded JSON"),
    ({"source_urls_json": json.dumps([])}, "1-3 evidence"),
    ({"source_urls_json": json.dumps([URL] * 4)}, "1-3 evidence"),
    ({"source_urls_json": json.dumps([URL, URL])}, "must be unique"),
    ({"source_urls_json": json.dumps(["https://releases.example.org/" + "x" * 500])}, "bounded HTTPS"),
    ({"source_urls_json": json.dumps(["https://127.0.0.1/file"])}, "public DNS"),
    ({"source_urls_json": json.dumps(["http://example.org/file"])}, "bounded HTTPS"),
    ({"commit_deadline_iso": "2030-01-02T00:00:00"}, "timezone offset"),
    ({"resolve_after_iso": "2030-01-04T00:00:00Z"}, "strictly ordered"),
    ({"reveal_deadline_iso": "2030-01-02T00:00:00Z"}, "strictly ordered"),
])
def test_frozen_input_size_and_schema_bounds(direct_vm, direct_deploy, direct_owner, overrides, message):
    with direct_vm.expect_revert(message):
        deploy(direct_vm, direct_deploy, direct_owner, **overrides)


@pytest.mark.parametrize("p,salt", [(-1, SALT), (10001, SALT), (True, SALT), (5000, "short"), (5000, "x" * 129)])
def test_probability_and_salt_bounds(pool, direct_vm, direct_alice, p, salt):
    with direct_vm.prank(direct_alice), unchanged(direct_vm, pool, "EXPECTED"):
        pool.get_commitment_hash(p, salt)


def test_exact_stake_and_commitment_format_bounds(pool, direct_vm, direct_alice):
    with direct_vm.prank(direct_alice):
        for amount in (0, 99, 101, True):
            with unchanged(direct_vm, pool, "exact frozen stake"):
                pool.commit_forecast("sha256:" + "a" * 64, amount)
        for h in ("a" * 64, "sha256:" + "A" * 64, "sha256:" + "a" * 65):
            with unchanged(direct_vm, pool, "commitment must"):
                pool.commit_forecast(h, 100)


def test_forecaster_cap_eight_and_max_stake(direct_vm, direct_deploy, direct_owner):
    c = deploy(direct_vm, direct_deploy, direct_owner, stake_units=10**12)
    for i in range(1, 9):
        address = bytes([i]) * 20
        commit(c, direct_vm, address, 5000)
    with direct_vm.prank(bytes([9]) * 20), unchanged(direct_vm, c, "question is full"):
        c.commit_forecast("sha256:" + "a" * 64, 10**12)
    assert finish(c, direct_vm)["pot_units"] == 8 * 10**12
    for i in range(1, 9):
        assert withdraw(c, direct_vm, bytes([i]) * 20) == 10**12


def test_outcome_normalization(pool, direct_vm):
    assert finish(pool, direct_vm, outcome=" yes ")["outcome"] == "YES"


def test_network_exception_is_retryable_without_state_changes(pool, direct_vm, monkeypatch):
    direct_vm.warp(RESOLVE)
    web = importlib.import_module("genlayer.gl.nondet.web")
    def disconnected(*args, **kwargs):
        raise RuntimeError("mocked network disconnection")
    with monkeypatch.context() as local:
        local.setattr(web, "get", disconnected)
        with unchanged(direct_vm, pool, "fetch failed"):
            pool.resolve_question()
    finish(pool, direct_vm)


def test_model_response_text_limit_reverts_without_state_changes(pool, direct_vm):
    direct_vm.warp(RESOLVE)
    direct_vm.mock_web(r".*", {"status": 200, "body": LINE})
    direct_vm.mock_llm(r".*", json.dumps(" " * 8001))
    with unchanged(direct_vm, pool, "response is too large"):
        pool.resolve_question()


def test_valid_quote_in_kept_prefix_can_resolve_oversized_body(pool, direct_vm, direct_alice):
    row = commit(pool, direct_vm, direct_alice, 10000)
    direct_vm.warp(REVEAL)
    reveal(pool, direct_vm, row)
    body = (LINE + "\n" + "a" * 6000).encode()
    result = finish(pool, direct_vm, body=body)
    assert result["outcome"] == "YES" and not result["refund"]
    assert pool.get_sources()["sources"][0]["status"] == "truncated"
    assert withdraw(pool, direct_vm, direct_alice) == 100
