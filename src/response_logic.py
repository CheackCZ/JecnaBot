import openai
import json

class Response_Logic:
    """
    Class that processes answers dynamically using the OpenAI API.
    """

    def __init__(self, config_file):
        """
        Initializes the Response_Logic instance.
        
        :param config_file (str): Path to the JSON configuration file containing server settings
        """
        self.config = config_file
        openai.api_key = self.config["openai_api_key"]

    def get_answer(self, question):
        """
        Retrieves an answer from the OpenAI API based on the user's question.

        :param question (str): The user's question to be answered.
        
        :return: Opeanai response / error.
        """
        prompt = (
            "You are an assistant that only provides accurate and factual information about SPŠE Ječná, "
            "a technical high school located in Prague. Avoid speculating or providing irrelevant information.\n"
            " Always respond in the same language as the user's input. "
            "If the user asks in Czech, respond only in Czech."
            "If the user asks in English, respond only in English."
            "Do not mix languages."
            f"User question: {question}"
        )

        try:
            response = openai.chat.completions.create (
                model="ft:gpt-4o-mini-2024-07-18:personal:jecnabot:AepbSNpA",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Chyba při volání OpenAI API: {e}")  
            return "Omlouvám se, došlo k chybě při získávání odpovědi."