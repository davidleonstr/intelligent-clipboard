from .relatives import RELATIVES
from .controllers import ServiceController
import pyperclip

class Combinations:
    @staticmethod
    async def interpret(key: str, modelName: str):
        prompt = RELATIVES.prompt
        
        controller = ServiceController(
            apiKey=key, 
            modelName=modelName, 
            systemInstruction=prompt
        )

        content = pyperclip.paste()
        content = await controller.askGui(content)

        pyperclip.copy(content)