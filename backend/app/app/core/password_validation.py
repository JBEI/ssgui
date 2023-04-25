from typing import Generator
import re


class StrongPasswordValidator:
    """
    Implements Password validation.

      - Minimum 10 characters
      - 1 lowercase letter
      - 1 uppercase letter
      - 1 number
      - 1 special character
    """

    lower = re.compile(r"[a-z]")
    upper = re.compile(r"[A-Z]")
    digit = re.compile(r"[0-9]")
    special = re.compile(r"[^a-zA-Z0-9]")

    def _checks_fail(self, password: str) -> Generator[bool, None, None]:
        yield len(password) < 10
        yield len(self.lower.findall(password)) < 1
        yield len(self.upper.findall(password)) < 1
        yield len(self.digit.findall(password)) < 1
        yield len(self.special.findall(password)) < 1

    def validate(self, password: str) -> None:
        if any(self._checks_fail(password)):
            raise ValueError(
                "Passwords must be at least 8 characters long, "
                "with at least one each of: Uppercase, lowercase, "
                "numeral, and special character."
            )


PasswordValidator = StrongPasswordValidator()
