import openai
import json

class ResponseLogic:
    """
    Class that processes answers dynamically using the OpenAI API.
    """

    def __init__(self, config_file):
        """
        Initializes the ResponseLogic instance.
        
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
        prompt = self.config["ai_prompt"] + f"User question: {question}"

        try:
            response = openai.chat.completions.create (
                model=self.config["ai_model"],
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