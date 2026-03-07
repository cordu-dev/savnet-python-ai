"""
Strings Experiments - Comprehensive String Manipulation Guide
This file will help you understand everything about string operations in Python
"""

print("=" * 80)
print("STRINGS EXPERIMENTS - COMPREHENSIVE GUIDE")
print("=" * 80)
print()

# Experiment 1: String Creation and Basic Properties
print("EXPERIMENT 1: STRING CREATION AND BASIC PROPERTIES")
print("-" * 50)

# Different ways to create strings
string1 = "Hello World"
string2 = 'Python Programming'
string3 = """Multi-line
string example"""
string4 = str(42)  # Converting number to string

print(f"string1 (double quotes): '{string1}' | Type: {type(string1)} | Length: {len(string1)}")
print(f"string2 (single quotes): '{string2}' | Type: {type(string2)} | Length: {len(string2)}")
print(f"string3 (triple quotes): '{string3}' | Type: {type(string3)} | Length: {len(string3)}")
print(f"string4 (from number): '{string4}' | Type: {type(string4)} | Length: {len(string4)}")
print()

# Experiment 2: String Concatenation
print("EXPERIMENT 2: STRING CONCATENATION")
print("-" * 50)

base_string = "Hello"
number = 42
another_string = "World"

# Different concatenation methods
method1 = base_string + " " + another_string  # Simple concatenation
method2 = f"{base_string} {another_string}"  # f-string
method3 = "{} {}".format(base_string, another_string)  # format method
method4 = " ".join([base_string, another_string])  # join method
method5 = base_string + " " + str(number)  # Concatenating with number (must convert!)

print(f"Method 1 (+): '{method1}'")
print(f"Method 2 (f-string): '{method2}'")
print(f"Method 3 (.format): '{method3}'")
print(f"Method 4 (.join): '{method4}'")
print(f"Method 5 (with number): '{method5}'")
print()

# Experiment 3: String Indexing - The Core Concept
print("EXPERIMENT 3: STRING INDEXING - ACCESSING INDIVIDUAL CHARACTERS")
print("-" * 50)

sample = "PYTHON"
print(f"Sample string: '{sample}'")
print(f"Length of sample: {len(sample)}")
print()

print("INDEXING (single characters):")
print(f"sample[0] = '{sample[0]}'  | First character (index 0)")
print(f"sample[1] = '{sample[1]}'  | Second character (index 1)")
print(f"sample[2] = '{sample[2]}'  | Third character (index 2)")
print(f"sample[5] = '{sample[5]}'  | Last character (index 5)")
print()

print("NEGATIVE INDEXING (from the end):")
print(f"sample[-1] = '{sample[-1]}' | Last character (index -1)")
print(f"sample[-2] = '{sample[-2]}' | Second to last (index -2)")
print(f"sample[-6] = '{sample[-6]}' | First character (index -6)")
print()

# Experiment 4: String Slicing - The Most Powerful Tool
print("EXPERIMENT 4: STRING SLICING - EXTRACTING SUBSTRINGS")
print("-" * 50)

sample = "PYTHON PROGRAMMING"
print(f"Sample string: '{sample}'")
print(f"Length: {len(sample)}")
print()

print("BASIC SLICING [start:end]:")
print(f"sample[0:6] = '{sample[0:6]}'   | Characters 0 to 5 (6 is NOT included)")
print(f"sample[7:18] = '{sample[7:18]}' | Characters 7 to 17")
print(f"sample[0:4] = '{sample[0:4]}'   | First 4 characters")
print()

print("SLICING WITH OMITTED INDICES:")
print(f"sample[:6] = '{sample[:6]}'     | From beginning to index 5 (6 excluded)")
print(f"sample[7:] = '{sample[7:]}'     | From index 7 to end")
print(f"sample[:] = '{sample[:]}'       | Entire string (copy)")
print()

