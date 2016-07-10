import unittest
import src.spiders.pianomidi as pianomidi


class MutopiaSpiderTests(unittest.TestCase):
    def test_parse_composer(self):
        test_cases = [
            ('España, Opus 165 (1890)', ('España, Opus 165', '1890')),
            ('Fantaisie-Impromptu, Opus 66 (1834)', ('Fantaisie-Impromptu, Opus 66', '1834')),
            ('Polonaise Ab major, Opus 53', ('Polonaise Ab major, Opus 53', None))
        ]

        for text, expected_result in test_cases:
            with self.subTest('{0} -> {1}'.format(text, expected_result)):
                result = pianomidi._parse_title_string(text)
                self.assertEqual(result[0], expected_result[0])
                self.assertEqual(result[1], expected_result[1])

if __name__ == '__main__':
    unittest.main()
