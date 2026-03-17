"""
Open-Source Model Configuration
These are free, self-hosted models - zero API costs
"""

from typing import Dict, Any
from enum import Enum


class ModelProvider(str, Enum):
    """Available open-source model providers"""
    OLLAMA = "ollama"  # Local open-source models
    HUGGING_FACE = "huggingface"  # HuggingFace hosted
    LLAMA = "llama"  # Llama models
    MISTRAL = "mistral"  # Mistral models
    GROQ = "groq"  # Free Groq API (limited)


# Recommended open-source models (no API costs)
OPEN_SOURCE_MODELS = {
    # Llama models (Meta) - Best performance
    "llama-2-13b": {
        "provider": ModelProvider.OLLAMA,
        "description": "Llama 2 13B - Balanced performance/speed",
        "speed": "medium",
        "quality": "high",
        "local": True,
    },
    "llama-2-70b": {
        "provider": ModelProvider.OLLAMA,
        "description": "Llama 2 70B - Best quality, slower",
        "speed": "slow",
        "quality": "very_high",
        "local": True,
    },
    
    # Mistral models - Fast and efficient
    "mistral-7b": {
        "provider": ModelProvider.OLLAMA,
        "description": "Mistral 7B - Fast and efficient",
        "speed": "fast",
        "quality": "high",
        "local": True,
    },
    
    # Neural Chat - Optimized for conversations
    "neural-chat": {
        "provider": ModelProvider.OLLAMA,
        "description": "Neural Chat - Conversation optimized",
        "speed": "fast",
        "quality": "medium",
        "local": True,
    },
    
    # Code Llama - For code generation
    "codellama": {
        "provider": ModelProvider.OLLAMA,
        "description": "CodeLlama - Specialized for code",
        "speed": "medium",
        "quality": "high",
        "local": True,
    },
    
    # Free alternative: Groq API (super fast, no local setup)
    "groq-mix": {
        "provider": ModelProvider.GROQ,
        "description": "Groq API - Free tier (limited)",
        "speed": "very_fast",
        "quality": "high",
        "local": False,
    },
}

# Default models for each agent role
AGENT_MODELS = {
    "frontend": {
        "default": "code-llama",
        "alternatives": ["mistral-7b", "neural-chat"],
        "prompt_focus": "HTML, CSS, JavaScript",
    },
    "backend": {
        "default": "llama-2-13b",
        "alternatives": ["mistral-7b", "code-llama"],
        "prompt_focus": "API design, database, Python",
    },
    "orchestrator": {
        "default": "llama-2-13b",
        "alternatives": ["mistral-7b"],
        "prompt_focus": "Planning, coordination, integration",
    },
}

# Configuration for Ollama setup
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",  # Default Ollama server
    "timeout": 300,  # 5 minutes
    "retry_attempts": 3,
    "temperature": 0.7,
    "top_p": 0.9,
}

# Configuration for Groq API (free alternative)
GROQ_CONFIG = {
    # Set GROQ_API_KEY environment variable
    "temperature": 0.7,
    "top_p": 1.0,
    "retry_attempts": 3,
}


def get_model_config(model_name: str) -> Dict[str, Any]:
    """Get configuration for a specific model"""
    return OPEN_SOURCE_MODELS.get(model_name, {})


def get_agent_models(agent_role: str) -> Dict[str, Any]:
    """Get recommended models for an agent role"""
    return AGENT_MODELS.get(agent_role, {})


SETUP_INSTRUCTIONS = """
SETUP INSTRUCTIONS FOR OPEN-SOURCE MODELS

Option 1: Use Ollama (Recommended - Local, No Cloud)
=========================================
1. Install Ollama: https://ollama.ai
2. Start Ollama: ollama serve
3. Pull models you want:
   - ollama pull llama2  (for general tasks)
   - ollama pull mistral  (for speed)
   - ollama pull codellama  (for code generation)
4. Models run locally on your machine - ZERO API costs

Option 2: Use Groq API (Free alternative - No setup)
====================================================
1. Get free API key: https://console.groq.com
2. Set environment variable: export GROQ_API_KEY="your-key"
3. Limited free tier (~500 calls/day)
4. Use if you don't have local GPU

Option 3: HuggingFace Inference API
===================================
1. Get free token: https://huggingface.co/settings/tokens
2. Use smaller models that fit in free tier
3. Best for experimenting

BENEFITS OF OPEN-SOURCE MODELS:
✓ Zero API costs
✓ No vendor lock-in
✓ Full data privacy
✓ Run on your infrastructure
✓ Customize models if needed
"""
