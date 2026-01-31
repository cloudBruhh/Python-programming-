"""Password Strength Analyzer - Defensive Security & User Education."""
import re
import math
import string
from dataclasses import dataclass


@dataclass
class AnalysisResult:
    """Container for password analysis results."""
    password_length: int
    entropy: float
    strength_score: int  # 0-100
    strength_label: str
    issues: list
    suggestions: list
    character_diversity: dict
    patterns_found: list


# Common password patterns and weak passwords
COMMON_PASSWORDS = {
    'password', '123456', '123456789', 'qwerty', 'abc123', 'password1',
    'admin', 'letmein', 'welcome', 'monkey', 'dragon', 'master',
    'login', 'princess', 'sunshine', 'flower', 'passw0rd', 'shadow',
    'iloveyou', 'trustno1', 'superman', 'batman', 'football', 'baseball'
}

KEYBOARD_PATTERNS = [
    'qwerty', 'qwertyuiop', 'asdfgh', 'asdfghjkl', 'zxcvbn', 'zxcvbnm',
    '1234567890', 'qazwsx', 'qweasd', '!@#$%^&*()'
]

COMMON_SUBSTITUTIONS = {
    'a': ['@', '4'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'],
    's': ['$', '5'], 't': ['7'], 'b': ['8'], 'g': ['9']
}


def calculate_entropy(password: str) -> float:
    """
    Calculate password entropy in bits.

    Entropy = L * log2(R)
    L = password length
    R = size of character pool used
    """
    charset_size = 0

    if any(c in string.ascii_lowercase for c in password):
        charset_size += 26
    if any(c in string.ascii_uppercase for c in password):
        charset_size += 26
    if any(c in string.digits for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += 32

    if charset_size == 0:
        return 0.0

    return len(password) * math.log2(charset_size)


def analyze_character_diversity(password: str) -> dict:
    """Analyze the character types present in the password."""
    return {
        'lowercase': sum(1 for c in password if c in string.ascii_lowercase),
        'uppercase': sum(1 for c in password if c in string.ascii_uppercase),
        'digits': sum(1 for c in password if c in string.digits),
        'symbols': sum(1 for c in password if c in string.punctuation),
        'spaces': sum(1 for c in password if c == ' '),
        'unique_chars': len(set(password))
    }


def detect_patterns(password: str) -> list:
    """Detect common weak patterns in the password."""
    patterns = []
    lower_pwd = password.lower()

    # Check for common passwords (including with substitutions)
    if lower_pwd in COMMON_PASSWORDS:
        patterns.append("Common password detected")

    # Check for keyboard patterns
    for pattern in KEYBOARD_PATTERNS:
        if pattern in lower_pwd or pattern[::-1] in lower_pwd:
            patterns.append(f"Keyboard pattern detected: '{pattern}'")

    # Check for repeated characters (e.g., 'aaa', '111')
    if re.search(r'(.)\1{2,}', password):
        patterns.append("Repeated characters detected (3+ in a row)")

    # Check for sequential numbers (e.g., '123', '321')
    if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
        patterns.append("Sequential numbers detected")
    if re.search(r'(098|987|876|765|654|543|432|321|210)', password):
        patterns.append("Reverse sequential numbers detected")

    # Check for sequential letters
    if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', lower_pwd):
        patterns.append("Sequential letters detected")

    # Check for date patterns (e.g., '1990', '2024')
    if re.search(r'(19|20)\d{2}', password):
        patterns.append("Possible year/date detected")

    # Check for leet speak substitutions of common words
    normalized = lower_pwd
    for char, subs in COMMON_SUBSTITUTIONS.items():
        for sub in subs:
            normalized = normalized.replace(sub, char)
    if normalized in COMMON_PASSWORDS:
        patterns.append("Common password with character substitutions")

    # Check for all same character type
    if password.isalpha():
        patterns.append("Only alphabetic characters used")
    elif password.isdigit():
        patterns.append("Only numeric characters used")

    # Check for common suffixes
    if re.search(r'(123|1234|!)$', password):
        patterns.append("Common suffix detected (123, 1234, !)")

    return patterns


def generate_suggestions(password: str, diversity: dict, patterns: list) -> list:
    """Generate actionable suggestions to improve password strength."""
    suggestions = []

    if len(password) < 12:
        suggestions.append("🔑 Increase length to at least 12 characters")

    if len(password) < 16:
        suggestions.append(
            "💡 Consider using 16+ characters for sensitive accounts")

    if diversity['lowercase'] == 0:
        suggestions.append("📝 Add lowercase letters (a-z)")

    if diversity['uppercase'] == 0:
        suggestions.append("🔠 Add uppercase letters (A-Z)")

    if diversity['digits'] == 0:
        suggestions.append("🔢 Add numbers (0-9)")

    if diversity['symbols'] == 0:
        suggestions.append("✨ Add special characters (!@#$%^&*)")

    if diversity['unique_chars'] < len(password) * 0.6:
        suggestions.append("🔄 Use more unique characters (avoid repetition)")

    if any("Common password" in p for p in patterns):
        suggestions.append(
            "🚫 Avoid common passwords - use a passphrase instead")

    if any("Keyboard pattern" in p for p in patterns):
        suggestions.append(
            "⌨️ Avoid keyboard patterns like 'qwerty' or 'asdf'")

    if any("Sequential" in p for p in patterns):
        suggestions.append("📊 Avoid sequential characters like '123' or 'abc'")

    if not suggestions:
        suggestions.append("✅ Great job! Consider using a password manager")

    return suggestions


def calculate_strength_score(password: str, entropy: float, patterns: list, diversity: dict) -> tuple:
    """Calculate overall strength score (0-100) and label."""
    score = 0

    # Length scoring (up to 30 points)
    score += min(30, len(password) * 2)

    # Entropy scoring (up to 30 points)
    score += min(30, entropy / 2)

    # Character diversity scoring (up to 20 points)
    diversity_types = sum(1 for k, v in diversity.items()
                          if k != 'unique_chars' and v > 0)
    score += diversity_types * 5

    # Uniqueness scoring (up to 20 points)
    uniqueness_ratio = diversity['unique_chars'] / max(len(password), 1)
    score += int(uniqueness_ratio * 20)

    # Penalty for patterns (subtract up to 40 points)
    score -= len(patterns) * 10

    # Ensure score is within bounds
    score = max(0, min(100, score))

    # Determine label
    if score >= 80:
        label = "🟢 Strong"
    elif score >= 60:
        label = "🟡 Moderate"
    elif score >= 40:
        label = "🟠 Weak"
    else:
        label = "🔴 Very Weak"

    return score, label


def analyze_password(password: str) -> AnalysisResult:
    """Perform complete password analysis."""
    entropy = calculate_entropy(password)
    diversity = analyze_character_diversity(password)
    patterns = detect_patterns(password)
    score, label = calculate_strength_score(
        password, entropy, patterns, diversity)
    suggestions = generate_suggestions(password, diversity, patterns)

    return AnalysisResult(
        password_length=len(password),
        entropy=round(entropy, 2),
        strength_score=score,
        strength_label=label,
        issues=patterns,
        suggestions=suggestions,
        character_diversity=diversity,
        patterns_found=patterns
    )


def print_analysis(result: AnalysisResult):
    """Display analysis results in a user-friendly format."""
    print("\n" + "=" * 50)
    print("        PASSWORD STRENGTH ANALYSIS")
    print("=" * 50)

    print(f"\n📏 Length: {result.password_length} characters")
    print(f"🔐 Entropy: {result.entropy} bits")
    print(f"💪 Strength: {result.strength_label} ({result.strength_score}/100)")

    print("\n📊 Character Breakdown:")
    print(f"   • Lowercase: {result.character_diversity['lowercase']}")
    print(f"   • Uppercase: {result.character_diversity['uppercase']}")
    print(f"   • Digits: {result.character_diversity['digits']}")
    print(f"   • Symbols: {result.character_diversity['symbols']}")
    print(
        f"   • Unique characters: {result.character_diversity['unique_chars']}")

    if result.issues:
        print("\n⚠️  Issues Found:")
        for issue in result.issues:
            print(f"   • {issue}")

    print("\n💡 Suggestions:")
    for suggestion in result.suggestions:
        print(f"   {suggestion}")

    # Educational note about entropy
    print("\n📚 About Entropy:")
    if result.entropy < 28:
        print("   Very low entropy - can be cracked in seconds")
    elif result.entropy < 36:
        print("   Low entropy - can be cracked in minutes to hours")
    elif result.entropy < 60:
        print("   Moderate entropy - may take days to months to crack")
    elif result.entropy < 80:
        print("   Good entropy - would take years to crack")
    else:
        print("   Excellent entropy - practically uncrackable with current technology")

    print("\n" + "=" * 50)


def main():
    """Interactive password analyzer."""
    print("\n🔒 Password Strength Analyzer")
    print("   Educational Tool for Defensive Security\n")

    # Example passwords to analyze
    test_passwords = [
        "password123",
        "Tr0ub4dor&3",
        "correct horse battery staple",
        "qwerty",
        "MyD0g$N@me!sMax2024"
    ]

    for pwd in test_passwords:
        print(f"\nAnalyzing: {'*' * len(pwd)} ({len(pwd)} chars)")
        result = analyze_password(pwd)
        print_analysis(result)
        input("\nPress Enter to continue...")

    # Interactive mode
    while True:
        print("\n" + "-" * 50)
        user_password = input(
            "Enter a password to analyze (or 'quit' to exit): ")

        if user_password.lower() == 'quit':
            print("\n👋 Stay secure!")
            break

        if user_password:
            result = analyze_password(user_password)
            print_analysis(result)


if __name__ == "__main__":
    main()
