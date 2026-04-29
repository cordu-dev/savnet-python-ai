# The Social Media Sanitizer Challenge

You are building a mini moderation tool for a new social media platform.

Your job is to help the platform clean messy posts, detect suspicious content, and extract useful information from text.

This challenge is all about practicing string manipulation in a real-world style problem.

## Why this challenge matters

Modern developers do not just write code that works.
They write code that handles messy input, thinks about edge cases, and is easy to improve later.

In this lab, students will practice:
- cleaning text data
- validating user input
- extracting patterns from strings
- combining small functions into a bigger workflow
- thinking analytically before coding

## The Story

A startup launches a tiny social media app.
Before a post goes live, it should be checked.
Some users write messy text with too many spaces.
Some users include hashtags and mentions.
Some users try spammy content like:

BUY NOW!!! CLICK HERE!!!

Your task is to create a small moderation system that helps process those posts.

## Main Goals

Students should build functions that can:
- clean extra whitespace
- censor banned words
- extract hashtags
- extract mentions
- detect likely spam
- validate whether a post is acceptable
- run a full sanitizing pipeline

## Required Functions

### 1. `clean_whitespace(post)`
Clean the text by normalizing spaces.

Expected behavior:
- remove spaces from the beginning and end
- replace multiple spaces with a single space
- handle tab characters and new lines

### 2. `censor_post(post, banned_words=None)`
Replace banned words with asterisks.

Expected behavior:
- matching should be case-insensitive
- preserve non-banned parts of the sentence
- ideally keep the same word length when censoring

### 3. `extract_hashtags(post)`
Return a list of hashtags found in the post.

Expected behavior:
- hashtags begin with `#`
- allowed hashtag content can include letters, numbers, and underscores
- return the hashtag text without the `#`

### 4. `extract_mentions(post)`
Return a list of mentions found in the post.

Expected behavior:
- mentions begin with `@`
- allowed mention content can include letters, numbers, and underscores
- return the mention text without the `@`

### 5. `is_spam(post)`
Return `True` if the post looks like spam, otherwise `False`.

Possible rules:
- too much uppercase text
- repeated characters like `!!!!!` or `heyyyyy`
- too many hashtags
- suspicious phrases such as `buy now` or `click here`

### 6. `validate_post(post, max_length=280)`
Validate the post and return structured feedback.

Expected behavior:
- reject empty posts
- reject posts that are too long
- reject spammy posts
- reject posts that contain only hashtags or mentions
- return useful feedback, not only `True` or `False`

### 7. `sanitize_post(post)`
Build the final pipeline.

This function should:
- clean the post
- censor banned words
- validate the final text
- extract metadata
- return one final structured result

## Analytical Thinking Markers

Before writing each function, students should stop and ask:

- What exactly is the input?
- What should the output look like?
- What are the edge cases?
- Should the check be case-sensitive or case-insensitive?
- What counts as invalid input?
- Can I split this into smaller helper functions?
- If requirements change later, will my code be easy to update?
- Am I solving the real problem, or only the easy happy path?

## Engineering Mindset Prompts

Use these as checkpoints during the lab:

### Data Cleaning
- What makes user text messy?
- What should be normalized first?
- What assumptions am I making about input?

### Validation
- What platform rules are strict errors?
- What should be a warning instead of a hard failure?
- Is my validation logic readable and reusable?

### Pattern Detection
- How do I know when a hashtag or mention starts?
- When should extraction stop?
- What punctuation should be ignored?

### Maintainability
- Am I repeating logic anywhere?
- Would a helper function make this cleaner?
- If I add URL detection later, where should that logic live?

## Suggested Test Posts

Use these ideas for testing:

- a normal clean post
- a post with extra spaces and line breaks
- a post with hashtags
- a post with mentions
- a post containing banned words
- a post written mostly in uppercase
- a post with many repeated punctuation marks
- a post containing only hashtags or mentions
- an empty string

## Output Idea

Students can return dictionaries like:
- whether the post is valid
- what errors were found
- what warnings were found
- the cleaned version of the post
- extracted hashtags and mentions
- spam status

## Optional Extensions

For stronger students, add one or more of these:
- extract URLs
- count emojis
- create a toxicity score from 0 to 100
- support custom moderation rules
- build a simple menu-driven app for testing posts
- assign moderation labels like `safe`, `warning`, and `blocked`

## Teaching Goal

This is not only a string exercise.
It is a software thinking exercise.

Students should learn to ask:
- What problem am I solving?
- What inputs can break my code?
- How do I design small, reusable functions?
- How do I turn messy text into trustworthy data?

## Final Challenge Prompt

Build a social media post sanitizer that can clean, inspect, and validate posts before they are published.

Your solution should be broken into small functions, tested with multiple examples, and written clearly enough that another developer can extend it later.

Think like a real engineer: not just about making it work, but about making it robust.
