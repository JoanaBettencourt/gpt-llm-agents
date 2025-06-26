from moodle_fetchers.moodle_connector import MoodleConnector

class PrivateMessageFetcher(MoodleConnector):
    """Classe para obter mensagens privadas recebidas por utilizador."""

    def getUserMessages(self, userid):
        """Obtém mensagens privadas recebidas (não lidas) pelo utilizador."""
        return self.requestData("core_message_get_messages", {
            "useridto": userid,
            "useridfrom": 0,
            "type": "conversations",
            "read": 0,
            "newestfirst": 1,
            "limitnum": 50
        })

    def compareWithPreviousMessages(self, userid, new_msgs):
        """Compara com mensagens anteriores guardadas e retorna apenas as novas."""
        filename = f"messages_user_{userid}.json"
        old_msgs = self.loadData(filename) or []
        old_ids = {msg["id"] for msg in old_msgs}
        return [msg for msg in new_msgs if msg["id"] not in old_ids]

    def saveMessages(self, userid, messages):
        """Guarda as mensagens atuais num ficheiro com nome baseado no ID do utilizador."""
        filename = f"messages_user_{userid}.json"
        self.saveData(filename, messages)
