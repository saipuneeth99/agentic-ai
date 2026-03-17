"""Exception classes for the agentic system"""


class AgenticException(Exception):
    """Base exception for agentic system"""
    pass


class AgentExecutionError(AgenticException):
    """Raised when agent execution fails"""
    pass


class APIError(AgenticException):
    """Raised when API call fails"""
    pass


class ConfigurationError(AgenticException):
    """Raised when configuration is invalid"""
    pass


class ValidationError(AgenticException):
    """Raised when validation fails"""
    pass
