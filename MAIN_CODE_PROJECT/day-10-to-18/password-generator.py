"""
Secure Password Generator with Entropy-Based Strength Checker
Generates passwords with customizable character sets, scores strength,
and checks against common dictionary words.
"""

import random
import string
import math
import re


COMMON_WORDS = {
    'password', 'qwerty', 'letmein', 'admin', 'welcome', 'monkey', 'dragon',
    'master', 'login', 'sunshine', 'princess', 'baseball', 'football',
    'shadow', 'superman', 'batman', 'trustno1', 'abc123', 'iloveyou',
    'passw0rd', 'hello', 'secret', 'root', 'test', 'user', 'guest',
}

STRENGTH_LEVELS = [
    (0,   20,  "❌ Very Weak",   "Extremely easy to crack"),
    (20,  40,  "🔴 Weak",        "Easily cracked"),
    (40,  60,  "🟡 Moderate",    "Crackable with effort"),
    (60,  80,  "🟢 Strong",      "Reasonably secure"),
    (80,  100, "💪 Very Strong", "Highly secure"),
    (100, 999, "🔒 Excellent",   "Practically uncrackable"),
]


def generate_password(
    length=16,
    use_upper=True,
    use_lower=True,
    use_digits=True,
    use_symbols=True,
    exclude_ambiguous=False,
):
    if length < 4:
        raise ValueError("Minimum password length is 4.")

    pool = ""
    required = []

    if use_lower:
        chars = string.ascii_lowercase
        if exclude_ambiguous:
            chars = chars.replace('l', '').replace('o', '')
        pool += chars
        required.append(random.choice(chars))

    if use_upper:
        chars = string.ascii_uppercase
        if exclude_ambiguous:
            chars = chars.replace('I', '').replace('O', '')
        pool += chars
        required.append(random.choice(chars))

    if use_digits:
        chars = string.digits
        if exclude_ambiguous:
            chars = chars.replace('0', '').replace('1', '')
        pool += chars
        required.append(random.choice(chars))

    if use_symbols:
        chars = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        pool += chars
        required.append(random.choice(chars))

    if not pool:
        raise ValueError("At least one character set must be selected.")

    remaining = [random.choice(pool) for _ in range(length - len(required))]
    all_chars = required + remaining
    random.shuffle(all_chars)
    return ''.join(all_chars)


def calculate_entropy(password):
    """Entropy = log2(pool_size^length) = length * log2(pool_size)."""
    pool_size = 0
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password)
    has_other = any(
        c not in string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
        for c in password
    )

    if has_lower:  pool_size += 26
    if has_upper:  pool_size += 26
    if has_digit:  pool_size += 10
    if has_symbol: pool_size += 28
    if has_other:  pool_size += 32

    if pool_size == 0:
        return 0

    return len(password) * math.log2(pool_size)


def password_strength_score(password):
    score = 0
    issues = []
    bonuses = []

    # Length scoring
    if len(password) >= 20:
        score += 30; bonuses.append("Great length (20+)")
    elif len(password) >= 16:
        score += 25; bonuses.append("Good length (16+)")
    elif len(password) >= 12:
        score += 15
    elif len(password) >= 8:
        score += 8; issues.append("Short password (<12)")
    else:
        score += 2; issues.append("Very short password (<8)")

    # Character variety
    if re.search(r'[a-z]', password): score += 5
    else: issues.append("No lowercase letters")
    if re.search(r'[A-Z]', password): score += 5
    else: issues.append("No uppercase letters")
    if re.search(r'\d', password): score += 5
    else: issues.append("No digits")
    if re.search(r'[^a-zA-Z0-9]', password): score += 10; bonuses.append("Has symbols")
    else: issues.append("No special symbols")

    # Entropy bonus
    entropy = calculate_entropy(password)
    if entropy >= 80: score += 20; bonuses.append(f"High entropy ({entropy:.0f} bits)")
    elif entropy >= 60: score += 15
    elif entropy >= 40: score += 8
    else: issues.append(f"Low entropy ({entropy:.0f} bits)")

    # Penalty for common words
    lower_pw = password.lower()
    found_common = [w for w in COMMON_WORDS if w in lower_pw]
    if found_common:
        score -= 20
        issues.append(f"Contains common word(s): {found_common}")

    # Penalty for repeated chars
    if re.search(r'(.)\1{2,}', password):
        score -= 10; issues.append("Contains repeated characters (e.g. aaa)")

    # Penalty for sequential patterns
    sequences = ['0123456789', 'abcdefghijklmnopqrstuvwxyz', 'qwertyuiop']
    for seq in sequences:
        for i in range(len(seq) - 2):
            if seq[i:i+3] in lower_pw:
                score -= 5; issues.append(f"Contains sequence '{seq[i:i+3]}'")
                break

    return min(110, max(0, score)), issues, bonuses, entropy


def strength_label(score):
    for lo, hi, label, desc in STRENGTH_LEVELS:
        if lo <= score < hi:
            return label, desc
    return STRENGTH_LEVELS[-1][2], STRENGTH_LEVELS[-1][3]


def check_password(password):
    score, issues, bonuses, entropy = password_strength_score(password)
    label, desc = strength_label(score)

    print(f"\n  Password Analysis for: {'*' * min(len(password), 3) + password[3:]}")
    print(f"  Length    : {len(password)} characters")
    print(f"  Entropy   : {entropy:.1f} bits")
    print(f"  Score     : {score}/100")
    print(f"  Strength  : {label} — {desc}")

    bar_filled = int(score / 5)
    bar = '█' * bar_filled + '░' * (20 - bar_filled)
    print(f"  [{bar}] {score}%")

    if bonuses:
        print(f"\n  ✓ Strengths:")
        for b in bonuses: print(f"    + {b}")
    if issues:
        print(f"\n  ✗ Issues:")
        for issue in issues: print(f"    - {issue}")


def batch_generate(count=5, length=16, **kwargs):
    print(f"\n  Generated {count} passwords (length={length}):")
    print(f"  {'─'*55}")
    passwords = []
    for i in range(count):
        pw = generate_password(length=length, **kwargs)
        score, _, _, entropy = password_strength_score(pw)
        label, _ = strength_label(score)
        print(f"  {i+1:>2}. {pw:<30} {label}  ({entropy:.0f}b)")
        passwords.append(pw)
    print(f"  {'─'*55}")
    return passwords


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Password Generator & Checker v1.0     ║")
    print("╚══════════════════════════════════════════╝")

    batch_generate(5, 12)
    batch_generate(5, 20)

    test_passwords = [
        "password123", "abc", "P@ssw0rd!", "Xk7#mN2$qLp9@Rs5",
        "qwerty", "MySecureP@ss2024!", "aaaaaaa",
    ]
    print(f"\n  ── Strength Analysis ──")
    for pw in test_passwords:
        check_password(pw)

    print("\n  ── Interactive Mode ──")
    while True:
        choice = input("\n  [1] Generate  [2] Check strength  [3] Quit\n  Choice: ").strip()
        if choice == '3':
            break
        elif choice == '1':
            try:
                length = int(input("  Length (8-64): ") or "16")
                pw = generate_password(length=min(64, max(8, length)))
                print(f"  Generated: {pw}")
                check_password(pw)
            except ValueError as e:
                print(f"  Error: {e}")
        elif choice == '2':
            pw = input("  Enter password: ")
            check_password(pw)


if __name__ == "__main__":
    main()
