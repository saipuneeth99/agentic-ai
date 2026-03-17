"""
LLM Adapter - Unified interface for all models (open-source and proprietary)
"""

from typing import Optional, Dict, Any
from src.config import logger
from src.config.open_source_models import ModelProvider, OLLAMA_CONFIG


class LLMAdapter:
    """Adapter to use different LLM providers with unified interface"""
    
    def __init__(self, model: str, provider: Optional[str] = None):
        """Initialize LLM adapter
        
        Args:
            model: Model name (e.g., "llama-2-13b", "mistral-7b", "gpt-4")
            provider: Provider (ollama, groq, openai, etc). Auto-detected if not provided
        """
        self.model = model
        self.provider = provider or self._detect_provider(model)
        self.llm_client = None
        self._initialize_client()
    
    def _detect_provider(self, model: str) -> str:
        """Auto-detect provider based on model name"""
        model_lower = model.lower()
        
        if any(x in model_lower for x in ["llama", "mistral", "neural", "codellama"]):
            return "ollama"
        elif model_lower.startswith("gpt"):
            return "openai"
        elif "claude" in model_lower:
            return "anthropic"
        elif "gemini" in model_lower:
            return "google"
        elif "groq" in model_lower:
            return "groq"
        else:
            return "ollama"  # Default to ollama
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client"""
        try:
            if self.provider == "ollama":
                self._init_ollama()
            elif self.provider == "groq":
                self._init_groq()
            elif self.provider == "openai":
                self._init_openai()
            elif self.provider == "anthropic":
                self._init_anthropic()
            elif self.provider == "google":
                self._init_google()
            else:
                logger.warning(f"Unknown provider: {self.provider}, using mock client")
                self.llm_client = None
        except Exception as e:
            logger.warning(f"Failed to initialize {self.provider} client: {e}. Using mock.")
            self.llm_client = None
    
    def _init_ollama(self):
        """Initialize Ollama client (local open-source)"""
        try:
            # Check if ollama is available
            import requests
            response = requests.get(f"{OLLAMA_CONFIG['base_url']}/api/tags")
            if response.status_code == 200:
                self.llm_client = {
                    "type": "ollama",
                    "model": self.model,
                    "url": OLLAMA_CONFIG["base_url"]
                }
                logger.info(f"Initialized Ollama client with model: {self.model}")
            else:
                raise Exception("Ollama server not responding")
        except Exception as e:
            raise Exception(f"Ollama not available: {e}")
    
    def _init_groq(self):
        """Initialize Groq client (free API)"""
        try:
            import os
            from groq import Groq
            
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise Exception("GROQ_API_KEY environment variable not set")
            
            self.llm_client = Groq(api_key=api_key)
            logger.info(f"Initialized Groq client with model: {self.model}")
        except Exception as e:
            raise Exception(f"Groq initialization failed: {e}")
    
    def _init_openai(self):
        """Initialize OpenAI client (requires API key)"""
        try:
            from langchain_openai import ChatOpenAI
            self.llm_client = ChatOpenAI(model=self.model)
            logger.info(f"Initialized OpenAI client with model: {self.model}")
        except Exception as e:
            raise Exception(f"OpenAI initialization failed: {e}")
    
    def _init_anthropic(self):
        """Initialize Anthropic client (requires API key)"""
        try:
            from langchain_anthropic import ChatAnthropic
            self.llm_client = ChatAnthropic(model=self.model)
            logger.info(f"Initialized Anthropic client with model: {self.model}")
        except Exception as e:
            raise Exception(f"Anthropic initialization failed: {e}")
    
    def _init_google(self):
        """Initialize Google client (requires API key)"""
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.llm_client = ChatGoogleGenerativeAI(model=self.model)
            logger.info(f"Initialized Google client with model: {self.model}")
        except Exception as e:
            raise Exception(f"Google initialization failed: {e}")
    
    def call(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Call the LLM with a prompt
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            **kwargs: Additional parameters
            
        Returns:
            LLM response
        """
        if not self.llm_client:
            return self._mock_response(prompt)
        
        try:
            if self.provider == "ollama":
                return self._call_ollama(prompt, system_prompt, **kwargs)
            elif self.provider == "groq":
                return self._call_groq(prompt, system_prompt, **kwargs)
            else:
                # For LangChain clients (OpenAI, Anthropic, Google)
                return self._call_langchain(prompt, system_prompt, **kwargs)
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return self._mock_response(prompt)
    
    def _call_ollama(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Call Ollama model"""
        import requests
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = requests.post(
            f"{self.llm_client['url']}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
            },
            timeout=OLLAMA_CONFIG["timeout"]
        )
        
        if response.status_code == 200:
            return response.json()["message"]["content"]
        else:
            raise Exception(f"Ollama request failed: {response.text}")
    
    def _call_groq(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Call Groq API"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.llm_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
        )
        
        return response.choices[0].message.content
    
    def _call_langchain(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Call LangChain-based clients"""
        from langchain.prompts import ChatPromptTemplate
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt or "You are a helpful assistant."),
            ("human", prompt),
        ])
        
        chain = prompt_template | self.llm_client
        response = chain.invoke({})
        return response.content
    
    def _mock_response(self, prompt: str) -> str:
        """Generate mock response when no client is available"""
        return f"""Mock response from {self.model}:

The system would process your request:
"{prompt[:100]}..."

Note: This is a mock response because no LLM provider is configured.
To enable real responses, set up one of:
  1. Ollama (local) - https://ollama.ai
  2. Groq API - https://console.groq.com (free)
  3. Your existing API keys (OpenAI, Google, Anthropic)"""
