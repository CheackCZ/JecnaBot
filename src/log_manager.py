import asyncio
import re
import threading

from collections import Counter
from datetime import datetime

class LogManager:
    """
    A class to manage logging of questions and answers, analyze log files, and track the most frequently asked questions.
    """
    
    def __init__(self, log_file="../logs/log.txt", stats_file="../logs/stats.txt"):
        """
        Initializes the Log_Manager instance.
        
        :param log_file (str): Path to the log file where questions and answers are recorded.
        :param stats_file (str): Path to the stats file where the top questions are stored.
        """
        if type(log_file) != str:
            raise TypeError("Soubor s logy musí být poskytnut jako string!")
        
        if type(stats_file) != str:
            raise TypeError("Soubor s nejčastějšími dotazy musí být poskytnut jako string!")
        
        if not log_file.endswith(".txt") or not stats_file.endswith(".txt"):
            raise ValueError("Soubor s logy / se statistikami, musí mít příponu .txt!")
        
        self.log_file = log_file
        self.stats_file = stats_file
        
        self.lock = threading.Lock()
        self.most_asked_questions = self.load_stats()


    def log_record(self, question, answer):
        """
        Logs a user question and its corresponding answer to the log file.
        
        :param question (str): The user's question to log.
        :param answer (str): The bot's answer corresponding to the question.
        """
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{current_datetime} | Question: {question} -> Answer: {answer}\n"

        with open(self.log_file, "a", encoding="UTF-8") as file:
            file.write(log_entry)
            
        return log_entry


    def analyze_logs(self):
        """
        Analyzes the log file to identify the top 3 most frequently asked questions.        
        """
        try:
            with open(self.log_file, "r", encoding="UTF-8") as file:
                questions = []
                for line in file:
                    match = re.search(r"Question: (.*?) ->", line)
                    if match:
                        questions.append(match.group(1).strip().lower())

            most_asked = Counter(questions).most_common(3)

            with self.lock:
                with open(self.stats_file, "w", encoding="UTF-8") as stats:
                    for question, count in most_asked:
                        stats.write(f"{question}\n")

                self.most_asked_questions = [f"{q}" for q in most_asked]

        except Exception as e:
            print(f"Chyba při analýze logů: {e}")


    def load_stats(self):
        """
        Loads the top questions from the stats file into memory.
        """
        try:
            with open(self.stats_file, "r", encoding="UTF-8") as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            return ["Statistiky nejsou dostupné."]
        except Exception as e:
            return [f"Chyba při načítání statistik: {e}"]


    async def analyze_logs_async(self):
        """
        Runs the log analysis asynchronously in a separate thread.
        """
        await asyncio.to_thread(self.analyze_logs)


    def get_questions(self):
        """
        Returns the current list of the most frequently asked questions.
        """
        with self.lock:
            return self.most_asked_questions