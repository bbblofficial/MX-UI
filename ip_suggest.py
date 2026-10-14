# ip_suggest.py — random clean-address suggestions from ips.txt (IPv4 addresses and hostnames)
import ipaddress
import random
import re
from functools import lru_cache
from pathlib import Path

IPS_FILE = Path(__file__).parent / "ips.txt"
_HOST_RE = re.compile(r"^(?=.{1,253}$)(?!-)[a-z0-9-]{1,63}(?<!-)(\.[a-z0-9-]{1,63}(?<!-))+$", re.I)


def is_valid_address(value: str) -> bool:
    """True for an IP literal or a plain hostname. Used for both listing and pinning."""
    value = (value or "").strip()
    if not value:
        return False
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return bool(_HOST_RE.match(value))


@lru_cache(maxsize=1)
def load_ips() -> tuple[str, ...]:
    if not IPS_FILE.exists():
        return ()
    out, seen = [], set()
    for line in IPS_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or not is_valid_address(line):
            continue
        key = line.lower()
        if key not in seen:
            seen.add(key)
            out.append(line)
    return tuple(out)


def get_random_ips(count: int = 10) -> list[str]:
    pool = load_ips()
    count = max(1, min(int(count or 10), 50))
    if len(pool) <= count:
        return list(pool)
    return random.sample(pool, count)
