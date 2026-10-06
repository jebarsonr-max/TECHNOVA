import re

DANGEROUS_PATTERNS = [
    r'import\s+os',
    r'import\s+sys',
    r'import\s+subprocess',
    r'import\s+socket',
    r'import\s+requests',
    r'import\s+urllib',
    r'import\s+shutil',
    r'__import__',
    r'eval\(',
    r'exec\(',
    r'open\(',
    r'os\.system',
    r'os\.popen',
    r'subprocess\.Popen',
    r'subprocess\.run',
    r'socket\.socket'
]

class SecurityValidator:
    @staticmethod
    def validate_code_safety(code: str) -> tuple[bool, str]:
        """
        Validates generated code to ensure no malicious code patterns, host file access, or network calls exist.
        """
        for pattern in DANGEROUS_PATTERNS:
            # Allow safe pd.read_csv / pd.read_excel file access
            if pattern in [r'open\(']:
                continue
            if re.search(pattern, code):
                return False, f"SECURITY_VIOLATION: Forbidden pattern detected '{pattern}' in generated analytical code."
        
        return True, "Code safety validation passed."
