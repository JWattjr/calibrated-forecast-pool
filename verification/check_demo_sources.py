"""Anonymous read-only source checks; no wallet, credentials, or runtime calls."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import urllib.request


def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": "calibrated-forecast-pool-source-check/1.0"})
    # An explicit empty proxy handler and a fresh opener avoid ambient proxy
    # credentials; no cookie processor or authorization handler is installed.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=45) as response:
        return response.status, response.read(), response.url


def main():
    commit = "0ada998ebbf392238719358432cd723a622fcd5e"
    url = f"https://raw.githubusercontent.com/python/cpython/{commit}/Doc/library/distutils.rst"
    status, body, final_url = get(url)
    text = body[:5000].decode("utf-8")
    line = "It was :ref:`removed in Python 3.12 <whatsnew312-removed-distutils>` after"
    assert status == 200 and len(body) == 667 and line in text.splitlines()
    assert hashlib.sha256(body).hexdigest() == "8c44b643a8a70ff7bd1c479b5b0b53088ece62f0c73e02bd6668af118a156076"
    result = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "anonymous": True,
        "method": "GET; fresh urllib opener; no authorization or cookies",
        "source_status": "fetched",
        "proposed_revision_not_deployed": True,
        "upstream_commit": commit,
        "sources": [{"url": url, "final_url": final_url, "http_status": status,
                     "byte_count": len(body), "kept_byte_count": len(body[:5000]),
                     "sha256": hashlib.sha256(body).hexdigest(),
                     "kept_sha256": hashlib.sha256(body[:5000]).hexdigest(),
                     "supporting_line": line, "supporting_line_in_kept_prefix": True,
                     "supporting_line_byte_offset": body.index(line.encode("utf-8")),
                     "supporting_line_end_byte_offset": body.index(line.encode("utf-8")) + len(line.encode("utf-8"))}],
        "demo_run": False,
    }
    output = Path(__file__).with_name("demo-source-checks.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
