# Map, Filter, Zip Activity Lab: Think Like an Engineer

This lab gives you 5 short challenges.

Your goal is not only to make the code work.
Your goal is to notice patterns, compare approaches, and build good engineering instincts.

## Problem 1: Clean the Guest List

You are given a list of names collected from a signup form:

```python
names = ["Ana", "", "Mihai", "  ", "Elena", "Bob", ""]
```

Use `filter()` to keep only the valid names.

### Your task

- Remove empty strings.
- Remove strings that contain only spaces.
- Convert the result to a list.
- Print the clean list.

### Stretch idea

After filtering, use `map()` to convert every valid name to uppercase.

---

## Problem 2: Build a Discount Report

An online shop has these prices:

```python
prices = [100, 250, 80, 40, 500]
```

Use `map()` to create a new list where every price has a 10% discount applied.

### Your task

- Create a mapped result with the discounted prices.
- Convert it to a list.
- Print both the original prices and the discounted prices.

### Stretch idea

Round every discounted value to 2 decimal places.

---

## Problem 3: Match Students with Scores

You have two lists:

```python
students = ["Mara", "Tudor", "Elena", "Darius"]
scores = [9, 7, 10, 8]
```

Use `zip()` to combine the data.

### Your task

- Pair each student with their score.
- Print sentences like:
  `Mara scored 9`
- Convert the `zip()` result to a list and print it.

### Stretch idea

Create a new list of strings such as:
`"Mara -> passed"`

Rule: a student passes if the score is at least `8`.

---

## Problem 4: Filter First, Then Transform

You are given daily temperatures:

```python
temperatures = [-3, 12, 18, -1, 25, 7]
```

You only want the non-negative temperatures, and then you want to convert them from Celsius to Fahrenheit.

### Your task

- Use `filter()` to keep only temperatures greater than or equal to `0`.
- Use `map()` on the filtered result.
- Convert the final result to a list.
- Print the Fahrenheit values.

Formula:

```python
fahrenheit = celsius * 9 / 5 + 32
```

### Stretch idea

Print each original valid Celsius temperature next to its Fahrenheit value.

---

## Problem 5: Build a Mini Product Summary

A shop stores data in three separate lists:

```python
products = ["Keyboard", "Mouse", "Monitor", "USB Cable"]
prices = [120, 45, 900, 25]
in_stock = [True, False, True, True]
```

Create a small product summary using `zip()`, `filter()`, and `map()`.

### Your task

- Use `zip()` to combine the product name, price, and stock status.
- Use `filter()` to keep only the products that are in stock.
- Use `map()` to turn each remaining product into a sentence like:
  `Keyboard costs 120 RON and is ready to order.`
- Print the final list.

### Stretch idea

Only keep in-stock products that cost less than `200`.

---

## Questions to Myself: Engineer Mindset

After solving the problems, pause and answer these questions in your own words.

### About correctness

- Did I actually understand what `map()`, `filter()`, and `zip()` return?
- Did I remember that these functions return iterators, not final lists?
- Did I accidentally consume an iterator and then try to reuse it?

### About design

- When is `map()` clearer than a `for` loop?
- When is a normal loop more readable than `map()` or `filter()`?
- Is my solution easy for another engineer to understand in 10 seconds?

### About data flow

- What is the input data?
- What is the transformation step?
- What is the filtering step?
- What is the final output shape?

### About debugging

- If my result is empty, which step should I inspect first?
- If my `zip()` output is shorter than expected, which iterable is probably the cause?
- If I get strange results, should I print intermediate steps before blaming the final line?

### About engineering habits

- Did I choose good variable names?
- Did I test with small example data first?
- What edge case could break my solution?
- If this data came from a real API or database, what assumptions would become dangerous?

---

## Bonus Challenge

Create your own mini pipeline using all three:

- `filter()` to keep useful data
- `map()` to transform it
- `zip()` to combine related values

Pick a theme you enjoy:

- games
- music
- shopping
- fitness
- movies

Then ask yourself:

**Is my code just working, or is it also clear, reliable, and easy to extend?**
