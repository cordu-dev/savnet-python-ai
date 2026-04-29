ADVANCED_CHALLENGES = [
    "Extract URLs from a post and return them as a list.",
    "Create a function that removes emojis or counts how many emojis appear.",
    "Add a toxicity score from 0 to 100 based on simple rules.",
    "Support custom banned words entered by the user.",
    "Detect repeated posts by comparing normalized versions of messages.",
    "Build a menu-driven program where the user can test multiple posts.",
    "Write a function that summarizes a post if it is longer than 120 characters.",
    "Allow the validator to return separate moderation levels: safe, warning, blocked.",
]


GUIDING_QUESTIONS = [
    "Which part of the problem is pure string cleaning, and which part is validation?",
    "Can you reuse one helper function instead of repeating logic?",
    "What should happen with empty input or posts that contain only spaces?",
    "How can you make your code easier to test?",
    "If the platform rules change tomorrow, which part of your code should be easiest to update?",
]


if __name__ == "__main__":
    print("Advanced Challenges")
    for index, challenge in enumerate(ADVANCED_CHALLENGES, start=1):
        print(f"{index}. {challenge}")

    print("\nGuiding Questions")
    for index, question in enumerate(GUIDING_QUESTIONS, start=1):
        print(f"{index}. {question}")
