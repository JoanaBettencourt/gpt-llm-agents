import requests, json, os

class MoodleConnector:
    """Classe base para interagir com a API do Moodle."""

    MOODLE_URL = "http://localhost:8081/webservice/rest/server.php"
    TOKEN = "f7589d878ac5f35a2a46583b45521b38"
    HEADERS = {"Content-Type": "application/json"}
    
    def requestData(self, function, params=None):
        """Envia uma requisição GET à API do Moodle para uma função específica."""

        if params is None:
            params = {}
        params.update({
            "wstoken": self.TOKEN,
            "wsfunction": function,
            "moodlewsrestformat": "json"
        })
        response = requests.get(self.MOODLE_URL, params=params, headers=self.HEADERS)
        return response.json()
    
    def saveData(self, filename, data):
        """Guarda os dados num ficheiro JSON."""
        path = os.path.join("dados", filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"💾 Dados guardados em {path}")

    def loadData(self, filename):
        """Carrega dados de um ficheiro JSON, se existir."""
        path = os.path.join("dados", filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None