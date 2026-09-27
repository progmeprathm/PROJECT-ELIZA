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
                elif "World Model" in system_prompt:
                    return '''
                    {
                      "entities": [
                        {
                          "name": "WebApp",
                          "type": "Entity",
                          "attributes": {"confidence": 0.9, "progress": "Planning", "status": "active"}
                        },
                        {
                          "name": "Fast Backend",
                          "type": "Goal",
                          "attributes": {"confidence": 0.8, "progress": "Pending", "status": "active"}
                        },
                        {
                          "name": "FastAPI",
                          "type": "Skill",
                          "attributes": {"confidence": 0.95, "progress": "Known", "status": "active"}
                        },
                        {
                          "name": "Async DB Connections",
                          "type": "Obstacle",
                          "attributes": {"confidence": 0.7, "progress": "Blocking", "status": "active"}
                        },
                        {
                          "name": "SQLAlchemy 2.0",
                          "type": "Belief",
                          "attributes": {"confidence": 0.85, "progress": "Validating", "status": "active"}
                        },
                        {
                          "name": "Tiny AWS EC2",
                          "type": "Constraint",
                          "attributes": {"confidence": 1.0, "progress": "Enforced", "status": "active"}
                        },
                        {
                          "name": "OOM Crash",
                          "type": "Event",
                          "attributes": {"confidence": 1.0, "progress": "Occurred", "status": "past"}
                        }
                      ],
                      "relationships": [
                        {"source": "WebApp", "target": "Fast Backend", "relation": "REQUIRES"},
                        {"source": "Fast Backend", "target": "FastAPI", "relation": "ENABLES"},
                        {"source": "FastAPI", "target": "Async DB Connections", "relation": "BLOCKS"},
                        {"source": "Fast Backend", "target": "SQLAlchemy 2.0", "relation": "BELIEVES"},
                        {"source": "WebApp", "target": "Tiny AWS EC2", "relation": "CONSTRAINED_BY"},
                        {"source": "WebApp", "target": "OOM Crash", "relation": "AFFECTED_BY"}
                      ]
                    }
                    '''
                # Otherwise, return a mock chat response
                return "This is ELIZA's Tertiary Mock Engine. Your cloud API key was invalid and Ollama is not running locally, so I am providing this offline fallback response!"
llm_router = LLMRouter()
