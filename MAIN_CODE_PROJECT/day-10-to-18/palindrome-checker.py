"""
Palindrome Checker and Generator for Strings and Numbers
Checks strings/numbers, finds palindromic substrings, generates next palindrome.
"""

import re


def is_string_palindrome(s):
    """Ignore spaces, punctuation, and case."""
    clean = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return clean == clean[::-1], clean


def is_number_palindrome(n):
    s = str(abs(int(n)))
    return s == s[::-1]


def find_palindromic_substrings(s):
    """Find all distinct palindromic substrings of length >= 2."""
    s = s.lower()
    found = set()
    n = len(s)

    def expand(l, r):
        while l >= 0 and r < n and s[l] == s[r]:
            sub = s[l:r+1]
            if len(sub) >= 2:
                found.add(sub)
            l -= 1
            r += 1

    for i in range(n):
        expand(i, i)      # odd-length
        expand(i, i + 1)  # even-length

    return sorted(found, key=lambda x: (-len(x), x))


def next_palindrome(n):
    """Find the smallest palindrome strictly greater than n."""
    candidate = n + 1
    while True:
        s = str(candidate)
        if s == s[::-1]:
            return candidate
        candidate += 1


def next_palindrome_fast(n):
    """Efficient method for next palindrome."""
    s = str(n + 1)
    length = len(s)
    half = (length + 1) // 2
    prefix = s[:half]

    def mirror(p, odd_len):
        if odd_len:
            return p + p[-2::-1]
        return p + p[::-1]

    mirrored = mirror(prefix, length % 2 == 1)
    if int(mirrored) > n:
        return int(mirrored)

    # Increment prefix
    prefix_n = str(int(prefix) + 1).zfill(half)
    if len(prefix_n) > half:
        # Length overflow: e.g., 999 → 1001
        new_len = length + 1
        result = '1' + '0' * (new_len - 2) + '1'
        return int(result)

    return int(mirror(prefix_n, length % 2 == 1))


def palindrome_number_range(start, end):
    """Find all palindrome numbers in a range."""
    return [n for n in range(start, end + 1) if is_number_palindrome(n)]


def longest_palindromic_substring(s):
    """Find the longest palindromic substring using expand-around-center."""
    s = s.lower()
    best_start, best_len = 0, 1

    def expand(l, r):
        nonlocal best_start, best_len
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if r - l + 1 > best_len:
                best_start = l
                best_len = r - l + 1
            l -= 1
            r += 1

    for i in range(len(s)):
        expand(i, i)
        expand(i, i + 1)

    return s[best_start:best_start + best_len]


def print_check(label, value, result):
    icon = "✓" if result else "✗"
    print(f"  {icon}  {label:<35} → {'Palindrome' if result else 'Not a palindrome'}")


def demo():
    print("\n  ── String Palindromes ──")
    strings = [
        "racecar", "hello", "A man a plan a canal Panama",
        "Was it a car or a cat I saw", "Never odd or even", "Python"
    ]
    for s in strings:
        result, clean = is_string_palindrome(s)
        icon = "✓" if result else "✗"
        print(f"  {icon}  \"{s[:35]:<35}\" (clean: {clean[:20]})")

    print("\n  ── Number Palindromes ──")
    numbers = [121, 1221, 12321, 123, 0, -121, 1001, 99999]
    for n in numbers:
        result = is_number_palindrome(n)
        print_check(str(n), n, result)

    print("\n  ── Palindromic Substrings ──")
    test_strings = ["abacaba", "racecar", "abcba"]
    for s in test_strings:
        subs = find_palindromic_substrings(s)
        longest = longest_palindromic_substring(s)
        print(f"\n  String: \"{s}\"")
        print(f"    Longest palindromic substring: \"{longest}\"")
        print(f"    All palindromic substrings ({len(subs)}): {subs[:10]}")

    print("\n  ── Next Palindrome Numbers ──")
    for n in [11, 99, 100, 999, 1000, 12321, 99999]:
        nxt = next_palindrome_fast(n)
        print(f"  After {n:<8} → {nxt}")

    print("\n  ── Palindromes in Range 1–200 ──")
    pals = palindrome_number_range(1, 200)
    print(f"  {pals}")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Palindrome Checker & Generator v1.0   ║")
    print("╚══════════════════════════════════════════╝")
    demo()

    print("\n  ── Interactive Mode ──")
    while True:
        choice = input("\n  [1] Check string  [2] Check number  [3] Substrings  [4] Next palindrome  [5] Quit\n  Choice: ").strip()
        if choice == '5':
            break
        elif choice == '1':
            s = input("  String: ")
            result, clean = is_string_palindrome(s)
            print(f"  {'✓ Palindrome' if result else '✗ Not a palindrome'} (cleaned: {clean})")
        elif choice == '2':
            try:
                n = int(input("  Number: "))
                print(f"  {'✓ Palindrome' if is_number_palindrome(n) else '✗ Not a palindrome'}")
            except ValueError:
                print("  Invalid number.")
        elif choice == '3':
            s = input("  String: ")
            subs = find_palindromic_substrings(s)
            print(f"  Found {len(subs)}: {subs[:15]}")
        elif choice == '4':
            try:
                n = int(input("  Number: "))
                print(f"  Next palindrome: {next_palindrome_fast(n)}")
            except ValueError:
                print("  Invalid number.")


if __name__ == "__main__":
    main()
