import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor
import asyncio

class GeminiController:
    def __init__(
            self, 
            apiKey: str, 
            modelName: str = 'gemini-1.5-flash', 
            systemInstruction: str = ''
        ):
        genai.configure(api_key=apiKey)
        self.model = genai.GenerativeModel(model_name=modelName)
        self.chat = self.model.start_chat(history=[])
        self.executor = ThreadPoolExecutor(max_workers=1)

        self.systemInstruction = systemInstruction # Manual systemInstruction

    def getAvailableModels(self):
            models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    models.append(m.name)
            return models

    def askSync(self, prompt: str):
        try:
            # Manual system instruction insertions
            response = self.chat.send_message(f'System:\n{self.systemInstruction}\n\nUser:\n{prompt}')
            return response.text
        except Exception as e:
            return f'Error: {e}'

    # Function to use in the GUI
    async def askGui(self, prompt: str):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.askSync, prompt)