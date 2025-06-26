from moodle_fetchers.moodle_connector import MoodleConnector

class QuizFetcher(MoodleConnector):
    """Classe para obter tentativas de quizzes e as respetivas revisões."""

    def getUserQuizAttempts(self, quiz_id, user_id):
        """Obtém todas as tentativas feitas por utilizador num quiz específico."""
        return self.requestData("mod_quiz_get_user_attempts", {
            "quizid": quiz_id,
            "userid": user_id
        })

    def getAttemptReview(self, attempt_id):
        """Obtém a revisão de uma tentativa específica de quiz."""
        return self.requestData("mod_quiz_get_attempt_review", {
            "attemptid": attempt_id
        })