import json
from moodle_fetchers.moodle_connector import MoodleConnector

class GradesFetcher(MoodleConnector):
    """Classe para obter as avaliações dos estudantes."""

    def getStudentGrades(self, course_id, student_id):
        return self.requestData("gradereport_user_get_grade_items", {
            "courseid": course_id,
            "userid": student_id
        })