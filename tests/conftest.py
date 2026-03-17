"""Test configuration"""

import pytest


@pytest.fixture
def test_config():
    """Test configuration fixture"""
    return {
        "api_key": "test_key",
        "model": "test_model"
    }