print("SLICING WITH NEGATIVE INDICES:")
print(f"sample[-11:-1] = '{sample[-11:-1]}' | Last 10 characters (excluding last)")
print(f"sample[-6:] = '{sample[-6:]}'   | Last 6 characters")
print(f"sample[:-7] = '{sample[:-7]}'   | All except last 7 characters")
print()

print("SLICING WITH STEP [start:end:step]:")
print(f"sample[::2] = '{sample[::2]}'   | Every 2nd character (even indices)")
print(f"sample[1::2] = '{sample[1::2]}'  | Every 2nd character starting from index 1")
print(f"sample[::3] = '{sample[::3]}'   | Every 3rd character")
print()

print("REVERSE SLICING:")
print(f"sample[::-1] = '{sample[::-1]}' | REVERSE the entire string")
print(f"sample[::-2] = '{sample[::-2]}' | Every 2nd character in reverse")
print(f"sample[5:2:-1] = '{sample[5:2:-1]}' | Reverse slice from index 5 to 3")
print()

# Experiment 5: String Methods - Transformation
print("EXPERIMENT 5: STRING METHODS - TRANSFORMATION")
print("-" * 50)

text = "Hello World! Python is AWESOME!"
print(f"Original: '{text}'")
print()

print("CASE TRANSFORMATION:")
print(f".upper(): '{text.upper()}'")
print(f".lower(): '{text.lower()}'")
print(f".title(): '{text.title()}'")
print(f".capitalize(): '{text.capitalize()}'")
print(f".swapcase(): '{text.swapcase()}'")
print()

print("WHITESPACE HANDLING:")
whitespace_text = "   Hello World!   "
print(f"Original with spaces: '{whitespace_text}'")
print(f".strip(): '{whitespace_text.strip()}' | Removes leading and trailing spaces")
print(f".lstrip(): '{whitespace_text.lstrip()}' | Removes leading spaces only")
print(f".rstrip(): '{whitespace_text.rstrip()}' | Removes trailing spaces only")
print()

# Experiment 6: String Methods - Searching and Testing
print("EXPERIMENT 6: STRING METHODS - SEARCHING AND TESTING")
print("-" * 50)

text = "Python Programming is Fun and Python is Powerful"
print(f"Sample text: '{text}'")
print()

print("SEARCHING METHODS:")
print(f".find('Python'): {text.find('Python')} | First occurrence index")
print(f".rfind('Python'): {text.rfind('Python')} | Last occurrence index")
print(f".find('Java'): {text.find('Java')} | Returns -1 if not found")
print(f".index('Fun'): {text.index('Fun')} | Like find() but raises error if not found")
print()

print("TESTING METHODS:")
print(f".startswith('Python'): {text.startswith('Python')}")
print(f".endswith('Powerful'): {text.endswith('Powerful')}")
print(f".isalpha(): {text.isalpha()} | All alphabetic characters?")
print(f".isdigit(): {text.isdigit()} | All digits?")
print(f".isalnum(): {text.isalnum()} | All alphanumeric?")
print(f".isspace(): {text.isspace()} | All whitespace?")
print()

# Experiment 7: String Methods - Splitting and Joining
print("EXPERIMENT 7: STRING METHODS - SPLITTING AND JOINING")
print("-" * 50)

csv_data = "apple,banana,cherry,date,elderberry"
print(f"CSV data: '{csv_data}'")
print()

print("SPLITTING:")
split_result = csv_data.split(',')
print(f".split(','): {split_result}")
print(f"Type of result: {type(split_result)}")
print()

sentence = "This is a sample sentence with multiple words"
print(f"Sentence: '{sentence}'")
words = sentence.split()
print(f".split(): {words}")
print(f"Number of words: {len(words)}")
print()

print("JOINING:")
words = ['Hello', 'beautiful', 'world']
joined1 = ' '.join(words)
joined2 = '-'.join(words)
joined3 = ''.join(words)

print(f"Words: {words}")
print(f"' '.join(words): '{joined1}'")
print(f"'-'.join(words): '{joined2}'")
print(f"'' .join(words): '{joined3}'")
print()

