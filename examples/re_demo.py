#!/usr/bin/env python3
"""
Demo các chức năng của thư viện re
"""

import re

print("=" * 60)
print("THƯ VIỆN RE - DEMO CÁC CHỨC NĂNG")
print("=" * 60)

# ============================================================
# 1. re.compile() - Compile pattern
# ============================================================
print("\n1. re.compile() - Compile pattern")
print("-" * 60)

pattern = re.compile(r'module\s+(\w+)\s*\(([^)]*)\)\s*;')
print(f"Pattern compiled: {pattern}")

# ============================================================
# 2. re.search() - Tìm một match
# ============================================================
print("\n2. re.search() - Tìm một match")
print("-" * 60)

text = "module full_adder(a, b, cin, sum, cout);"
match = pattern.search(text)

if match:
    print(f"Full match: {match.group(0)}")
    print(f"Module name: {match.group(1)}")
    print(f"Port list: {match.group(2)}")
    print(f"Position: {match.span()}")
else:
    print("No match found")

# ============================================================
# 3. re.findall() - Tìm tất cả matches
# ============================================================
print("\n3. re.findall() - Tìm tất cả matches")
print("-" * 60)

text = "assign a = b; assign c = d; assign e = f;"
assign_pattern = re.compile(r'assign\s+(\w+)\s*=\s*(\w+)')
all_assigns = assign_pattern.findall(text)

print(f"Text: {text}")
print(f"All assigns (findall): {all_assigns}")
print(f"Number of matches: {len(all_assigns)}")

# ============================================================
# 4. re.finditer() - Iterator của matches
# ============================================================
print("\n4. re.finditer() - Iterator của matches")
print("-" * 60)

for i, match in enumerate(assign_pattern.finditer(text), 1):
    print(f"Match {i}:")
    print(f"  LHS: {match.group(1)}")
    print(f"  RHS: {match.group(2)}")
    print(f"  Position: {match.span()}")

# ============================================================
# 5. re.sub() - Replace text
# ============================================================
print("\n5. re.sub() - Replace text")
print("-" * 60)

text_with_comments = "module test(); // comment"
cleaned = re.sub(r'//.*$', '', text_with_comments)
print(f"Original: {text_with_comments}")
print(f"Cleaned: {cleaned}")

# ============================================================
# 6. Flags demo
# ============================================================
print("\n6. Flags demo")
print("-" * 60)

# DOTALL flag
multiline_text = """module test(
    a, b, c
);"""
pattern_dotall = re.compile(r'module\s+(\w+)\s*\(([^)]*)\)\s*;', re.DOTALL)
match_dotall = pattern_dotall.search(multiline_text)
if match_dotall:
    print(f"Multi-line match (with DOTALL):")
    print(f"  Module: {match_dotall.group(1)}")
    print(f"  Ports: {match_dotall.group(2).strip()}")

# IGNORECASE flag
pattern_ic = re.compile(r'test', re.IGNORECASE)
test_cases = ["TEST", "Test", "test"]
print(f"\nCase-insensitive matching:")
for case in test_cases:
    match = pattern_ic.search(case)
    print(f"  '{case}': {'Match' if match else 'No match'}")

# ============================================================
# 7. Character classes và quantifiers
# ============================================================
print("\n7. Character classes và quantifiers")
print("-" * 60)

# \w (word characters)
word_pattern = re.compile(r'\w+')
text_words = "module full_adder123();"
words = word_pattern.findall(text_words)
print(f"Words in '{text_words}': {words}")

# \d (digits)
digit_pattern = re.compile(r'\d+')
text_digits = "width = 32, depth = 128"
digits = digit_pattern.findall(text_digits)
print(f"Digits in '{text_digits}': {digits}")

# ============================================================
# 8. Non-greedy vs greedy
# ============================================================
print("\n8. Non-greedy vs greedy")
print("-" * 60)

text = "<tag>content1</tag><tag>content2</tag>"

# Greedy (*)
greedy = re.search(r'<tag>.*</tag>', text)
print(f"Greedy match: {greedy.group() if greedy else None}")
# Result: "<tag>content1</tag><tag>content2</tag>" (tất cả)

# Non-greedy (*?)
non_greedy = re.search(r'<tag>.*?</tag>', text)
print(f"Non-greedy match: {non_greedy.group() if non_greedy else None}")
# Result: "<tag>content1</tag>" (chỉ một)

print("\n" + "=" * 60)

