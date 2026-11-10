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
    commit = "0fb18b02c8ad56299d6a2910be0bab8ad601ef24"
    url = f"https://raw.githubusercontent.com/python/cpython/{commit}/Doc/whatsnew/3.12.rst"
    status, body, final_url = get(url)
    text = body[:5000].decode("utf-8")
    line = "Of note, the :mod:`!distutils` package has been removed from the standard library."
    assert status == 200 and line in text.splitlines()
    result = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "anonymous": True,
        "method": "GET; fresh urllib opener; no authorization or cookies",
        "upstream_release_tag": "v3.12.0",
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
