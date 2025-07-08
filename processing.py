import math
import urllib.parse
import logging
logging.basicConfig(level=logging.INFO)

# Mock reputation table
REPUTATION = {
    "example.com": "good",
    "spam.com": "bad",
}


def compute_url_entropy(url: str) -> float:
    # Shannon entropy over path component
    path = urllib.parse.urlparse(url).path
    if not path:
        return 0.0
    freq = {}
    for ch in path:
        freq[ch] = freq.get(ch, 0) + 1
    entropy = 0.0
    length = len(path)
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy


def domain_of(sender: str) -> str:
    return sender.split("@")[-1].lower()


def process_signals(db, raw_record):
    logging.info(f"Processing signals for email ID: {raw_record.id}")
    # Domain reputation lookup
    dom = domain_of(raw_record.sender)
    reputation = REPUTATION.get(dom, "unknown")
    # Compute max entropy among all links
    entropies = [compute_url_entropy(u) for u in raw_record.links]
    max_entropy = max(entropies) if entropies else 0.0
    # Spoof check: simple match local-part vs. keep it dummy True
    spoof = raw_record.sender.endswith(f"@{dom}")
    # Save signal
    from models import EmailSignal
    sig = EmailSignal(
        raw_id=raw_record.id,
        domain_reputation=reputation,
        url_entropy=max_entropy,
        spoof_check=spoof
    )
    db.add(sig)
    db.commit()
