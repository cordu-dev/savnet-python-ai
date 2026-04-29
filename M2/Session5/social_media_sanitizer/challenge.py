def clean_whitespace(post: str) -> str:
    """Return a cleaned version of the post with normalized spacing."""
    pass


def censor_post(post: str, banned_words: list[str] | None = None) -> str:
    """Replace banned words with asterisks."""
    pass


def extract_hashtags(post: str) -> list[str]:
    """Return a list of hashtags found in the post, without the # symbol."""
    pass


def extract_mentions(post: str) -> list[str]:
    """Return a list of mentions found in the post, without the @ symbol."""
    pass


def is_spam(post: str) -> bool:
    """Return True if the post looks like spam based on simple rules."""
    pass


def validate_post(post: str, max_length: int = 280) -> dict:
    """Return validation details for the post."""
    pass


def sanitize_post(post: str) -> dict:
    """Run the full sanitizing pipeline and return the result."""
    pass


if __name__ == "__main__":
    banned_words = ["badword", "spam", "offensive"]

    sample_posts = [
        "  Hello   world  ",
        "BUY NOW!!! CLICK HERE!!! #sale #deal #offer #promo #wow #shop",
        "Hey @john_doe, are you joining #Python tonight?",
        "This post has badword inside it.",
    ]

    for post in sample_posts:
        print("-" * 40)
        print(f"Original: {post!r}")
        print(f"Whitespace cleaned: {clean_whitespace(post)!r}")
        print(f"Censored: {censor_post(post, banned_words)!r}")
        print(f"Hashtags: {extract_hashtags(post)}")
        print(f"Mentions: {extract_mentions(post)}")
        print(f"Spam: {is_spam(post)}")
        print(f"Validation: {validate_post(post)}")
        print(f"Sanitized: {sanitize_post(post)}")
