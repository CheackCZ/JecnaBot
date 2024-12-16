from datetime import datetime

class Log_Manager():
    """
    Logging for saving questions and answers to a text file.
    """
    
    def __init__(self, log_file = "log.txt"):
        """
        Initializes the logger with a specified file.

        :param log_file (str): Path to the log file.
        """
        self.log_file = log_file
        
    def log_record(self, question, answer):
        """
        Logs the user's question and the bot's answer to the file.

        :param question (str): The user's question.
        :param answer (str): The bot's answer.
        """
        current_datetime = datetime.now().strftime("%D-%d-%Y %H:%M:%S")
        log_entry = f"{current_datetime} | Question: {question} -> Answer: {answer}\n"
        
        with open(self.log_file, "a", encoding="UTF-8") as file:
            file.write(log_entry)