import unittest
import src.spiders.mutopiaproject as mutopiaproject


class MutopiaSpiderTests(unittest.TestCase):
    def test_parse_composer(self):
        test_cases = [
            ('by J. Ascher (1829–1869)', 'J. Ascher'),
            ('by I. M. F. Albéniz (1860–1909)', 'I. M. F. Albéniz'),
            ('Anonymous', 'Anonymous')
        ]

        for text, expected_result in test_cases:
            with self.subTest('{0} -> {1}'.format(text, expected_result)):
                result = mutopiaproject._parse_composer(text)
                self.assertEqual(result, expected_result)

    def test_parse_instruments(self):
        test_cases = [
            ('for Piano, Orgue', ['Piano', 'Orgue']),
            ('for Organ', ['Organ']),
            ('-', ['-'])
        ]

        for text, expected_result in test_cases:
            with self.subTest('{0} -> {1}'.format(text, expected_result)):
                result = mutopiaproject._parse_instruments(text)
                self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
