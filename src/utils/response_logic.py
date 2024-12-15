import json

class Response_Logic:
    """
    Třída pro s logikou zpracovávající odpovědí podle dat z JSON souboru.
    """
    
    def __init__(self, data_file):
        """
        Inicializace instance Response_Logic.

        :param data_file (str): Cesta k JSON souboru obsahujícímu data otázek a odpovědí.
        """
        self.data_file = data_file
        self.data = self._load_data()

    def _load_data(self):
        """
        Načítá data z JSON souboru.
        """
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_topics(self):
        """
        Vrací seznam všech témat a jejich klíčových slov.
        """
        return {topic: info["keywords"] for topic, info in self.data["topics"].items()}

    def get_questions(self, keywords):
        """
        Vrací seznam otázek na základě klíčových slov.
        
        :param keywords (list[str]): Seznam klíčových slov zadaných uživatelem.
        """
        for topic, info in self.data["topics"].items():
            if any(keyword in info["keywords"] for keyword in keywords):
                return info["questions"]
        return ["O této oblasti nemám dostatek informací."]

    def get_answer(self, question):
        """
        Vrací odpověď na zadanou otázku.

        :param question (str): Otázka zadaná uživatelem.
        """
        for topic, info in self.data["topics"].items():
            if question in info["answers"]:
                return info["answers"][question]
        return "Na tohle nevím odpověď. Zkus se zeptat jinak!"