# Experiment 8: String Methods - Replacement and Cleaning
print("EXPERIMENT 8: STRING METHODS - REPLACEMENT AND CLEANING")
print("-" * 50)

text = "Hello World! Hello Python! Hello Programming!"
print(f"Original: '{text}'")
print()

print("REPLACEMENT:")
print(f".replace('Hello', 'Hi'): '{text.replace('Hello', 'Hi')}'")
print(f".replace('Hello', 'Hi', 2): '{text.replace('Hello', 'Hi', 2)}' | Replace only first 2")
print()

print("CHARACTER REMOVAL:")
dirty_text = "H-e-l-l-o- W-o-r-l-d-!"
print(f"Original with dashes: '{dirty_text}'")
print(f".replace('-', ''): '{dirty_text.replace('-', '')}' | Remove all dashes")
print()

# Experiment 9: Advanced String Operations
print("EXPERIMENT 9: ADVANCED STRING OPERATIONS")
print("-" * 50)

text = "Python123Programming456"
print(f"Original: '{text}'")
print()

print("FILTERING WITH COMPREHENSIONS:")
letters_only = ''.join([char for char in text if char.isalpha()])
numbers_only = ''.join([char for char in text if char.isdigit()])
print(f"Letters only: '{letters_only}'")
print(f"Numbers only: '{numbers_only}'")
print()

print("COUNTING CHARACTERS:")
char_count = {char: text.count(char) for char in set(text)}
print("Character frequency:")
for char, count in sorted(char_count.items()):
    print(f"  '{char}': {count}")
print()

# Experiment 10: String Formatting - Modern Approaches
print("EXPERIMENT 10: STRING FORMATTING - MODERN APPROACHES")
print("-" * 50)

name = "Alice"
age = 25
height = 1.65
is_student = True

print("F-STRING FORMATTING (recommended):")
print(f"Name: {name}, Age: {age}, Height: {height}m, Student: {is_student}")
print(f"Height with 2 decimals: {height:.2f}")
print(f"Age in 5 years: {age + 5}")
print(f"Name uppercase: {name.upper()}")
print()

print("FORMAT() METHOD:")
print("Name: {}, Age: {}, Height: {:.2f}m".format(name, age, height))
print("Name: {0}, Age: {1}, Height: {2:.2f}m".format(name, age, height))
print()

# Experiment 11: String Immutability - Important Concept!
print("EXPERIMENT 11: STRING IMMUTABILITY - CRITICAL CONCEPT")
print("-" * 50)

original = "Hello"
print(f"Original string: '{original}'")
print(f"ID of original: {id(original)}")

# This creates a NEW string, doesn't modify the original
modified = original + " World"
print(f"After concatenation: '{modified}'")
print(f"ID of modified: {id(modified)}")
print(f"Original still unchanged: '{original}'")
print()

# Experiment 12: Practical Examples
print("EXPERIMENT 12: PRACTICAL EXAMPLES")
print("-" * 50)

# Email validation example
email = "student@example.com"
print(f"Email: '{email}'")
print(f"Contains '@': {'@' in email}")
print(f"Ends with '.com': {email.endswith('.com')}")
print(f"Username part: '{email.split('@')[0]}'")
print(f"Domain part: '{email.split('@')[1]}'")
print()

# Phone number formatting
phone = "1234567890"
formatted_phone = f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
print(f"Original phone: {phone}")
print(f"Formatted phone: {formatted_phone}")
print()

# Text analysis
paragraph = "The quick brown fox jumps over the lazy dog. The fox is clever."
print(f"Paragraph: '{paragraph}'")
print(f"Word count: {len(paragraph.split())}")
print(f"Character count: {len(paragraph)}")
print(f"Number of 'the': {paragraph.lower().count('the')}")
print()

print("=" * 80)
print("END OF STRINGS EXPERIMENTS")
print("Run this file multiple times and experiment with the code!")
print("=" * 80)
