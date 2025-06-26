import json

from moodle_fetchers.moodle_connector import MoodleConnector
from datetime import datetime


class CourseContentFetcher(MoodleConnector):
    """Classe para obter e guardar os conteúdos da disciplina."""

    def getCourseContents(self, course_id):
        contents = self.requestData("core_course_get_contents", {"courseid": course_id})
        return contents

