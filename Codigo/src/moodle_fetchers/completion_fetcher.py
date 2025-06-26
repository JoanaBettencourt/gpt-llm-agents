import json
from moodle_fetchers.moodle_connector import MoodleConnector


class CompletionFetcher(MoodleConnector):
    """Classe para obter o estado de conclusão das atividades da disciplina para um determinado utilizador."""

    def getActivityCompletionStatus(self, course_id, user_id):
        """Obtém o estado de conclusão de todas as atividades da disciplina para um utilizador específico."""

        return self.requestData("core_completion_get_activities_completion_status", {
            "courseid": course_id,
            "userid": user_id
        })
