from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
import asyncio

# Needed import directly from package
from app import RELATIVES

class AIController:
    def __init__(
        self, 
        apiKey: str, 
        modelName: str = '',
        systemInstruction: str = ''
    ):
        self.client = OpenAI(
            api_key=apiKey,
            # Set wrapper URL
            base_url=RELATIVES.RelativesFile.get('ic-openai-wrapper')
        )

        self.modelName = modelName
        self.systemInstruction = systemInstruction

        # Messages
        self.messages = []

        # Set system instruction
        if self.systemInstruction:
            self.messages.append({
                'role': 'system',
                'content': self.systemInstruction
            })

        self.executor = ThreadPoolExecutor(max_workers=1)

    def askSync(self, prompt: str):
        try:
            # Add user prompt
            self.messages.append({
                'role': 'user',
                'content': prompt
            })

            response = self.client.chat.completions.create(
                model=self.modelName,
                messages=self.messages
            )

            reply = response.choices[0].message.content

            # Guardar respuesta del modelo
            self.messages.append({
                'role': 'assistant',
                'content': reply
            })

            return reply

        except Exception as e:
            return f'Error: {e}'

    # Function to ask when the UI is running
    async def askGui(self, prompt: str):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.askSync, prompt)

    # Function to get all models
    def getAvailableModels(self):
        try:
            # Get all models
            return [m.id for m in self.client.models.list().data]
        except Exception:
            return []