from moodle_fetchers.moodle_connector import MoodleConnector

class QuizFinder(MoodleConnector):
    """Classe para obter a lista de quizzes de um curso."""

    def getQuizzesByCourse(self, course_id):
        return self.requestData("mod_quiz_get_quizzes_by_courses", {
            "courseids[0]": course_id
        }).get("quizzes", [])