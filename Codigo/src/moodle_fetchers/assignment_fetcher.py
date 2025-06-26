from moodle_fetchers.moodle_connector import MoodleConnector

class AssignmentFetcher(MoodleConnector):
    """Classe para obter trabalhos (assignments) e submissões da disciplina no Moodle"""

    def getAssignments(self, course_id):
        """Obtém todos os trabalhos associados ao curso."""

        return self.requestData("mod_assign_get_assignments", {"courseids[0]": course_id})

    def getSubmissions(self, assignment_id):
        """Obtém todas as submissões feitas para um trabalho específico."""
        
        return self.requestData("mod_assign_get_submissions", {"assignmentids[0]": assignment_id})
