# 🎮 The Secret Message Decoder Challenge

Create a program that decodes secret messages using a multi-step encryption system. This challenge combines everything you've learned!

## The Problem

You've intercepted encrypted messages from a spy network. Each message has been encoded using a 3-layer encryption:

1. **Caesar Cipher**: Each letter is shifted by a key number
2. **Character Swap**: Pairs of characters are swapped based on a dictionary
3. **Reverse Chunks**: The message is split into chunks and reversed

Your mission: Build a decoder system with the following requirements:

## Requirements

### 1. Create a function `caesar_decode(text, shift)`
- Shifts each letter back by `shift` positions
- Preserves case (uppercase stays uppercase)
- Non-letters remain unchanged

### 2. Create a function `swap_decode(text, swap_dict)`
- Uses a dictionary to swap characters back
- Example: `{'@': 'a', '#': 'e'}` means @ becomes a, # becomes e

### 3. Create a function `reverse_chunks(text, chunk_size)`
- Splits text into chunks of `chunk_size`
- Reverses each chunk
- Handles leftover characters properly

### 4. Create a main function `decode_message(encrypted, shift, swap_dict, chunk_size)`
- Applies all three decoding steps in the correct order
- Handles exceptions (invalid inputs, empty strings, etc.)
- Returns the decoded message

### 5. Process multiple messages
- Store at least 3 encrypted messages in a list
- Use a loop to decode all messages
- Store results in a dictionary with message IDs as keys

## Test Data

```python
encrypted_messages = [
    "3r@c#S p0T",
    "n0thy1P s1 #m0s#w@",
    "!d1r0w 0ll#H"
]

shift = 1
swap_dict = {'@': 'a', '#': 'e', '0': 'o', '1': 'i'}
chunk_size = 3
```

## Bonus Challenges (Optional)
- Add input validation with try/except blocks
- Create a function that can also **encode** messages
- Allow user input for custom messages
- Calculate and display decoding statistics (time taken, character count, etc.)

## Expected Output Format
```
Decoding Message 1: [encrypted] -> [decoded]
Decoding Message 2: [encrypted] -> [decoded]
Decoding Message 3: [encrypted] -> [decoded]

Summary: X messages decoded successfully!
```

## Hints
- Think about the order of decoding (reverse the encryption process!)
- Use string slicing, loops, and dictionary methods
- The `ord()` and `chr()` functions are useful for Caesar cipher
- Test each function separately before combining them

---

This problem will challenge you to combine functions, loops, dictionaries, string manipulation, and exception handling into one cohesive program. Good luck, agent! 🕵️
