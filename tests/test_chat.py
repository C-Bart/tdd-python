import unittest


class ChatClient:
    def __init__(self, nickname):
        self.nickname = nickname

    def send_message(self, message):
        sent_message = "{}: {}".format(self.nickname, message)
        self.connection.broadcast(message)
        return sent_message


class TestChatAcceptance(unittest.TestCase):
    def test_message_exchange(self):
        user1 = ChatClient("Jan Kowalski")
        user2 = ChatClient("Harry Potter")
        user1.send_message("Witaj, świecie!")
        messages = user2.fetch_message()
        assert messages == ["Jan Kowalski: Witaj, świecie!"]

    def test_send_message(self):
        client = ChatClient("Użytkownik 1")
        sent_message = client.sent_message("Witaj, świecie!")
        assert sent_message == "Użytkownik 1: Witaj, świecie!"


class TestChatClient(unittest.TestCase):
    def test_nickname(self):
        client = ChatClient("Użytkownik 1")
        assert client.nickname == "Użytkownik 1"


if __name__ == '__main__':
    unittest.main()
