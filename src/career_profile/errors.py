"""Domain-specific errors with actionable messages."""


class CareerProfileError(Exception):
    """Base error for user-correctable career profile failures."""


class DataLoadError(CareerProfileError):
    """Raised when canonical YAML cannot be loaded."""


class ValidationError(CareerProfileError):
    """Raised when cross-file validation fails."""


class RenderError(CareerProfileError):
    """Raised when a requested output cannot be rendered."""


class PdfEnvironmentError(CareerProfileError):
    """Raised when the local PDF environment is incomplete."""


class PrivacyError(CareerProfileError):
    """Raised when unsafe data is found in a public path."""
