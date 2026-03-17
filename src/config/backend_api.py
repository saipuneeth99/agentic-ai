"""Backend API Client - Manages all LLM API calls with credit system"""

from typing import Optional, Dict, Any
from src.config import logger, settings


class BackendAPIClient:
    """
    Manages all API calls to LLM providers (Google, OpenAI, Anthropic).
    All calls use user credits instead of requiring personal API keys.
    """
    
    # Credit costs (per 1000 tokens)
    CREDIT_COSTS = {
        "gemini": 1.0,      # Google Gemini
        "gpt-4": 5.0,       # OpenAI GPT-4
        "gpt-3.5": 0.5,     # OpenAI GPT-3.5
        "claude": 3.0,      # Anthropic Claude
    }
    
    def __init__(self, user_manager):
        """Initialize with user manager for credit tracking"""
        self.user_manager = user_manager
        self.settings = settings
    
    def check_credits(self, model: str, estimated_tokens: int = 100) -> Dict[str, Any]:
        """Check if user has enough credits for an API call"""
        credits_needed = self._calculate_cost(model, estimated_tokens)
        
        credits_status = self.user_manager.get_credits()
        if not credits_status.get("success"):
            return {"available": False, "error": credits_status.get("error")}
        
        available = credits_status.get("credits", {}).get("available", 0)
        
        return {
            "available": available >= credits_needed,
            "required": credits_needed,
            "current_balance": available,
            "model": model
        }
    
    def _calculate_cost(self, model: str, tokens: int = 100) -> float:
        """Calculate credit cost for API call"""
        # Extract model base name
        model_base = model.lower().split("-")[0]
        
        base_cost = self.CREDIT_COSTS.get(model_base, 1.0)
        # Cost based on tokens used
        return (tokens / 1000) * base_cost
    
    def call_llm(self, 
                 model: str, 
                 prompt: str, 
                 system_prompt: Optional[str] = None,
                 **kwargs) -> Dict[str, Any]:
        """
        Call LLM with automatic credit deduction.
        This is a MOCK implementation - real version would call actual APIs.
        """
        
        # Check credits
        estimated_tokens = len(prompt.split()) + (len(system_prompt.split()) if system_prompt else 0)
        credits_check = self.check_credits(model, estimated_tokens)
        
        if not credits_check.get("available"):
            return {
                "success": False,
                "error": f"Insufficient credits. Need: {credits_check['required']}, Have: {credits_check['current_balance']}"
            }
        
        try:
            # MOCK: In production, this would call the actual LLM API
            response = self._mock_llm_call(model, prompt, system_prompt)
            
            # Deduct credits
            credits_needed = credits_check['required']
            self.user_manager.deduct_credits(
                credits_needed, 
                operation=f"llm_call_{model}"
            )
            
            logger.info(f"LLM call successful: {model} (Cost: {credits_needed} credits)")
            
            return {
                "success": True,
                "model": model,
                "response": response,
                "credits_used": credits_needed
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _mock_llm_call(self, model: str, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Mock LLM response for demo purposes"""
        return f"""Mock response from {model}:
        
System: {system_prompt or 'No system prompt'}
User: {prompt[:100]}...

This is a demonstration. In production, this would be an actual API response."""
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get user's API usage statistics"""
        credits = self.user_manager.get_credits()
        
        if not credits.get("success"):
            return {"error": "Not logged in"}
        
        credits_data = credits.get("credits", {})
        
        return {
            "user": self.user_manager.current_user,
            "plan": credits_data.get("plan", "starter"),
            "total_credits_allocated": credits_data.get("total_allocated", 0),
            "credits_used": credits_data.get("total_used", 0),
            "credits_remaining": credits_data.get("available", 0),
            "usage_percentage": credits_data.get("usage_percentage", 0),
        }
