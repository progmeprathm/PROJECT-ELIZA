from litellm import completion
import os

class LLMRouter:
    def __init__(self):
        # Default to an Open Source AI API (HuggingFace free inference) for initial application
        self.primary_model = "huggingface/HuggingFaceH4/zephyr-7b-beta"
        self.fallback_model = "ollama/llama3"

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            # Attempt Cloud Open Source API (HuggingFace Inference API often allows small free requests)
            response = completion(
                model=self.primary_model,
                messages=messages,
                api_key=os.environ.get("HUGGINGFACE_API_KEY", "") # Empty string allows anonymous requests if supported
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Cloud model failed ({e}). Falling back to local AI ({self.fallback_model})...")
            try:
                # Attempt Local Model (requires Ollama running on localhost:11434)
                response = completion(
                    model=self.fallback_model,
                    messages=messages,
                    api_base="http://localhost:11434"
                )
                return response.choices[0].message.content
            except Exception as fallback_e:
                print(f"Fallback model failed ({fallback_e}). Using Tertiary Mock Engine.")
                # If this is a planning request, return mock JSON so the UI doesn't crash
                if "Planner module" in system_prompt:
                    return '''
                    {
                        "plan_a": [
                            {"name": "Safe: Initialize Core Systems", "status": "pending"},
                            {"name": "Safe: Configure Database Schema", "status": "pending"}
                        ],
                        "plan_b": [
                            {"name": "Agile: Deploy API Endpoints immediately", "status": "pending"},
                            {"name": "Agile: Mock Database until later", "status": "pending"}
                        ]
                    }
                    '''
                # Otherwise, return a mock chat response
                return "This is ELIZA's Tertiary Mock Engine. Your cloud API key was invalid and Ollama is not running locally, so I am providing this offline fallback response!"
llm_router = LLMRouter()
