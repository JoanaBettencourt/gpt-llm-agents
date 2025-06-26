from moodle_fetchers.moodle_connector import MoodleConnector

class CalendarFetcher(MoodleConnector):
    """Classe para obter eventos futuros do calendário da disciplina no Moodle."""

    def getUpcomingEvents(self, course_id):
        """Obtém os eventos futuros associados à disciplina."""
        
        return self.requestData("core_calendar_get_calendar_events", {
            "events[courseids][0]": course_id,
            "options[userevents]": 0,   # Ignora eventos pessoais do utilizador
            "options[siteevents]": 0    # Ignora eventos globais do site
        })
