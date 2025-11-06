import os
import google.generativeai as genai
from IPython.display import Markdown, display


class GeminiLLM:
    def __init__(self):
        api_key = os.environ['GOOGLE_API_KEY']
        if api_key is None:
            assert "GOOGLE_API_KEY environment variable not set"
        genai.configure(api_key=api_key)
        print(f"GOOGLE_API_KEY begins with={api_key[:8]}")
        model_list = [m.name for m in genai.list_models() if m.name.endswith('flash')]
        self.model_name = "gemini-2.5-flash"
        if f'models/{self.model_name}' in model_list:
            print(f"The {self.model_name} model is available.")
        else:
            assert f"The {self.model_name} model is not available."
        self.model = genai.GenerativeModel(self.model_name)
        print(f"Using model: {self.model_name}")
        self.chat = None

    def ask(self, prompt):
        print(f"Question: {prompt}")
        response = self.model.generate_content(prompt)
        answer = response.text
        print("Response:")
        print(answer)
        # print(Markdown(answer))
        return answer

    def start_chat(self):
        self.chat = self.model.start_chat()

    def end_chat(self):
        self.chat = None

    def ask_chat(self, prompt):
        if self.chat is None:
            self.start_chat()
        print(f"Question: {prompt}")
        response = self.chat.send_message(prompt)
        answer = response.text
        print("Response:")
        print(answer)
        # print(Markdown(answer))
        return answer


if __name__ == '__main__':
    llm = GeminiLLM()
    llm.start_chat()
    question1 = "give me 10 first numbers in Fibonacci sequence"
    answer = llm.ask_chat(question1)
    question2 = "what of the numbers is odd?"
    answer = llm.ask_chat(question2)
    question3 = "what is the sum of the odd numbers?"
    answer = llm.ask_chat(question3)
    question4 = "what is the sum of the even numbers?"
    answer = llm.ask_chat(question4)
    llm.end_chat()
