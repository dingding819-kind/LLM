"""
LLM Client for interacting with OpenAI or Vertex AI (Gemini)
"""
from typing import Optional, Dict, List
from config import (
    LLM_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS,
    GOOGLE_PROJECT_ID,
    GOOGLE_LOCATION,
    GEMINI_MODEL_NAME,
    GOOGLE_API_KEY,
    GENERATIVEAI_MODEL_NAME,
)

# Lazy imports inside client to avoid hard dependency


class LLMClient:
    """Client for LLM API interactions"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize LLM client
        
        Args:
            api_key: API key (OpenAI) if using OpenAI
            model: Model name (OpenAI or Gemini)
        """
        self.provider = LLM_PROVIDER.lower()
        
        if self.provider == "openai":
            self.api_key = api_key or OPENAI_API_KEY
            self.model = model or OPENAI_MODEL_NAME
        elif self.provider == "vertexai":
            self.api_key = None
            self.model = model or GEMINI_MODEL_NAME
        elif self.provider == "generativeai":
            self.api_key = api_key or GOOGLE_API_KEY
            self.model = model or GENERATIVEAI_MODEL_NAME
        else:
            self.api_key = None
            self.model = model or OPENAI_MODEL_NAME
        
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS
        self._init_provider()

    def _init_provider(self):
        if self.provider == "openai":
            try:
                import openai
                openai.api_key = self.api_key
                self._openai = openai
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
                self._openai = None
        elif self.provider == "vertexai":
            try:
                import vertexai
                from vertexai.generative_models import GenerativeModel
                self._GenerativeModel = GenerativeModel
                # Initialize Vertex AI with ADC or env credentials
                project = GOOGLE_PROJECT_ID or None
                location = GOOGLE_LOCATION or "us-central1"
                if project:
                    vertexai.init(project=project, location=location)
                else:
                    vertexai.init(location=location)
            except Exception as e:
                print(f"Error initializing Vertex AI client: {e}")
                self._GenerativeModel = None
        elif self.provider == "generativeai":
            try:
                import google.generativeai as genai
                api_key = self.api_key or __import__('os').getenv('GOOGLE_API_KEY')
                if api_key:
                    genai.configure(api_key=api_key)
                    self._genai = genai
                else:
                    print("Error: GOOGLE_API_KEY not set")
                    self._genai = None
            except Exception as e:
                print(f"Error initializing Google Generative AI client: {e}")
                self._genai = None
        else:
            print(f"Unknown LLM provider: {self.provider}")
            self._openai = None
            self._GenerativeModel = None
            self._genai = None

    def generate_text(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text using LLM
        
        Args:
            prompt: User prompt
            system_message: System message for context
            temperature: Sampling temperature
            max_tokens: Maximum response length
            
        Returns:
            Generated text response
        """
        if self.provider == "openai" and self._openai:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            try:
                response = self._openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature or self.temperature,
                    max_tokens=max_tokens or self.max_tokens
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"Error calling LLM: {str(e)}")
                return ""
        elif self.provider == "vertexai" and self._GenerativeModel:
            try:
                model = self._GenerativeModel(self.model)
                sys_prompt = system_message or ""
                full_prompt = (sys_prompt + "\n\n" + prompt).strip()
                resp = model.generate_content(
                    full_prompt,
                    generation_config={
                        "temperature": temperature or self.temperature,
                        "max_output_tokens": max_tokens or self.max_tokens,
                    },
                )
                return (resp.text or "").strip()
            except Exception as e:
                print(f"Error calling LLM (Vertex AI): {str(e)}")
                return ""
        elif self.provider == "generativeai" and self._genai:
            try:
                model = self._genai.GenerativeModel(self.model)
                sys_prompt = system_message or ""
                full_prompt = (sys_prompt + "\n\n" + prompt).strip()
                response = model.generate_content(
                    full_prompt,
                    generation_config=self._genai.types.GenerationConfig(
                        temperature=temperature or self.temperature,
                        max_output_tokens=max_tokens or self.max_tokens,
                    ),
                )
                return (response.text or "").strip()
            except Exception as e:
                print(f"Error calling LLM (Google Generative AI): {str(e)}")
                return ""
        else:
            print("LLM provider not initialized")
            return ""

    def generate_multiple(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        num_variations: int = 1
    ) -> List[str]:
        """
        Generate multiple variations of response
        
        Args:
            prompt: User prompt
            system_message: System message
            num_variations: Number of variations to generate
            
        Returns:
            List of generated responses
        """
        responses = []
        for _ in range(num_variations):
            response = self.generate_text(prompt, system_message)
            if response:
                responses.append(response)
        return responses

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Multi-turn conversation
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            Assistant response
        """
        if self.provider == "openai" and self._openai:
            try:
                response = self._openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"Error in chat: {str(e)}")
                return ""
        elif self.provider == "vertexai" and self._GenerativeModel:
            try:
                # Convert chat messages into a single prompt for simplicity
                prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
                model = self._GenerativeModel(self.model)
                resp = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": self.temperature,
                        "max_output_tokens": self.max_tokens,
                    },
                )
                return (resp.text or "").strip()
            except Exception as e:
                print(f"Error in chat (Vertex AI): {str(e)}")
                return ""
        else:
            print("LLM provider not initialized for chat")
            return ""

    def create_system_prompt(self, context: str, task: str) -> str:
        """
        Create a detailed system prompt
        
        Args:
            context: Context information
            task: Task description
            
        Returns:
            System prompt string
        """
        return f"""你是一位富有經驗的教育者，致力於幫助學生改進學習。

    背景信息：{context}

    任務：{task}

    請以清晰、簡潔且易於理解的方式回應。"""
