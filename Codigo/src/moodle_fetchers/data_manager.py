import os
import time
from datetime import datetime
from moodle_fetchers import (
    fetch_enrollments,
    fetch_private_messages,
    fetch_forum_posts,
    fetch_grades,
    fetch_course_contents,
    fetch_assignments,
    fetch_calendar_events,
    fetch_completion_status,
    fetch_quiz_attempts
)

class MoodleDataManager:
    def __init__(self, course_id: int, user_id: int):
        self.course_id = course_id
        self.user_id = user_id
        self.logfile = "data_updates.log"
        self.ficheiros = {
            "enrollments": f"dados/enrollments_course_{course_id}.json",
            "private_messages": f"dados/messages_user_{user_id}.json",
            "forum_posts": f"dados/forum_posts_course_{course_id}.json",
            "grades": f"dados/grades_course_{course_id}.json",
            "course_contents": f"dados/course_{course_id}_contents.json",
            "assignments": f"dados/assignments_course_{course_id}.json",
            "calendar_events": f"dados/calendar_events_course_{course_id}.json",
            "quiz_attempts": f"dados/quiz_attempts_course_{course_id}.json"
        }

    def _obter_timestamps_dos_ficheiros(self):
        return {nome: os.path.getmtime(f) if os.path.exists(f) else 0 for nome, f in self.ficheiros.items()}

    def _registar_log(self, modificados):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.logfile, "a", encoding="utf-8") as f:
            if modificados:
                linha = f"[{timestamp}] Ficheiros modificados: {', '.join(modificados)}\n"
            else:
                linha = f"[{timestamp}] Nenhuma modificação\n"
            f.write(linha)

    def fetch_all(self):
        timestamps_antes = self._obter_timestamps_dos_ficheiros()

        self._obter_enrollments()
        self._obter_mensagens_privadas()
        self._obter_posts_forum()
        self._obter_grades()
        self._obter_conteudos_curso()
        self._obter_tarefas()
        self._obter_eventos_calendario()
        self._obter_estado_conclusao()
        self._obter_tentativas_quizzes()

        timestamps_depois = self._obter_timestamps_dos_ficheiros()

        modificados = [
            nome for nome in self.ficheiros
            if timestamps_depois[nome] > timestamps_antes[nome]
        ]

        if modificados:
            print(f"📝 Ficheiros atualizados: {modificados}")
        else:
            print("✅ Nenhuma alteração nos dados.")

        self._registar_log(modificados)

    def _obter_enrollments(self):
        fetch_enrollments.fetch(self.course_id)

    def _obter_mensagens_privadas(self):
        fetch_private_messages.fetch(self.user_id)

    def _obter_posts_forum(self):
        fetch_forum_posts.fetch(self.course_id)

    def _obter_grades(self):
        fetch_grades.fetch(self.course_id)

    def _obter_conteudos_curso(self):
        fetch_course_contents.fetch(self.course_id)

    def _obter_tarefas(self):
        fetch_assignments.fetch(self.course_id)

    def _obter_eventos_calendario(self):
        fetch_calendar_events.fetch(self.course_id)

    def _obter_estado_conclusao(self):
        fetch_completion_status.fetch(self.course_id)

    def _obter_tentativas_quizzes(self):
        fetch_quiz_attempts.fetch(self.course_id)