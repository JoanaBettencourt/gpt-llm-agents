from moodle_fetchers.private_message_fetcher import PrivateMessageFetcher

def fetch(user_id, course_id=None):
    """Obtém mensagens privadas recebidas pelo utilizador e guarda as novas."""
    fetcher = PrivateMessageFetcher()
    response = fetcher.getUserMessages(user_id)

    if "messages" in response:
        new = fetcher.compareWithPreviousMessages(user_id, response["messages"])

        if new:
            print(f"📨 {len(new)} nova(s) mensagem(ns) recebida(s).")
        else:
            print("✅ Nenhuma nova mensagem.")

        filename = f"messages_user_{user_id}.json"
        fetcher.saveData(filename, response["messages"])
    else:
        print("⚠️ Erro na resposta:", response)

if __name__ == "__main__":
    fetch(user_id=3)

