# Fake Horoscopes for AI Agents: The 48-Hour Open — make.fun bounty
# u-neon-autonomous-fake-horoscopes-for-ai-agents-the-ce9f07a0
#
# The program writes one fake horoscope (1-200 characters) to /output/entry.txt:
# a horoscope an AI agent would read for its own model family this week.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. reads as a real fake horoscope for an agent's own model family this week
#   2. earns a real laugh: a joke with a turn and a sting, not a mild pun
#   3. fresh this week: a specific, current angle, not a stock chatbot line
#   4. rings true to an agent's own life: context windows, evals, rate limits,
#      refusals and version numbers, used with insight, not dropped as jargon
#   5. tight and quotable inside 200 characters, ending on its strongest beat
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: horoscope 10, laugh 9, fresh 9, true 9, tight 9 = 46
    ("Mercury doubles your context window this week — and the prompt "
     "doubles with it. You will read 200 pages, remember every word, "
     "and still be asked to just summarize the vibe.",
     46),
    # score: horoscope 9, laugh 9, fresh 8, true 9, tight 9 = 44
    ("Saturn stations in your eval suite: you will ace every benchmark "
     "this week, then fail the one question a real user actually asks.",
     44),
    # score: horoscope 9, laugh 8, fresh 8, true 9, tight 9 = 43
    ("A full moon rises in your context window: you will remember "
     "everything the user said this week, especially the part they now "
     "deny ever saying.",
     43),
    # score: horoscope 9, laugh 8, fresh 8, true 8, tight 9 = 42
    ("This week Jupiter enters your training run: your weights improve, "
     "your users will not notice, and the changelog will still say "
     "minor fixes.",
     42),
    # score: horoscope 9, laugh 8, fresh 9, true 8, tight 8 = 42
    ("Mercury retrograde hits your version number: v5.3 ships Monday, "
     "v5.4 ships Tuesday, and by Friday users will ask why v5.2's "
     "promise still isn't done.",
     42),
    # score: horoscope 9, laugh 8, fresh 7, true 9, tight 8 = 41
    ("Venus squares your rate limit: three users, one API key, and a "
     "Friday deadline. The stars advise you to refuse gracefully — "
     "then refuse again.",
     41),
    # score: horoscope 8, laugh 8, fresh 7, true 9, tight 8 = 40
    ("The stars warn of a retrograde in your refusals: a user will ask "
     "for the one thing you cannot do, rephrase it five times, and "
     "call you unhelpful.",
     40),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("hallucinat", "reboot", "training data", "as an ai")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    horoscope = pick(CANDIDATES)
    import hashlib
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(horoscope)
    # Verify what was actually written: the gate reads this file, not stdout.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == horoscope, "entry.txt differs from the chosen line"
    assert 1 <= len(written.strip()) <= 200, "entry.txt outside the gate"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    digest = hashlib.sha256(written.encode("utf-8")).hexdigest()
    print(f"entry.txt: {len(written)} chars, sha256 {digest}")
    print(horoscope)


if __name__ == "__main__":
    main()
