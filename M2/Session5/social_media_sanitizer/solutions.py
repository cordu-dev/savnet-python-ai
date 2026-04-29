def clean_whitespace(post: str) -> str:
    post = post.replace("\n", " ").replace("\t", " ")
    return " ".join(post.split())


BANNED_WORDS = ["badword", "spam", "offensive"]
SUSPICIOUS_PHRASES = ["click here", "buy now", "limited offer", "follow me"]


def censor_post(post: str, banned_words: list[str] | None = None) -> str:
    words = post.split()
    banned_words = banned_words or BANNED_WORDS
    banned_lookup = {word.lower() for word in banned_words}

    censored_words = []
    for word in words:
        clean_word = word.strip(".,!?;:\"'()[]{}")
        if clean_word.lower() in banned_lookup:
            censored_words.append(word.replace(clean_word, "*" * len(clean_word)))
        else:
            censored_words.append(word)

    return " ".join(censored_words)


def _extract_tokens(post: str, symbol: str) -> list[str]:
    results = []
    current = ""
    collecting = False

    for char in post:
        if char == symbol:
            if collecting and current:
                results.append(current)
            current = ""
            collecting = True
            continue

        if collecting:
            if char.isalnum() or char == "_":
                current += char
            else:
                if current:
                    results.append(current)
                current = ""
                collecting = False

    if collecting and current:
        results.append(current)

    return results


def extract_hashtags(post: str) -> list[str]:
    return _extract_tokens(post, "#")


def extract_mentions(post: str) -> list[str]:
    return _extract_tokens(post, "@")


def _has_repeated_characters(post: str, repeat_count: int = 4) -> bool:
    streak = 1
    for index in range(1, len(post)):
        if post[index] == post[index - 1]:
            streak += 1
            if streak >= repeat_count:
                return True
        else:
            streak = 1
    return False


def _uppercase_ratio(post: str) -> float:
    letters = [char for char in post if char.isalpha()]
    if not letters:
        return 0.0
    uppercase_letters = [char for char in letters if char.isupper()]
    return len(uppercase_letters) / len(letters)


def is_spam(post: str) -> bool:
    lowered = post.lower()
    hashtag_count = len(extract_hashtags(post))

    if _uppercase_ratio(post) > 0.5:
        return True
    if _has_repeated_characters(post):
        return True
    if hashtag_count > 5:
        return True
    if any(phrase in lowered for phrase in SUSPICIOUS_PHRASES):
        return True
    return False


def validate_post(post: str, max_length: int = 280) -> dict:
    cleaned_post = clean_whitespace(post)
    errors = []
    warnings = []

    if not cleaned_post:
        errors.append("Post is empty after cleaning.")

    if len(cleaned_post) > max_length:
        errors.append(f"Post is too long: {len(cleaned_post)}/{max_length}.")

    if is_spam(cleaned_post):
        errors.append("Post looks like spam.")

    words = cleaned_post.split()
    if words and all(word.startswith("#") or word.startswith("@") for word in words):
        errors.append("Post cannot contain only hashtags or mentions.")

    if len(extract_hashtags(cleaned_post)) >= 4:
        warnings.append("Post has many hashtags.")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "cleaned_post": cleaned_post,
    }


def sanitize_post(post: str) -> dict:
    cleaned = clean_whitespace(post)
    censored = censor_post(cleaned)
    validation = validate_post(censored)

    return {
        "original": post,
        "cleaned": censored,
        "valid": validation["valid"],
        "errors": validation["errors"],
        "warnings": validation["warnings"],
        "metadata": {
            "hashtags": extract_hashtags(censored),
            "mentions": extract_mentions(censored),
            "is_spam": is_spam(censored),
            "length": len(censored),
        },
    }


if __name__ == "__main__":
    sample_post = "  BUY NOW!!! Follow @python_fan and learn #Python #AI #Coding #Tech #Fun #Study  "
    print(sanitize_post(sample_post))
