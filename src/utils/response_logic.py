import openai
import json

class Response_Logic:
    """
    Třída pro logiku zpracovávající odpovědi dynamicky pomocí OpenAI API.
    """

    def __init__(self, config_file):
        """
        Inicializace instance Response_Logic.

        :param config_file (str): Cesta k JSON souboru obsahujícímu konfiguraci.
        """
        self.config = self._load_config(config_file)
        openai.api_key = self.config["openai_api_key"]

    def _load_config(self, config_file):
        """
        Načítá konfiguraci z JSON souboru.
        """
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_answer(self, question):
        """
        Vrací odpověď z OpenAI API na otázku týkající se SPŠE Ječná.

        :param question (str): Otázka zadaná uživatelem.
        """
        prompt = (
            "You are an assistant that only provides accurate and factual information about SPŠE Ječná, "
            "a technical high school located in Prague. Avoid speculating or providing irrelevant information.\n"
            f"User question: {question}"
        )

        try:
            response = openai.chat.completions.create (
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant providing information about SPŠE Ječná."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error querying OpenAI API: {e}"
