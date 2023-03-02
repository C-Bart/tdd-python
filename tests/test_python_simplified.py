import unittest


class TestEncryption(unittest.TestCase):
    def setUp(self) -> None:
        self.my_message = ""

    def test_input_exists(self):
        self.assertIsNotNone(self.my_message)

    def test_input_type(self):
        self.assertIsInstance(self.my_message, str)


if __name__ == "__main__":
    unittest.main()
