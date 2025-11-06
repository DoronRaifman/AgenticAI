import os
from openai import OpenAI
from IPython.display import Markdown, display


class GPTLLM:
    def __init__(self):
        """Constructor initializes OpenAI connection using API key from environment"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        self.client = OpenAI(api_key=api_key)
        self.chat_session = None
        self.model = "gpt-4.1"
        # self.model = "gpt-4o"
        # self.model = "gpt-4o-mini"

    def ask(self, question: str) -> str:
        """Single question/answer interaction"""
        print(f"Question: {question}")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": question}]
        )
        response = response.choices[0].message.content
        print("Response:")
        # display(Markdown(response))
        print(response)
        return response

    def start_chat(self):
        """Initialize a chat session"""
        self.chat_session = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    def end_chat(self):
        """End the chat session"""
        self.chat_session = None

    def ask_chat(self, question: str) -> str:
        """Ask within the chat session"""
        if self.chat_session is None:
            raise ValueError("Chat not started. Call start_chat() first.")

        print(f"Question: {question}")
        # Add user message
        self.chat_session.append({"role": "user", "content": question})

        # Get response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.chat_session
        )

        answer = response.choices[0].message.content

        # Add assistant reply to session
        self.chat_session.append({"role": "assistant", "content": answer})
        print("Response:")
        # display(Markdown(response))
        print(answer)
        return answer


if __name__ == "__main__":
    gpt = GPTLLM()

    # Single ask
    print("Single ask:", gpt.ask("What is 2 + 2?"))

    # Chat mode
    gpt.start_chat()
    answer1 = gpt.ask_chat("give me 10 first numbers in Fibonacci sequence")
    answer2 = gpt.ask_chat("what of the numbers is odd?")
    answer3 = gpt.ask_chat("what is the sum of the odd numbers")
    gpt.end_chat()
