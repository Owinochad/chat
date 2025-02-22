import google.generativeai as genai

class GeniAIException(Exception):
    "GenAI Exception base class"
class ChatBot:
    "chat can only have one candidate count"
    CHATBOT_NAME = "Ukulima AI"

    def __init__(self,api_key):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel('gemini-pro')
        self.conversation = None
        self.conversation_history = []

        self.preload_conversation() 

    def send_prompt(self, prompt, temprature=0.1):
        if temprature<0 or temprature>1:
            raise GeniAIException('Temprature must be between 0 and 1')
        
        if not prompt:
            raise GeniAIException('Prompt cannot be empty')
        
        try:
            response = self.conversation.send_message(
                content = prompt,
                generation_config=self._generation_config(temprature),
            )
            response.resolve()
            return f'{response.text}\n' + '---' * 20
            
        except Exception as e:
            raise GeniAIException(str(e))
    @property
    def history(self):
        conversation_history= [
            {'role':message.role, 'text': message.parts[0].text} for message in self.conversation.history
        ]

    def clear_conversation(self):
        self.conversation = self.start_chat(history=[])
    def start_conversation(self):
        self.conversation = self.model.start_chat(history=self.conversation_history)
    
    
    def _generation_config(self, temperature):
        return genai.types.GenerationConfig(
        temperature=temperature
    )

    def _construct_message(self, text, role='user'):
        return{
            'role': role,
            'parts': [text]
        }
    
    def preload_conversation(self, conversation_history=None):
        if isinstance(conversation_history, list):
            self._coversation_history = conversation_history
        else:
            self._coversation_history = [
    self._construct_message('From now on, return the output as a JSON object that can be loaded in python with the key as \'text\'. For example, {"text": "<output goes here>"}'),
    self._construct_message('{"text": "Sure, I can return the output as a regular JSON object with the key as \'text\'. Here is an example: {\'text\': \'Your Output\'}."}', 'model')
]

        
    
          
