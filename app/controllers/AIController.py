from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
import asyncio

from app.settings import SETTINGS

class AIController:
    def __init__(
        self, 
        apiKey: str, 
        modelName: str = None,
        systemInstruction: str = None
    ):
        self.client = OpenAI(
            api_key=apiKey,
            base_url=SETTINGS.OPENAIWRAPPER
        )

        self.modelName = modelName
        self.systemInstruction = systemInstruction

        self.messages = []

        if self.systemInstruction:
            self.messages.append({
                'role': 'system',
                'content': self.systemInstruction
            })

        self.executor = ThreadPoolExecutor(max_workers=1)

    def askSync(self, prompt: str):
        try:
            self.messages.append({
                'role': 'user',
                'content': prompt
            })

            response = self.client.chat.completions.create(
                model=self.modelName,
                messages=self.messages
            )

            reply = response.choices[0].message.content

            self.messages.append({
                'role': 'assistant',
                'content': reply
            })

            return reply
        except Exception as e:
            return f'Error: {e}'

    async def askAsync(self, prompt: str):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.askSync, prompt)

    def getModels(self):
        try:
            return [m.id for m in self.client.models.list().data]
        except Exception:
            return []