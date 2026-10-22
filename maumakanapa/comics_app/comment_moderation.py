import re


PROFANITY_PATTERN = re.compile(
    r"\b(?:asshole|bastard|bitch|bullshit|cunt|damn|dick|fuck|motherfucker|shit)\b",
    re.IGNORECASE,
)
THREAT_PATTERNS = (
    re.compile(r"\b(?:i(?:'| wi)?ll|i am going to|i'm going to)\s+(?:kill|hurt|attack)\b", re.IGNORECASE),
    re.compile(r"\b(?:kill|hurt|attack)\s+you\b", re.IGNORECASE),
)
URL_PATTERN = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)


def screen_comment(display_name, body):
    text = f"{display_name}\n{body}"
    reasons = []

    if PROFANITY_PATTERN.search(text):
        reasons.append("Possible profanity")
    if any(pattern.search(text) for pattern in THREAT_PATTERNS):
        reasons.append("Possible threat")
    if len(URL_PATTERN.findall(text)) >= 3:
        reasons.append("Multiple links (possible spam)")

    return reasons
