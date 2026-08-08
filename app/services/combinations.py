import pyperclip

from app.controllers import AIController

class Combinations:
    @staticmethod
    async def interpret(apiKey: str, modelName: str, prompt: str):    
        controller = AIController(
            apiKey=apiKey, 
            modelName=modelName, 
            systemInstruction=prompt
        )

        action = pyperclip.paste()
        response = await controller.askAsync(action)

        pyperclip.copy(response)