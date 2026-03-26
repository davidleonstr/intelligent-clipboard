from .relatives import RELATIVES
from .controllers import GeminiController
import pyperclip

class Combinations:
    @staticmethod
    async def interpret(key: str, modelName: str):
        # Prompt from config
        prompt = RELATIVES.prompt
        
        # Gemini Controller
        controller = GeminiController(
            apiKey=key, 
            modelName=modelName, 
            systemInstruction=prompt
        )

        # Content from Clipboard
        content = pyperclip.paste()

        # Reset
        content = await controller.askGui(content)

        # Set in clipboard
        pyperclip.copy(content)