import sys
import os
import json
from datetime import datetime

# Add the 'src' directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from log_manager import LogManager

import unittest

class TestOfLogManager(unittest.TestCase):
    """
    Unit test class for testing the `LogManager` class methods.
    """
    
    def setUp(self):
        """
        Sets up the test environment by initializing the `LogManager` instance and temporary test files.
        """
        self.logger = LogManager(log_file="logs/log.txt", stats_file="logs/stats.txt")
        
        self.log_file = "test_log_file.txt"
        self.stats_file = "test_stats_file.txt"

    def tearDown(self):
        """
        Cleans up temporary files created during tests.
        """
        if os.path.exists(self.log_file):
                os.remove(self.log_file)
        if os.path.exists(self.stats_file):
            os.remove(self.stats_file)
            
    
    def test_init(self):
        """
        Verifies correct initialization with default and custom log file paths.
        """
        # Tests default log files (path)
        logger = LogManager()
        self.assertEqual(logger.log_file, "../logs/log.txt")
        self.assertEqual(logger.stats_file, "../logs/stats.txt")
        
        # Tests custom log files (path)
        custom_log_file = "custom_log.txt"
        custom_stats_file = "custom_stats.txt"
        logger = LogManager(log_file=custom_log_file, stats_file=custom_stats_file)
        
        self.assertEqual(logger.log_file, custom_log_file)
        self.assertEqual(logger.stats_file, custom_stats_file)
        
    def test_init_invalid(self):
        """
        Ensures exceptions are raised for invalid log or stats file paths.
        """
        # Tests invalid log files data type
        custom_log_file = 12
        with self.assertRaises(TypeError):
            LogManager(log_file=custom_log_file)
        
        custom_stats_file = None
        with self.assertRaises(TypeError):
            LogManager(stats_file=custom_stats_file)
            
        # Tests invalid log file type
        with self.assertRaises(ValueError):
            LogManager(log_file="test.csv")
        with self.assertRaises(ValueError):
            LogManager(log_file="test.json")
           
        # Tests invalid stats file type
        with self.assertRaises(ValueError):
            LogManager(log_file="test.csv")
        with self.assertRaises(ValueError):
            LogManager(stats_file="test.json")
        
        
    def test_log_record(self):
        """
        Validates correct formatting of log entries for questions and answers.
        """
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        question = "Kdy začíná výuka?"
        answer = "Výuka začíná většinou od 7:30. Dříve než jinde, aby měli studenti odpoledně více času."
        
        expected_log_entry = f"{current_datetime} | Question: {question} -> Answer: {answer}\n"
        
        self.assertEqual(self.logger.log_record(question, answer), expected_log_entry)
        
    
    def test_analyze_logs(self):
        """
        Confirms proper analysis of logs to extract frequently asked questions.
        """
        test_logger = LogManager(log_file=self.log_file, stats_file=self.stats_file)
        
        with open(self.log_file, "w", encoding="UTF-8") as log_file:
            log_file.write(
                "2024-12-17 16:32:58 | Question: jaká je její dostupnost MHD? -> Answer: Škola má výbornou dostupnost MHD, nachází se blízko stanic metra Karlovo náměstí a I.P. Pavlova (linka C), a také poblíž stanic náměstí I.P. Pavlova a Můstek (linky A a B).\n" +
                "2024-12-17 16:36:40 | Question: Kdy se otevírá škola? -> Answer: Škola se obvykle otevírá v 7:00.\n" +
                "2024-12-17 16:36:49 | Question: kdy se otevírá škola? -> Answer: Škola se otevírá v 7:00, přičemž první hodina začíná v 7:30.\n" +
                "2024-12-17 16:39:46 | Question: Kde se dá koupit jídlo? -> Answer: Jídlo se dá zakoupit ve školní jídelně, která nabízí obědy, nebo v blízkých bufetech a bistrech.\n"
            )

        test_logger.analyze_logs()

        results = test_logger.load_stats()

        expected_stats = [
            "kdy se otevírá škola?",
            "jaká je její dostupnost mhd?",
            "kde se dá koupit jídlo?"
        ]
        self.assertEqual(results, expected_stats)
        
        
    def test_load_stats(self):
        """
        Verifies correct loading of statistics from the stats file.
        """
        test_logger = LogManager(log_file=self.log_file, stats_file=self.stats_file)
        stats = ["kdy se otevírá škola?", "jaká je její dostupnost mhd?", "kde se dá koupit jídlo?"]

        with open(self.stats_file, "w", encoding="UTF-8") as f:
            f.write("\n".join(stats))

        result = test_logger.load_stats()
        self.assertEqual(result, stats)
        
    def test_load_stats_invalid(self):
        """
        Ensures proper behavior when the stats file is missing.
        """
        # Tests that file does not exist
        if os.path.exists(self.stats_file):
            os.remove(self.stats_file)

        test_logger = LogManager(log_file=self.log_file, stats_file=self.stats_file)

        result = test_logger.load_stats()
        self.assertEqual(result, ["Statistiky nejsou dostupné."])


    @unittest.skip("test_analyze_logs_async is not implemented.")
    async def test_analyze_logs_async(self):
        """
        Tests the asynchronous log analysis method `analyze_logs_async`.
        """
        test_logger = LogManager(log_file=self.log_file, stats_file=self.stats_file)
        
        with open(self.log_file, "w", encoding="UTF-8") as log_file:
            log_file.write(
                "2024-12-17 16:32:58 | Question: jaká je její dostupnost MHD? -> Answer: Škola má výbornou dostupnost MHD, nachází se blízko stanic metra Karlovo náměstí a I.P. Pavlova (linka C), a také poblíž stanic náměstí I.P. Pavlova a Můstek (linky A a B).\n" +
                "2024-12-17 16:36:40 | Question: Kdy se otevírá škola? -> Answer: Škola se obvykle otevírá v 7:00.\n" +
                "2024-12-17 16:36:49 | Question: kdy se otevírá škola? -> Answer: Škola se otevírá v 7:00, přičemž první hodina začíná v 7:30.\n" +
                "2024-12-17 16:39:46 | Question: Kde se dá koupit jídlo? -> Answer: Jídlo se dá zakoupit ve školní jídelně, která nabízí obědy, nebo v blízkých bufetech a bistrech.\n"
            )

        await test_logger.analyze_logs_async()

        # Verify the results
        results = test_logger.load_stats()
        expected_stats = [
            "kdy se otevírá škola?",
            "jaká je její dostupnost mhd?",
            "kde se dá koupit jídlo?"
        ]

        self.assertEqual(results, expected_stats)
        
          
    def test_get_questions(self):
        """
        Checks retrieval of most asked questions from memory.
        """
        test_logger = LogManager(log_file=self.log_file, stats_file=self.stats_file)

        test_logger.most_asked_questions = ["kdy se otevírá škola?", "jaká je její dostupnost mhd?", "kde se dá koupit jídlo?"]

        self.assertEqual(test_logger.get_questions(), test_logger.most_asked_questions)
        
        
if __name__ == "__main__":
    unittest.main()