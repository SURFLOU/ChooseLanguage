import unittest
from src import main
import data


class TestMainMethods(unittest.TestCase):
    def test_number_of_total_speakers(self):
        for lang in data.all_languages:
            self.assertIsNot(main.number_of_total_speakers(lang), "", msg="You didnt get correct data")

    def test_type_of_number_of_total_speakers(self):
        for lang in data.all_languages:
            self.assertTrue(isinstance(main.number_of_total_speakers(lang), int), msg="Value isn't int")

    def test_number_of_job_offers(self):
        for lang in data.all_languages:
            self.assertIsNot(main.number_of_job_offers(lang), "", msg="You didnt get correct data")

    def test_type_of_number_of_job_offers(self):
        for lang in data.all_languages:
            self.assertTrue(isinstance(main.number_of_job_offers(lang), int), msg="Value isn't int")

    def test_family_of_language(self):
        for lang in data.all_languages:
            self.assertIsNot(main.type_of_family(lang), "", msg="You didnt get correct data")

    def test_type_of_family_of_language(self):
        for lang in data.all_languages:
            self.assertTrue(isinstance(main.type_of_family(lang), str), msg="Value isn't string")


if __name__ == '__main__':
    unittest.main()
