import unittest
import unittest.mock

from multiprocessing.managers import SyncManager


class ChatClient:
    def __init__(self, nickname):
        self.nickname = nickname
        self._connection = None

    def send_message(self, message):
        sent_message = "{}: {}".format(self.nickname, message)
        self.connection.broadcast(sent_message)
        return sent_message

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self._get_connection()
        return self._connection

    @connection.setter
    def connection(self, value):
        if self._connection is not None:
            self._connection.close()
        self._connection = value

    def _get_connection(self):
        return Connection(("localhost", 9090))


class Connection(SyncManager):
    def __init__(self, address):
        self.register("get_messages")
        super().__init__(address=address, authkey=b'mychatsecret')
        self.connect()

    def broadcast(self, message):
        messages = self.get_messages()
        messages.append(message)


# Dummy object
# class _DummyConnection:
#     def broadcast(*args, **kwargs):
#         pass


class TestChatAcceptance(unittest.TestCase):
    def test_message_exchange(self):
        user1 = ChatClient("Jan Kowalski")
        user2 = ChatClient("Harry Potter")
        user1.send_message("Witaj, świecie!")
        messages = user2.fetch_message()
        assert messages == ["Jan Kowalski: Witaj, świecie!"]


class TestChatClient(unittest.TestCase):
    def test_nickname(self):
        client = ChatClient("Użytkownik 1")
        assert client.nickname == "Użytkownik 1"

    def test_send_message(self):
        client = ChatClient("Użytkownik 1")
        # client.connection = _DummyConnection()
        client.connection = unittest.mock.Mock()
        sent_message = client.send_message("Witaj, świecie!")
        assert sent_message == "Użytkownik 1: Witaj, świecie!"


class TestConnection(unittest.TestCase):
    def test_broadcast(self):
        with unittest.mock.patch.object(Connection, "connect"):
            c = Connection(("localhost", 9090))
        with unittest.mock.patch.object(c, "get_messages", return_value=[]):
            c.broadcast("dowolny komunikat")
            assert c.get_messages()[-1] == "dowolony komunikat"

    def test_client_connection(self):
        client = ChatClient("Użytkownik 1")
        connection_spy = unittest.mock.MagicMock()
        with unittest.mock.patch.object(client, "_get_connection", return_value=connection_spy):
            client.send_message("Witaj, świecie!")
        connection_spy.broadcast.assert_called_with(("Użytkownik 1: Witaj, świecie!"))


if __name__ == '__main__':
    unittest.main()
